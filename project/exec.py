import datetime
from pathlib import Path
from typing import List, Optional
import shutil
import subprocess

from astropy.table import Table
from sqlmodel import Session, select

from project.database import engine
from project.models import Image, Parameter, PSF, Result, Run, Target


def hst1pass(
    image: Image,
    parameter: Parameter,
    psf: PSF,
    name: str = "",
    description: str = "",
    output_dir: Optional[Path] = None
) -> List[Result]:
    
    options = [
        f"HMIN={parameter.hmin}",
        f"FMIN={parameter.fmin}",
        f"PSF={psf.path}/{psf.filename}" ,
        "REG=xy",
        "REG=rd",
        "OUTPUT=xympqXYMUVWrd",
    ]
    
    cmd = ["hst1pass.e"]
    cmd += options
    image_path = Path(image.path) / image.filename
    cmd += [str(image_path)]
    print(cmd)
    
    # Excecute command
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Salida estándar:", result.stdout)
    print("Salida de error:", result.stderr)
    
    if result.returncode == 0:
        print("Command executed successfully.")
    else:
        print("Command failed with return code:", result.returncode)
        print("Error message:", result.stderr)
        raise RuntimeError('Failed to execute command') 
    
    # Expected resulting files
    result_file = image.filename.replace(".fits", ".xympqXYMUVWrd")
    reg_xy_file = image.filename.replace(".fits", "_xy.reg")
    reg_rd_file = image.filename.replace(".fits", "_rd.reg")
    
    # Read results
    COLUMNS = ["x", "y", "m", "p", "q", "X", "Y", "M", "U", "V", "W", "r", "d"]
    t = Table.read(result_file, format="ascii", names=COLUMNS)
    
    # Move results
    if output_dir is not None:
        result_file = shutil.move(Path(".") / result_file, output_dir)  # Agregar un hash
        reg_xy_file = shutil.move(Path(".") / reg_xy_file, output_dir)  # Agregar un hash
        reg_rd_file = shutil.move(Path(".") / reg_rd_file, output_dir)  # Agregar un hash
    
    
    run = Run(
        name=name,
        description=description,
        date=datetime.datetime.now(),
        image_filename=image.filename,
        image=image,
        result_file=result_file,
        reg_xy_file=reg_xy_file,
        reg_rd_file=reg_rd_file,
        parameter=parameter,
    )
    
    
    
    # Generate output objects
    results = []
    for row in t:
        result = Result(
            p=row["p"],
            q=row["q"],
            x_chip=row["x"],
            y_chip=row["y"],
            x_cte_corr=row["X"],
            y_cte_corr=row["Y"],
            u_dist_corr_wcs=row["U"],
            v_dist_corr_wcs=row["V"],
            ra=row["r"],
            dec=row["d"],
            m_inst=row["m"],
            m_cte_corr=row["M"],
            w_cte_pixa_corr_zp=row["W"],
            run=run
        )
        results.append(result)
    
    
    
    
    
    return results