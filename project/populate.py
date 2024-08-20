from pathlib import Path
import datetime

from astropy.io import fits
import pandas as pd

from .models import Image, Target, PSF


def read_fits_header(fits_path: Path) -> dict:
    with fits.open(fits_path) as hdul:
        header = hdul[0].header

    header_selection = {
        "filename": fits_path.name,
        "type": fits_path.name[-8:-5],
        "path": str(fits_path.parent),
        "dateobs": (
            datetime.datetime.fromisoformat(
                header["DATE-OBS"] + "T" + header["TIME-OBS"]
            )
            if "DATE-OBS" in header and "TIME-OBS" in header
            else None
        ),
        "band": header["FILTER"] if "FILTER" in header else None,
        "exptime": header["EXPTIME"] if "EXPTIME" in header else None,
        "name": header["TARGNAME"],
        "ra": header["RA_TARG"],
        "dec": header["DEC_TARG"],
        "detector": header["DETECTOR"],
    }

    return header_selection


def build_table(fits_paths: list[Path]) -> pd.DataFrame:
    headers = []
    for fits_path in fits_paths:
        header = read_fits_header(fits_path)
        headers.append(header)
    df = pd.DataFrame(headers)
    return df


def get_targets(df: pd.DataFrame) -> dict[str, Target]:
    df_unique_targets = df[["name", "ra", "dec"]].drop_duplicates()
    targets_dict = {}
    for index, row in df_unique_targets.iterrows():
        row_dict = row.to_dict()
        target = Target(**row_dict)
        targets_dict = {target.name: target}

    return targets_dict


def get_images(df: pd.DataFrame) -> list[Image]:
    targets_dict = get_targets(df)

    df_images = df[["filename", "type", "path", "exptime", "band", "dateobs", "name"]]
    output_list = []

    for _, row in df_images.iterrows():
        row_dict = row.to_dict()
        target_name = row_dict.pop("name")
        row_dict["target"] = targets_dict[target_name]
        # Convert NaT to None
        if row_dict["dateobs"] is pd.NaT:
            row_dict["dateobs"] = None
        image = Image(**row_dict)
        output_list.append(image)

    return output_list


def get_psfs(df: pd.DataFrame) -> list[PSF]:
    pass


def list_images(data_path: Path) -> list[Image]:
    fits_paths = list(data_path.glob("**/*.fits"))
    df = build_table(fits_paths)
    images = get_images(df)
    return images


def list_psfs(data_path: Path) -> list[PSF]:
    """Generate a list of psf. Data extracted from filename"""
    fits_paths = list(data_path.glob("**/*.fits"))
    psf_list = []
    for fits_path in fits_paths:
        file_name = str(fits_path.name)
        details = file_name.replace(".fits", "").split("_")
        psf = PSF(
            filename=file_name,
            path=str(fits_path),
            psftype=details[0],
            instrument=details[1],
            band=details[2],
        )
        psf_list.append(psf)
    return psf_list
