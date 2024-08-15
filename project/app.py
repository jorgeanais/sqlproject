import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, select

from .database import create_db_and_tables, engine
from .models import Image, Result, Run, Parameter, Target


def create_images():
    with Session(engine) as session:
        target_minni114 = Target(name="Minni114", ra=280.0375, dec=-30.5739)
        target_minni666 = Target(name="Minni666", ra=66.66, dec=-66.66)
        session.add(target_minni114)
        session.add(target_minni666)
        session.commit()
        # session.refresh(target_minni114)
        
        image_test_1 = Image(
            name="ifb444010_drc.fits",
            type="drc",
            path="Minni144_reccomendedfile/MAST_2024-07-16T15_54_37.493Z/HST/ifb444020_drc.fits",
            exptime=1040,
            band="F606W",
            dateobs=datetime.datetime.fromisoformat("2024-03-07T23:51:40+00:00"),
            target_id=target_minni114.id
        )
        image_test_2 = Image(
            name="ifb444010_drz.fits",
            type="drz",
            path="Minni144_reccomendedfile/MAST_2024-07-16T15_54_37.493Z/HST/ifb444020_drz.fits",
            exptime=1040,
            band="F606W",
            dateobs=datetime.datetime.fromisoformat("2024-03-07T23:51:40+00:00"),
            target_id=target_minni114.id
        )
        session.add(image_test_1)
        session.add(image_test_2)
        session.commit()

def select_images():
    with Session(engine) as session:
        statement = select(Image, Target).where(Image.target_id == Target.id)
        results = session.exec(statement)
        for im, target in results:
            print("Image:", im, "Target:", target)

def select_images_alt1():
    with Session(engine) as session:
        statement = select(Image, Target).join(Target)
        results = session.exec(statement)
        for im, target in results:
            print("Image:", im, "Target:", target)


def main():
    create_db_and_tables()
    create_images()
    select_images_alt1()


if __name__ == "__main__":
    main()