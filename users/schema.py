from datetime import datetime
from typing import (Optional, Union,
                    List, Annotated, Dict,
                    Literal)

from pydantic import (BaseModel, EmailStr,
                      field_validator, ConfigDict,
                      StringConstraints,
                      model_validator)
from .validators import password_validator ,email_is_valid
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from fastapi import Form

class Login(BaseModel):
    email : EmailStr
    password : str

    @model_validator(mode='before')
    @classmethod
    def validate_email_passowrd(cls , values : dict) :
        email = values.get('email')
        password = values.get('password')

        password_validator(password)

        if not email_is_valid(email=email):
            raise ValueError('Email Invalid')
        
        return values
    
class GoogleSchema(BaseModel):
    id_token : str

class RegisterForm (BaseModel):

    email : EmailStr
    password : str

    @model_validator(mode='before')
    @classmethod
    def validate_email_password(cls, values : dict):
       
        email = values.get('email')
        password = values.get('password')
        
        password_validator(password)

        if not email_is_valid(email = email) :
            raise ValueError('Email Invalid')
        
        return values
    





class Refresh(BaseModel):
    refresh_token : str

class Numbers(BaseModel):
    number_1 : int
    number_2 : int


def get_register_form_data(
    email : str = Form(...),
    password : str = Form(...)
):
     try :
          return RegisterForm(email=email , password=password)
     except ValidationError as e :
          raise RequestValidationError(errors=e.errors())

