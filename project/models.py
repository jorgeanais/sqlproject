import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Parameter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hmin: int = Field()
    fmin: float = Field()
    out: str = Field()
    extra: Optional[str] = Field(default=None)
    psf_filename: Optional[str] = Field(default=None, foreign_key="psf.filename")
    psf: Optional["PSF"] = Relationship(back_populates="parameter")
    runs: Optional["Run"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="parameter"
    )


class Target(SQLModel, table=True):
    name: str = Field(primary_key=True)
    ra: float = Field()
    dec: float = Field()
    images: List["Image"] = Relationship(back_populates="target")


class Image(SQLModel, table=True):
    filename: str = Field(primary_key=True)
    type: str = Field(index=True)
    path: str = Field()
    exptime: Optional[float] = Field(default=None)
    band: Optional[str] = Field(index=True, default=None)
    dateobs: Optional[datetime.datetime] = Field(
        default=None
    )  # ISO 8601 2008-09-15T15:53:00+05:00
    target_name: Optional[int] = Field(default=None, foreign_key="target.name")
    target: Optional["Target"] = Relationship(back_populates="images")
    runs: List["Run"] = Relationship(back_populates="image")


class Result(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    p: float = Field()
    q: float = Field()
    x_chip: float = Field()
    y_chip: float = Field()
    x_cte_corr: float = Field()
    y_cte_corr: float = Field()
    u_dist_corr_wcs: float = Field()
    v_dist_corr_wcs: float = Field()
    ra: float = Field()
    dec: float = Field()
    m_inst: float = Field()
    m_cte_corr: float = Field()
    w_cte_pixa_corr_zp: float = Field()
    
    run_id: Optional[int] = Field(default=None, foreign_key="run.id")
    run: Optional["Run"] = Relationship(back_populates="results")
    


class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    date: datetime.datetime = Field(default=datetime.datetime.now)
    image_filename: Optional[int] = Field(default=None, foreign_key="image.filename")
    image: Optional[Image] = Relationship(back_populates="runs")
    result_file: Optional[str] = Field(default=None)
    reg_xy_file: Optional[str] = Field(default=None)
    reg_rd_file: Optional[str] = Field(default=None)
    
    results: List["Result"] = Relationship(back_populates="run")
    #parameter: Optional["Parameter"] = Relationship(back_populates="result") # MOD
    
    
    parameter_id: Optional[int] = Field(default=None, foreign_key="parameter.id")
    parameter: Optional[Parameter] = Relationship(back_populates="runs")


class PSF(SQLModel, table=True):
    filename: str = Field(primary_key=True)
    path: str = Field()
    psftype: str = Field()
    instrument: str = Field()
    band: str = Field(index=True)
    
    parameter: Optional[Parameter] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="psf"
    )