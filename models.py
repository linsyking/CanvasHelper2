#!/usr/bin/env python3

from pydantic import BaseModel, Field
from typing import Union

"""
Models
"""


class Position(BaseModel):
    left: int = Field(..., description="Left position")
    top: int = Field(..., description="Top position")
    width: int = Field(..., description="Width")
    height: int = Field(..., description="Height")


class Check(BaseModel):
    type: int


class Course(BaseModel):
    id: int
    name: str
    type: str
    maxshow: int = -1
    order: str = "normal"
    msg: str = ""


class URL(BaseModel):
    url: str
    browser: Union[str, None] = None
