from typing import Optional
from unicodedata import category
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# from sqlalchemy import DateTime

# format = "%Y-%m-%dT%H:%M:%S.%fZ"

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



class Cate_update_response(BaseModel):
    created_on: datetime
    name: str
  

class User_response(BaseModel):
    
    name: str
    email: str
    user_id: int
    created_at: str 
    

class Account(BaseModel):
    user_id: int
    account_name: str
    initial_balance: int
    type: str
    created_at: datetime
    
    
class Account_response(BaseModel):
    user_id:int 
    account_id: int
    initial_balance: int
    created_at: datetime
    type: str
    account_name: str



    

class Responses(BaseModel):
    
    status: bool
    message: str
    

class Ledger(BaseModel):
    
    amount: int
    account_id: int
    category_Id: int
    user_id: int
    transaction: str
    transfer_to: str
    created_at: datetime
    

    
class UserSchema(BaseModel):
    firstname: str = Field(default=None)
    lastname: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(BaseModel):
    # fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    passwoed: str = Field(default=None)
