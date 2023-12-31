
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)

from database import Base
from enums import ActiveStatus, ProductTags


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

class Product(Base):
    __tablename__='product'

    id = Column(Integer, primary_key=True,index=True)
    product_name = Column(String, index=True)
    image_href = Column(String, index=True)
    product_price = Column(String,index=True)
    product_description = Column(String,index=True)
    product_options = Column(String,index=True)
    image_url = Column(String, index=True)
    imageAlt = Column(String, index=True)
    tags = Column(Enum(ProductTags), default=ProductTags.NEW_ARRIVALS)

class FooterCategory(Base):
    __tablename__ = 'footercategory'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)
    footer_body = Column(String, index=True)
    active_status = Column(Enum(ActiveStatus), default=ActiveStatus.ACTIVE)

class DiscountCode(Base):
    __tablename__ = 'discountcode'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)
    discount_code = Column(String, index=True)
    discount_price = Column(String, index=True)
    discount_rate = Column(String, index=True)
    active_status = Column(Enum(ActiveStatus), default=ActiveStatus.ACTIVE)
    start_date =  Column(DateTime, default=datetime.now)
    end_date =  Column(DateTime, default=datetime.now)

class ProductCategory(Base):
    __tablename__ = "productcategory"

    id = Column(Integer, primary_key=True,index=True)
    category_name = Column(String, index=True)
    created_at = Column(DateTime,default=datetime.now)
    active_status = Column(Enum(ActiveStatus), default=ActiveStatus.ACTIVE)


class ProductBrand(Base):
    __tablename__ = "productbrand"

    id = Column(Integer, primary_key=True,index=True)
    brand_name = Column(String, index=True)
    created_at = Column(DateTime,default=datetime.now)
    active_status = Column(Enum(ActiveStatus), default=ActiveStatus.ACTIVE)

class ProductModel(Base):
    __tablename__ = "productmodel"

    id = Column(Integer, primary_key=True,index=True)
    model_name = Column(String, index=True)
    created_at = Column(DateTime,default=datetime.now)
    active_status = Column(Enum(ActiveStatus), default=ActiveStatus.ACTIVE)
    model_sku = Column(String, index=True)
    brand_id = Column(Integer, ForeignKey("productbrand.id"))


class Engine(Base):
    __tablename__ = "engine"

    id = Column(Integer, primary_key=True,index=True)
    engine_name = Column(String, index=True)
    created_at = Column(DateTime,default=datetime.now)
    active_status = Column(Enum(ActiveStatus), default=ActiveStatus.ACTIVE)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)