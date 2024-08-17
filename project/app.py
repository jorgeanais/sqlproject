import datetime
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine, select

from .database import create_db_and_tables, engine
from .models import Image, Result, Run, Parameter, Target
from .populate import list_images


def create_test_images():
    with Session(engine) as session:
        target_minni114 = Target(name="Minni114", ra=280.0375, dec=-30.5739)
        target_minni666 = Target(name="Minni666", ra=66.66, dec=-66.66)
        session.add(target_minni114)
        session.add(target_minni666)
        session.commit()
        
        image_test_1 = Image(
            filename="ifb444010_drc.fits",
            type="drc",
            path="MAST_2024-07-16T15_54_37.493Z/HST/ifb444020_drc.fits",
            exptime=1040,
            band="F606W",
            dateobs=datetime.datetime.fromisoformat("2024-03-07T23:51:40+00:00"),
            target_id=target_minni114.id,
        )
        image_test_2 = Image(
            filename="ifb444010_drz.fits",
            type="drz",
            path="MAST_2024-07-16T15_54_37.493Z/HST/ifb444020_drz.fits",
            exptime=1040,
            band="F606W",
            dateobs=datetime.datetime.fromisoformat("2024-03-07T23:51:40+00:00"),
            target_id=target_minni114.id,
        )
        session.add(image_test_1)
        session.add(image_test_2)
        session.commit()


# Check if image exists in the database
def check_image_exists(image: Image):
    with Session(engine) as session:
        statement = select(Image).where(Image.filename == image.filename)
        result = session.exec(statement)
        return result.one_or_none()


def populate_db_with_images():
    BASE_DATA_PATH = "/home/jorge/Documents/data/hst_data" # "/Users/jorgeanais/Documents/data/HST"
    data_path = Path(BASE_DATA_PATH)
    images = list_images(data_path)
    
    
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


def main():
    create_db_and_tables()
    # create_test_images()
    populate_db_with_images()


if __name__ == "__main__":
    main()
