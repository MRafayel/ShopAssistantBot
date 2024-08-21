import datetime
import requests

from config import headers, PRODUCTS_URL, PRODUCTS_PAYLOAD, PRODUCTS_FILTER
from DB.database import Session
from DB.ProductsDB import Product


def products(parent_category, sub_category):
    if parent_category:
        PRODUCTS_PAYLOAD.update({"parentId": parent_category,
                                 "categoryId": parent_category,
                                 "count": 200})
    else:
        product_filters = requests.post(url=PRODUCTS_FILTER, headers=headers, json={"categoryId": sub_category}).json()
        price_from = product_filters.get("data").get("priceFrom")
        price_to = product_filters.get("data").get("priceTo")
        PRODUCTS_PAYLOAD.update({"parentId": sub_category,
                                 "categoryId": sub_category,
                                 "priceFrom": price_from,
                                 "priceTo": price_to})

    response = requests.post(url=PRODUCTS_URL, headers=headers, json=PRODUCTS_PAYLOAD).json()

    session = Session()

    for product in response.get("data").get("list"):
        check_product = session.query(Product).filter(Product.product_id == product.get("id")).first()

        if check_product:
            if parent_category and not check_product.cat_id:
                check_product.cat_id = parent_category
                session.commit()
            elif sub_category and not check_product.sub_id:
                check_product.sub_id = sub_category
                session.commit()
            continue

        else:
            prod_to_save = Product(cat_id=parent_category,
                                   sub_id=sub_category,
                                   product_id=product.get("id"),
                                   name=product.get("name"),
                                   old_price=round(product.get("price"), 2),
                                   new_price=round(product.get("discountedPrice"), 2),
                                   discount_percent=product.get("discountPercent"),
                                   cat_name=product.get("categoryName"),
                                   photo=product.get("photo"),
                                   start_date=product.get("updatedDate").split("T")[0],
                                   term=datetime.datetime.now())

            session.add(prod_to_save)
            session.commit()

    session.close()

    print("\t --\t Data saved in 'Products'")

    return True


if __name__ == '__main__':
    pass
