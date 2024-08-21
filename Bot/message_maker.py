from aiogram.utils.markdown import hbold, hcode, hitalic
from DB.ProductsDB import Product


async def make_product_message(product: Product):
    card = f"{hbold('Անվանումը:')} {hitalic(product.name)}\n\n" \
           f"{hbold('Հին գին:')} {product.old_price}\n\n" \
           f"{hbold('Նոր գին:')} {product.new_price}\n\n" \
           f"{hbold('Զեղչի տոկոս:')} {hcode(product.discount_percent)}%\n\n" \
           f"{hbold('Գործում է:')} {hcode(product.start_date)} - ից\n\n"

    return card

if __name__ == '__main__':
    pass
