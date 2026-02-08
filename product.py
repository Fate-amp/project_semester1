from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, Integer

Base = declarative_base()

class Product(Base):
    __tablename__ = "cosmetics"

    product_name = Column(String, primary_key=True)
    website = Column(String)
    country = Column(String)
    category = Column(String)
    subcategory = Column(String)
    image_url = Column(String)
    price = Column(Float)
    brand = Column(String)
    ingredients = Column(String)
    form = Column(String)
    type = Column(String)
    color = Column(String)
    size = Column(String)
    rating = Column(Float)
    noofratings = Column(Integer)
