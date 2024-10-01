import datetime
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select

from .database import create_db_and_tables, engine
from .models import Image, Result, Run, Parameter, Target, PSF
from .populate import list_images, list_psfs
from .settings import Config


def create_test_images():
    """Manual creation of SQLModel objects"""
    with Session(engine) as session:
        target_minni114 = Target(name="MINNI144", ra=280.0375, dec=-30.5739)
        target_minni114 = Target(name="MINNI146", ra=283.05, dec=-31.94583)
        target_minni114 = Target(name="MINNI330", ra=283.9083, dec=-29.99)
        target_minni666 = Target(name="MINNI666", ra=66.66, dec=-66.66)
        session.add(target_minni114)
        session.add(target_minni666)
        session.commit()

        image_test_1 = Image(
            filename="ifb444010_drc.fits",
            type="drc",
            path="MAST_2024-07-16T15_54_37.493Z/HST/",
            exptime=1040,
            band="F606W",
            dateobs=datetime.datetime.fromisoformat("2024-03-07T23:51:40+00:00"),
            target_id=target_minni114.id,
        )
        image_test_2 = Image(
            filename="ifb444010_drz.fits",
            type="drz",
            path="MAST_2024-07-16T15_54_37.493Z/HST/",
            exptime=1040,
            band="F606W",
            dateobs=datetime.datetime.fromisoformat("2024-03-07T23:51:40+00:00"),
            target_id=target_minni114.id,
        )
        session.add(image_test_1)
        session.add(image_test_2)
        session.commit()


def check_image_exists(image: Image):
    """Check if image exists in the database"""
    with Session(engine) as session:
        statement = select(Image).where(Image.filename == image.filename)
        result = session.exec(statement)
        return result.one_or_none()


def check_psf_exists(psf: PSF):
    """Check if psf exists in the database"""
    with Session(engine) as session:
        statement = select(PSF).where(PSF.filename == psf.filename)
        result = session.exec(statement)
        return result.one_or_none()


def populate_db_with_images() -> None:
    """Read all the fits images in the IMAGE_DATA_PATH folder and add it to the database"""
    IMAGE_DATA_PATH = Config.IMAGE_DATA_PATH
    data_path = Path(IMAGE_DATA_PATH)
    images = list_images(data_path)
    print(images)

    with Session(engine) as session:
        for image in images:
            db_image = check_image_exists(image)
            if db_image is None:
                session.add(image)
            # Update path if it has changed
            elif db_image.path != image.path:
                db_image.path = image.path
                session.add(db_image)

        session.commit()


def populate_db_with_psf():
    """Read all the psf files in the PSF_DATA_PATH folder and add it to the database"""
    PSF_DATA_PATH = Config.PSF_DATA_PATH
    data_path = Path(PSF_DATA_PATH)
    psfs = list_psfs(data_path)

    with Session(engine) as session:
        for psf in psfs:
            db_psf = check_psf_exists(psf)
            if db_psf is None:
                session.add(psf)
            # Update path if it has changed
            elif db_psf.path != psf.path:
                db_psf.path = psf.path
                session.add(db_psf)

        session.commit()

def add_aperture_phot_psf():
    
    psf = PSF(
            filename="APPHOT 3.5 6 9",
            path="APPHOT 3.5 6 9",
            psftype="APPHOT",
            instrument="APPHOT",
            band="APPHOT",
        )
    
    with Session(engine) as session:
        db_psf = check_psf_exists(psf)
        if db_psf is None:
            session.add(psf)
        elif db_psf.path != psf.path:
            db_psf.path = psf.path
            session.add(db_psf)
        session.commit()

def main():
    """Run this to create the DB structure and populate it"""
    create_db_and_tables()
    # create_test_images()
    populate_db_with_images()
    populate_db_with_psf()
    add_aperture_phot_psf()


if __name__ == "__main__":
    main()
    
