from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True,index=True)
    question_text = Column(String, index=True)

class Choices(Base):
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choices_text = Column(String, index=True)
    is_correct = Column(Boolean,default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))

class Slider(Base):
    __tablename__='slider'

    id = Column(Integer, primary_key=True,index=True)
    image_name = Column(String, index=True)
    image_url = Column(String, index=True)
    shop_url = Column(String, index=True)

class AddSlider(Base):
    __tablename__='addslider'

    id = Column(Integer, primary_key=True,index=True)
    image_name = Column(String, index=True)
    image_url = Column(String, index=True)
    shop_url = Column(String, index=True)
