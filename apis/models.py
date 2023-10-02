from datetime import datetime
from pydantic import Field
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from .database import Base
# Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

    inventory = relationship("Inventory", back_populates="product")
    sale = relationship("ProductSale", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    product = relationship("Product", back_populates="inventory")

class ProductSale(Base):
    __tablename__ = "product_sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sale_date = Column(DateTime, default = datetime.now())
    quantity = Column(Integer)

    product = relationship("Product", back_populates="sale")



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    email = Column(String(45),nullable=False)
    password = Column(String(30), nullable=False)






















# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# from .database import Base

# from sqlalchemy.orm import relationship


# class CategoriesTableSchema(Base):

#     __tablename__ ='categories'
#     category_Id=Column(Integer,primary_key=True,index=True)
#     created_on=Column(DateTime)
#     name=Column(String)
#     users=relationship('User',back_populates='owner')
#     user_id=Column(Integer,ForeignKey('User.user_id'))
#     cate=relationship('Ledger', back_populates='led')

# class Account(Base):
    
#     __tablename__='Account'
#     account_id=Column(Integer,primary_key=True, index= True)
#     account_name=Column(String)
#     initial_balance=Column(Integer)
#     type=Column(String)
#     created_at=Column(DateTime)
#     uses=relationship('User',back_populates='account')
#     user_id=Column(Integer,ForeignKey('User.user_id'))
#     use=relationship('Ledger', back_populates='ledger')
    


# class Ledger(Base):
    
#     __tablename__='Ledger'
    
#     ledger_id=Column(Integer,primary_key=True, index= True)
#     amount=Column(Integer)
#     account_id=Column(Integer, ForeignKey('Account.account_id'))
#     category_Id=Column(Integer, ForeignKey('categories.category_Id'))
#     transaction=Column(String)
#     user_id= Column(Integer, ForeignKey('User.user_id'))
#     transfer_to=Column(String)
#     created_at=Column(DateTime)
#     ledger=relationship('Account', back_populates='use') 
#     led=relationship('CategoriesTableSchema',back_populates='cate')
#     lead=relationship('User', back_populates='urs')                                                                                                                                                                                                       
    
    
# class User(Base):
    
#     __tablename__='User'
    
#     user_id=Column(Integer,primary_key=True, index= True)
#     name=Column(String)
#     email=Column(String)
#     created_at=Column(DateTime)
#     owner=relationship('CategoriesTableSchema', back_populates='users')
#     account=relationship('Account', back_populates='uses')
#     urs=relationship('Ledger', back_populates='lead')  
    


