import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

class Parameter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    hmin :int = Field()
    fmin: float = Field()
    psf: str = Field()
    out: str = Field()
    extra: Optional[str] = Field(default=None)
    
    runs: List["Run"] = Relationship(back_populates="parameter")

class Target(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name: str = Field(index=True)
    ra: float = Field()
    dec: float = Field()
    
    images: List["Image"] = Relationship(back_populates="target")

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str = Field(index=True)
    path: str = Field()
    exptime: float = Field()
    band: str = Field(index=True)
    dateobs: datetime.datetime = Field()  # ISO 8601 2008-09-15T15:53:00+05:00
    
    target_id: Optional[int] = Field(default=None, foreign_key="target.id")
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
    U_dist_corr_wcs: float = Field()
    V_dist_corr_wcs: float = Field()
    ra: float = Field()
    dec: float = Field()
    m_inst: float = Field()
    m_cte_corr: float = Field()
    w_cte_pixa_corr: float = Field()
    w_cte_pixa_corr_zp: float = Field()
    reg_xy: Optional[str] = Field(default=None,)
    reg_rd: Optional[str] = Field(default=None,)
    
    runs: List["Run"] = Relationship(back_populates="result")

class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    date: datetime.datetime = Field(default=datetime.datetime.now)
    
    image_id : Optional[int] = Field(default=None, foreign_key="image.id")
    image: Optional[Image] = Relationship(back_populates="runs")
    
    parameter_id : Optional[int] = Field(default=None, foreign_key="parameter.id")
    parameter: Optional[Parameter] = Relationship(back_populates="runs")
    
    
    result_id : Optional[int] = Field(default=None, foreign_key="result.id")
    result: Optional[Result] = Relationship(back_populates="runs")




