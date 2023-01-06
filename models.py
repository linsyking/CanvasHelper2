#!/usr/bin/env python3
'''
@Author: King
@Date: 2023-01-04 21:24:24
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

from pydantic import BaseModel, Field

'''
Models
'''


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
