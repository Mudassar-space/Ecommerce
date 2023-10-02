from datetime import date
from typing import List

from fastapi import (APIRouter, Body, Depends, HTTPException, Query, Response,
                     status)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from apis.database import SessionLocal, engine
from auth.jwt_bearer import jwtBearer
from auth.jwt_handler import signJWT

from . import models, schemas

models.Base.metadata.create_all(engine)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:
        db.close()


router = APIRouter()


@router.post('/products', tags=['Products'], status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse,dependencies=[Depends(jwtBearer())],
             responses={
    status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
    status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(request: schemas.Product, db: Session = Depends(get_db)):
    new_category = models.Product(
        name=request.name,
        description=request.description,
        price=request.price)
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_category))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))



@router.get('/products/{Id}', tags=['Products'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductResponse},
                                                            status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                            status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                                                            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def get_by_id(Id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == Id).first()
    if not product:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(product))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.get('/products', tags=['Products'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": List[schemas.ProductResponse]},
                                                       status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                       status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                                                       status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def get_all(db: Session = Depends(get_db)):
    categories = db.query(models.Product).all()
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(categories))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.put('/products/{id}', tags=['Products'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductResponse},
                                                            status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                            status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                            status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                                                            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                                                            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def update(id: str, ques: schemas.Product, db: Session = Depends(get_db)):
    data = ques.dict()
    result = db.query(models.Product).filter(
        models.Product.id == id).update(data)
    db.commit()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        if result == 1:
            data.update({"id": int(id)})
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.delete('/products/{id}', tags=['Products'],dependencies=[Depends(jwtBearer())],  status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
    status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
    status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def Destroy(id, db: Session = Depends(get_db)):
    deleted = db.query(models.Product).filter(
        models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.post('/inventory', status_code=201, tags=['Inventory'],dependencies=[Depends(jwtBearer())], response_model=schemas.InventorySchema, responses={
    status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
    status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(inventory_request: schemas.InventorySchema, db: Session = Depends(get_db)):
    inventory = db.query(models.Inventory).filter(
        models.Inventory.product_id == inventory_request.product_id).first()
    if inventory:
        data = inventory_request.dict()
        inventory_update = db.query(models.Inventory).filter(
            models.Inventory.id == inventory.id).update(data)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(data))

    else:
        try:
            new_inventory = models.Inventory(
                product_id=inventory_request.product_id, quantity=inventory_request.quantity)
            db.add(new_inventory)
            db.commit()
            db.refresh(new_inventory)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_inventory))
        except Exception:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.get('/inventory/{Id}', tags=['Inventory'],dependencies=[Depends(jwtBearer())],  responses={status.HTTP_200_OK: {"model": schemas.InventorySchema},
                                                               status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                               status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                               status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                                                               status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def show(Id: int, db: Session = Depends(get_db)):
    inventory = db.query(models.Inventory).filter(
        models.Inventory.id == Id).first()
    if inventory:
        product = db.query(models.Product).filter(
            models.Product.id == inventory.product_id).first()
        inv_response = schemas.InventoryResponse(
            inventory_id=product.id,
            product_name=product.name,
            quantity=inventory.quantity
        )

    if not inventory:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(inv_response))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.get('/inventory', tags=['Inventory'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": List[schemas.InventoryResponse]},
                                                         status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                         status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                                                         status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def all(db: Session = Depends(get_db)):
    all_inventory = db.query(models.Inventory).all()
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(all_inventory))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.delete('/inventory/{id}', tags=['Inventory'],dependencies=[Depends(jwtBearer())], status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
    status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
    status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def Destroy(id, db: Session = Depends(get_db)):

    deleted = db.query(models.Inventory).filter(
        models.Inventory.id == id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.post('/sale', status_code=201, tags=['Sales'],dependencies=[Depends(jwtBearer())], response_model=schemas.ProductSale,
             responses={
    status.HTTP_400_BAD_REQUEST: {"model":  schemas.Responses},
    status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def create(sale: schemas.ProductSale, db: Session = Depends(get_db)):
    new_sale = models.ProductSale(product_id=sale.product_id, sale_date=sale.sale_date,
                                  quantity=sale.quantity)

    try:
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        print(db)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_sale))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.get('/sales', tags=['Sales'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": List[schemas.ProductSale]},
                                                 status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                 status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def all(start_date: date, end_date: date, product_id: int, db: Session = Depends(get_db)):
    total_revenue = (
        db.query(func.sum(models.ProductSale.quantity * models.Product.price))
        .join(models.Product)
        .filter(models.ProductSale.product_id == product_id)
        .filter(models.ProductSale.sale_date >= start_date)
        .filter(models.ProductSale.sale_date <= end_date)
        .scalar()
    )
    if total_revenue is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Product was not found")))

    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    sales_response = {
        "Product Name":  product.name,
        "Total Revenue": total_revenue,
        "Data": [start_date, end_date]}
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(sales_response))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.get('/sales/{Id}', tags=['Sales'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductSale},
                                                      status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                      status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                      status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                                                      status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def show(Id: int, db: Session = Depends(get_db)):
    sales_by_id = db.query(models.ProductSale).filter(
        models.ProductSale.id == Id).first()
    if not sales_by_id:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(sales_by_id))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.get("/revenue/daily/",  tags=['Sales'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductSale},
                                                           status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                           status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                           status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                                                           status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def analyze_daily_revenue(product_id: int, date: date = Query(...), db: Session = Depends(get_db)):
    daily_revenue = (
        db.query(func.sum(models.ProductSale.quantity * models.Product.price))
        .join(models.Product)
        .filter(models.ProductSale.sale_date == date)
        .scalar()
    )
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    daily_revenue_response = {
        "Product Name":  product.name,
        "Total Revenue": daily_revenue,
        "Date": date}
    return daily_revenue_response


@router.get("/revenue/weekly/",  tags=['Sales'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductSale},
                                                            status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                            status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                                                            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def analyze_weekly_revenue(product_id: int, start_date: date = Query(...), end_date: date = Query(...), db: Session = Depends(get_db)):
    weekly_revenue = (
        db.query(func.sum(models.ProductSale.quantity * models.Product.price))
        .join(models.Product)
        .filter(models.ProductSale.sale_date >= start_date)
        .filter(models.ProductSale.sale_date <= end_date)
        .scalar()
    )
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    daily_revenue_response = {
        "Product Name":  product.name,
        "Total Revenue": weekly_revenue,
        "Data": [start_date, end_date]}
    return daily_revenue_response


@router.get("/revenue/monthly/",  tags=['Sales'], dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductSale},
                                                             status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                             status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                             status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                                                             status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def analyze_monthly_revenue(product_id: int, year: int = Query(...), month: int = Query(...), db: Session = Depends(get_db)):
    query = (
        select([func.sum(models.ProductSale.quantity * models.Product.price)])
        .join(models.Product)
        .where(func.strftime('%Y', models.ProductSale.sale_date) == str(year))
        .where(func.strftime('%m', models.ProductSale.sale_date) == str(month))
    )
    result = db.execute(query)
    fatch_all = result.fetchall()
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    daily_revenue_response = {
        "Product Name":  product.name,
        "Total Revenue": fatch_all[0]["sum"],
        "Data": f"{year}-{month}-1"}
    return daily_revenue_response


@router.get("/revenue/annual/",  tags=['Sales'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductSale},
                                                            status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                            status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
                                                            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def analyze_daily_revenue(product_id: int, year: int = Query(...), db: Session = Depends(get_db)):
    query = (
        select([func.sum(models.ProductSale.quantity * models.Product.price)])
        .join(models.Product)
        .where(func.strftime('%Y', models.ProductSale.sale_date) == str(year))
    )
    result = db.execute(query)
    fatch_all = result.fetchall()
    product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    daily_revenue_response = {
        "Product Name":  product.name,
        "Total Revenue":  fatch_all[0]["sum"],
        "Year": year}
    return daily_revenue_response


@router.put('/sales{id}', tags=['Sales'],dependencies=[Depends(jwtBearer())], responses={status.HTTP_200_OK: {"model": schemas.ProductSale},
                                                     status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
                                                     status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
                                                     status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
                                                     status.HTTP_422_UNPROCESSABLE_ENTITY: {"model":  schemas.Responses},
                                                     status.HTTP_500_INTERNAL_SERVER_ERROR: {"model":  schemas.Responses}})
def update(id: int, para: schemas.ProductSale, db: Session = Depends(get_db)):
    data = para.dict()
    updated_sales = db.query(models.ProductSale).filter(
        models.ProductSale.id == id).update(data)
    db.commit()
    if not updated_sales:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        if updated_sales == 1:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(data))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.delete('/sales{id}', tags=['Sales'],dependencies=[Depends(jwtBearer())], status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_404_NOT_FOUND: {"model": schemas.Responses},
    status.HTTP_400_BAD_REQUEST: {"model": schemas.Responses},
    status.HTTP_401_UNAUTHORIZED: {"model": schemas.Responses},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": schemas.Responses},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.Responses}})
def delete(id, db: Session = Depends(get_db)):
    deleted_sales = db.query(models.ProductSale).filter(
        models.ProductSale.id == id).delete(synchronize_session=False)
    db.commit()
    if not deleted_sales:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(schemas.Responses(status=False, message="Not found")))
    try:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


@router.post('/signup', tags=["User"], response_model=schemas.UserSchema, status_code=status.HTTP_201_CREATED)
def add_person(user_schema: schemas.UserSchema, db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(
        models.User.email == user_schema.email).first()
    if find_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already exists")
    new_person = models.User(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        email=user_schema.email,
        password=user_schema.password
    )
    try:
        db.add(new_person)
        db.commit()
        db.refresh(new_person)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(new_person))
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(schemas.Responses))


def check_user(data: schemas.UserLoginSchema, db: Session = Depends(get_db)):
    find_user = db.query(models.User).filter(
        models.User.email == data.email).first()
    if find_user:
        return True
    return False


@router.post('/user/login/', tags=['User'])
def user_login(user: schemas.UserLoginSchema = Body(default=None), db: Session = Depends(get_db)):
    if check_user(user, db):
        return signJWT(user.email)

    else:
        return {
            'message': f'Invalid email or password'}
