from typing import List, Optional

from sqlmodel import SQLModel, Field, Session, select

from project.database import engine
from project.models import Parameter, PSF, Result, Image, Run, Target


def get_image_from_db(filename: str) -> Image:
    """Check if image is in database, otherwise it raise an error"""
    with Session(engine) as session:
        statement = select(Image).where(Image.filename == filename)
        results = session.exec(statement)
        image = results.one()

    return image


def get_psf_from_db(image: Image) -> PSF:
    """Auto find the PSF for the image based on the band"""
    with Session(engine) as session:
        statement = (
            select(PSF)
            .where(PSF.band == image.band)
            .where(PSF.psftype == "STDPSF")
            .where(PSF.instrument == "WFC3UV")
        )
        results = session.exec(statement)
        psf = results.one()

    return psf

def get_apphot(apphot: str) -> PSF:
    """Auto find the PSF for the image based on the band"""
    with Session(engine) as session:
        statement = (
            select(PSF)
            .where(PSF.filename == apphot)
        )
        results = session.exec(statement)
        psf = results.one()

    return psf

def commit_results(results: List[Result]) -> None:
    with Session(engine) as session:
        for r in results:
            session.add(r)
        session.commit()
