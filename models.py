#!/usr/bin/env python3
"""
@Author: King
@Date: 2023-01-04 21:24:24
@Email: linsy_king@sjtu.edu.cn
"""

from pydantic import BaseModel, Field
from typing import Union
"""
Models
"""


class Check(BaseModel):
    type: int


class Course(BaseModel):
    id: int
    name: str
    type: int
    maxshow: int = -1
    order: str = "normal"
    msg: str = ""


class RequestForm(BaseModel):
    username: str
    password: str
    url: str
    bid: str
