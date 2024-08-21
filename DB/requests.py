from DB.database import Session
from DB.ProductsDB import Product
from DB.UserProducts import UserProducts
from sqlalchemy import and_, or_, asc
from sqlalchemy.orm.exc import UnmappedInstanceError
from GetData.Products import products


async def check_data_existence_in_user(user_id, subcategory_id, category_id):
    session = Session()

    if category_id:
        if session.query(UserProducts).filter(and_(UserProducts.user_id == user_id,
                                                   UserProducts.cat_id == category_id)).first():
            session.close()
            return False

        else:
            session.close()
            return True
    else:
        if session.query(UserProducts).filter(and_(UserProducts.user_id == user_id,
                                                   UserProducts.sub_id == subcategory_id)).first():
            session.close()
            return False

        else:
            session.close()
            return True


async def check_data_existence_in_data(subcategory_id, category_id):
    session = Session()

    if session.query(Product).filter(or_(Product.sub_id == subcategory_id,
                                         Product.cat_id == category_id)).first():
        session.close()
        return True
    else:
        session.close()
        return False


async def check_discount_existence_in_data(category_id):
    session = Session()

    if session.query(Product.discount_percent).filter(Product.cat_id == category_id).first():
        session.close()
        return True
    else:
        session.close()
        return False


async def add_data_in_user(user_id, category_id, subcategory_id):
    session = Session()
    if category_id:
        product_ids = session.query(Product.product_id).filter(Product.cat_id == category_id).all()
    else:
        product_ids = session.query(Product.product_id).filter(Product.sub_id == subcategory_id).all()

    for product_id in product_ids:
        if session.query(UserProducts).filter(UserProducts.product_id == product_id[0]).first():
            print(f"[INFO] continue to add in user db for id: {product_id}")
            continue
        else:
            data = UserProducts(user_id=user_id,
                                product_id=product_id[0],
                                cat_id=category_id,
                                sub_id=subcategory_id
                                )
            session.add(data)
            session.commit()

    session.close()
    return True


async def retrieve_product(user_id, subcategory_id, category_id):
    session = Session()
    try:
        if category_id:
            user_product = session.query(UserProducts).filter(and_(UserProducts.cat_id == category_id,
                                                                   UserProducts.user_id == user_id)).first()
        else:
            user_product = session.query(UserProducts).filter(and_(UserProducts.sub_id == subcategory_id,
                                                                   UserProducts.user_id == user_id)).first()
        session.delete(user_product)
        session.commit()

        product = session.query(Product).filter(Product.product_id == user_product.product_id).first()

        session.close()

        return product

    except UnmappedInstanceError:
        print("Catching error")
        session.close()
        return False


async def retrieve_discounted_products(category_id, range_start, range_end):
    session = Session()

    products_to_return = session.query(Product).filter(and_(Product.cat_id == category_id,
                                                            Product.discount_percent.between(range_start, range_end)))\
        .order_by(asc(Product.discount_percent)).all()

    session.close()

    return products_to_return


async def get_count(user_id, category_id, subcategory_id):
    session = Session()
    if category_id:
        count = session.query(UserProducts).filter(and_(UserProducts.user_id == user_id,
                                                        UserProducts.cat_id == category_id)).count()
    else:
        count = session.query(UserProducts).filter(and_(UserProducts.user_id == user_id,
                                                        UserProducts.sub_id == subcategory_id)).count()

    session.close()

    return count


async def get_percent_range(category_id):
    session = Session()
    if not session.query(Product).filter(Product.cat_id == category_id).first():
        products(parent_category=category_id, sub_category=None)

    percents = session.query(Product.discount_percent).filter(Product.cat_id == category_id).order_by(asc(Product.discount_percent)).all()

    session.close()
    return percents


if __name__ == '__main__':
    pass
