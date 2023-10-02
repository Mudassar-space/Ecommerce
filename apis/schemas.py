from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class Product(BaseModel):
    name : str
    description : str
    price : int
    
    
class ProductResponse(BaseModel) :
    id: int
    name : str
    description : str
    price : int
 


class InventorySchema(BaseModel):
    product_id : int
    quantity : int

class InventoryResponse(BaseModel):
    product_name: str
    quantity: int
    inventory_id: int


class ProductSale(BaseModel):
    product_id : int
    sale_date : datetime
    quantity : int 


class Responses(BaseModel):
    
    status: bool
    message: str
    

    
class UserSchema(BaseModel):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(BaseModel):
    # fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    passwoed: str = Field(default=None)
