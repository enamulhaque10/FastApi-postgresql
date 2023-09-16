from datetime import datetime
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import bindparam, text

import models
from database import SessionLocal, engine
from enums import ActiveStatus, ProductTags

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choices_text:str
    is_correct:bool

class QuestionBase(BaseModel):
    question_text:str
    choices:List[ChoiceBase]

class imagesliderBase(BaseModel):
    image_name:str
    image_url:str
    shop_url:str

class addsliderBase(BaseModel):
    image_name:str
    image_url:str
    shop_url:str

class productBase(BaseModel):
    product_name :str
    image_href  :str
    product_price :str
    product_description :str
    product_options :str
    image_url :str
    imageAlt :str
    tags :ProductTags

class footerBase(BaseModel):
    name :str
    footer_body  :str
    active_status :ActiveStatus

class discountBase(BaseModel):
    name :str
    discount_code  :str
    active_status :ActiveStatus
    start_date : datetime
    end_date : datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/choices/list/")
async def read_choices(db:db_dependency):
    result = db.query(models.Choices).all()
    if not result:
        raise HTTPException(status_code=404, detail="Choice is not found")
    return result

@app.post("/questions/")
async def create_questions (question:QuestionBase,db:db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(choices_text=choice.choices_text, is_correct=choice.is_correct,question_id=db_question.id)

        db.add(db_choice)
    db.commit()

# Slider Create

@app.post("/slider/")
async def create_slider (slider:imagesliderBase,db:db_dependency):
    db_slider = models.Slider(image_name=slider.image_name, image_url=slider.image_url, shop_url=slider.shop_url)
    db.add(db_slider)
    db.commit()
    db.refresh(db_slider)

@app.get("/slider/list/")
async def read_slider(db:db_dependency):
    result = db.query(models.Slider).all()
    if not result:
        raise HTTPException(status_code=404, detail="Slider is not found")
    return result

# Add Slider
@app.post("/add/slider/")
async def create_slider (slider:addsliderBase,db:db_dependency):
    db_slider = models.AddSlider(image_name=slider.image_name, image_url=slider.image_url, shop_url=slider.shop_url)
    db.add(db_slider)
    db.commit()
    db.refresh(db_slider)

@app.get("/add/slider/list/")
async def read_slider(db:db_dependency):
    result = db.query(models.AddSlider).all()
    if not result:
        raise HTTPException(status_code=404, detail="Slider is not found")
   
    return result

#PRODUCT

@app.post("/product/")
async def create_product(product:productBase, db:db_dependency):
    db_product = models.Product(
    product_name = product.product_name,
    image_href = product.image_href,
    product_price = product.product_price,
    product_description = product.product_description,
    product_options = product.product_options,
    image_url = product.image_url,
    imageAlt = product.imageAlt,
    tags = product.tags
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

@app.get("/product/list/")
async def product_list(db:db_dependency):
    result = db.query(models.Product).all()
    if not result:
        raise HTTPException(status_code=404, detail="Product is not found")
   
    return result

@app.get("/product/list/{tags}")
async def product_(tags:str,db:db_dependency):
    queryData = db.execute(text("SELECT * FROM Product as p where p.tags=:tags").bindparams(bindparam("tags", tags)))
    raw_data = queryData.fetchall()
    result = []

    for item in raw_data:
        object_data = {
        'product_name' : item[1],
        'image_href' : item[2],
        'product_price' : item[3],
        'product_description' : item[4],
        'product_options' : item[5],
        'image_url' : item[6],
        'imageAlt' : item[7],
        'tags' : item[8],
        }
        result.append(object_data)
    
    if not result:
        raise HTTPException(status_code=404, detail="Product is not found")
   
    return result

#FOOTER

@app.post("/footer/save/")
async def create_footer(footer:footerBase, db:db_dependency):
    request_name = footer.name
    footer_category = db.execute(text("SELECT * FROM FooterCategory as f where f.name=:request_name").bindparams(bindparam("request_name", request_name)))
    footer_category = footer_category.fetchone()
    if footer_category is None:
        db_footer = models.FooterCategory(
        name = footer.name,
        footer_body = footer.footer_body,
        active_status = footer.active_status
        )

        db.add(db_footer)
        db.commit()
        db.refresh(db_footer)
        
        
        
    else:
        raise HTTPException(status_code=400, detail="Same Footer Name Already Exist")
        
        
@app.get("/footer/list/")
async def footer_list(db:db_dependency):
    result = db.query(models.FooterCategory).all()
    if not result:
        raise HTTPException(status_code=404, detail="Active Footer is not found")
   
    return result

#DISCOUNT CODE

@app.post("/discountcode/save/")
async def discountcode_add(discount:discountBase,  db:db_dependency):
    db_discount = models.DiscountCode(
        name = discount.name,
        discount_code = discount.discount_code,
        active_status = discount.active_status,
        start_date = discount.start_date,
        end_date = discount.end_date
        )
    db.add(db_discount)
    db.commit()
    db.refresh(db_discount)

@app.get("/discount/list/")
async def discount_list(db:db_dependency):
    result = db.query(models.DiscountCode).all()
    if not result:
        raise HTTPException(status_code=404, detail="Active Discount is not found")
   
    return result






