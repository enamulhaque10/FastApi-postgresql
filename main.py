from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models
from database import SessionLocal, engine

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





