from sqlalchemy import Integer, Column
from DB.database import Base


class UserProducts(Base):
    __tablename__ = "userproduct"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
    cat_id = Column(Integer)
    sub_id = Column(Integer)


if __name__ == '__main__':
    pass
