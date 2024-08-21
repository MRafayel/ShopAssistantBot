import datetime

from sqlalchemy import Integer, Column, DateTime, String, Float
from DB.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer)
    sub_id = Column(Integer)
    product_id = Column(Integer, unique=True)
    name = Column(String)
    old_price = Column(Float)
    new_price = Column(Float)
    discount_percent = Column(Float)
    cat_name = Column(String)
    photo = Column(String)
    start_date = Column(String)
    term = Column(DateTime, default=datetime.datetime.now())


if __name__ == '__main__':
    pass
