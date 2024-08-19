import click
import datetime
from pathlib import Path
import uuid

from project.database import engine
from project.exec import hst1pass
from project.sqlops import commit_results, get_image_from_db, get_psf_from_db
from project.models import Parameter, Result, Image, Run, Target
from project.settings import Config


@click.command()
@click.option("-f", "--filename", help="Input fits file", required=True)
@click.option("--hmin", help="", type=int)
@click.option("--fmin", help="", type=int)
@click.option("-d", "--description", help="Description", type=int)
def main(filename, hmin, fmin, description):

    # Check if input file is in the db
    image = get_image_from_db(filename)
    print(image)
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
    results = hst1pass(image, parameter, psf, output_dir=output_dir)
    commit_results(results)


if __name__ == "__main__":
    main()
