import click
import datetime
import logging
from pathlib import Path
import uuid

from project.database import engine
from project.exec import hst1pass
from project.sqlops import commit_results, get_apphot, get_image_from_db, get_psf_from_db
from project.models import Parameter, Result, Image, Run, Target
from project.settings import Config


@click.command()
@click.option("-f", "--filename", help="Input fits file", required=True)
@click.option("--hmin", help="", type=int)
@click.option("--fmin", help="", type=int)
@click.option("-n", "--name", help="Optional run id", type=str, default="")
@click.option("-d", "--description", help="Description", type=str, default="")
@click.option("--apphot", help="Use APHOT PSF", is_flag=True, default=False)
def main(filename, hmin, fmin, description, name, apphot):
    
    # Log
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="logfile.txt",
        level=logging.INFO,
    )
    # logger = logging.getLogger('sqlalchemy.engine')
    # logger.setLevel(logging.DEBUG)
    logging.info("--Program Started--")
    logging.info(f"Input file: {filename}")
    logging.info(f"Params: {name=} {hmin=} {fmin=} {description=}")

    # Check if input file is in the db
    input_file = Path(filename)
    image = get_image_from_db(input_file.name)
    
    if apphot:
        psf = get_apphot("APPHOT 3.5 6 9")
    else:
        psf = get_psf_from_db(image)

    # Create parameter
    parameter = Parameter(
        hmin=hmin,
        fmin=fmin,
        psf=psf,
        out="xympqXYMUVWrd",
    )

    # Output dir path: Target, band, filename, unique id
    output_dir = Path(
        Config.OUTPUT_DIR,
        image.target_name,
        image.band,
        image.filename.replace(".fits", ""),
        datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(uuid.uuid4())[:8],
    )

    output_dir.mkdir(parents=True)  # Create the directory
    results = hst1pass(image, parameter, psf, name=name, description=description, output_dir=output_dir)
    commit_results(results)
    logging.info("Results commited to the DB")


if __name__ == "__main__":
    main()
