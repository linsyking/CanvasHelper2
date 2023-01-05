#!/usr/bin/env python3
'''
@Author: King
@Date: 2023-01-04 21:24:24
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

'''
Models
'''

from pydantic import BaseModel, Field

class Position(BaseModel):
    left: int = Field(..., description="Left position")
    top: int = Field(..., description="Top position")
    width: int = Field(..., description="Width")
    height: int = Field(..., description="Height")

class Check(BaseModel):
    type: int | None = None

class Course(BaseModel):
    id: int
    name: str
    type: str
    maxshow: int | None = None
    order: str | None = None
    msg: str | None = None
