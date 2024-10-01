from pathlib import Path
import datetime

from astropy.io import fits
import pandas as pd


OUTPUT_DIR: str = "/home/jorge/Documents/data/hst_output/"
IMAGE_DATA_PATH: str = "/home/jorge/Documents/data/hst/"
PSF_DATA_PATH: str = (
    "/home/jorge/Documents/code/hst1pass/sourcecode/HST1PASS/LIB/PSFs/STDPSFs/WFC3UV"
)


def build_table(fits_paths: list[Path]) -> pd.DataFrame:
    headers = []
    for fits_path in fits_paths:
        header = read_fits_header(fits_path)
        headers.append(header)
    df = pd.DataFrame(headers)
    return df


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


data_path = Path(IMAGE_DATA_PATH)
fits_paths = list(data_path.glob("**/*.fits"))
df = build_table(fits_paths)
df
