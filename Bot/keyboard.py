import DB.requests as rq

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from GetData.Categories import save_categories
from GetData.get_categories import categories
from GetData.get_subcategory import subcategories
from aiogram.filters.callback_data import CallbackData
from config import RANGES


class StandardCallback(CallbackData, prefix="my"):
    user_id: str
    cat_id: str
    sub_id: str


async def main_kb():
    main = InlineKeyboardBuilder()
    main.add(InlineKeyboardButton(text="🤔 Ընտրել կատեգորիա", callback_data="choose_cat"))
    main.add(InlineKeyboardButton(text="😉 Զեղչերի դիապազոն", callback_data="all_discounts"))

    return main.adjust(1).as_markup()


async def go_home(category_id=None, back_option=False, back_for_discount=False):
    home_button = InlineKeyboardBuilder()

    home_button.add(InlineKeyboardButton(text="🏠 Գնալ սկիզբ", callback_data="Home"))

    if back_option:
        home_button.add(InlineKeyboardButton(text="👨‍🦯 Հետ", callback_data=f"cat_{category_id}"))
    elif back_for_discount:
        home_button.add(InlineKeyboardButton(text="👨‍🦯 Հետ", callback_data=f"allcat_{category_id}"))

    return home_button.adjust(1).as_markup()


async def get_categories(for_all=False, for_cash=False):

    if for_all:
        prefix = "allcat"
    elif for_cash:
        prefix = "cash"
    else:
        prefix = "cat"

    category_data = categories()
    category_button = InlineKeyboardBuilder()
    for category in category_data:
        category_button.add(InlineKeyboardButton(text=category.get("ParentName"),
                                                 callback_data=f"{prefix}_{category.get('ParentId')}"))

    category_button.add(InlineKeyboardButton(text="👨‍🦯 Հետ", callback_data="Home"))
    return category_button.adjust(2).as_markup()


async def get_subcategory(category_id):
    save_categories()
    subcategory_button = InlineKeyboardBuilder()
    count = 0

    for sub in subcategories(category_id=int(category_id)):
        subcategory_button.add(InlineKeyboardButton(text=f"{sub.get('SubCategoryName')} ({sub.get('SubCategoryItemCount')})",
                                                    callback_data=StandardCallback(user_id='',
                                                                                   cat_id=category_id,
                                                                                   sub_id=f"sub_{sub.get('SubCategoryId')}").pack()))
        count += sub.get("SubCategoryItemCount")

    subcategory_button.add(InlineKeyboardButton(text=f"Բոլորը ~ ({count})",
                                                callback_data=StandardCallback(user_id='',
                                                                               cat_id=f"allsub_{category_id}",
                                                                               sub_id='').pack()))
    subcategory_button.add(InlineKeyboardButton(text="👨‍🦯 Հետ", callback_data="choose_cat"))
    return subcategory_button.adjust(1).as_markup()


async def see_more(category_id, subcategory_id, user_id, count):
    # count = await rq.get_count(user_id=user_id, category_id=category_id, subcategory_id=subcategory_id)
    see_more_button = InlineKeyboardBuilder()
    see_more_button.add(InlineKeyboardButton(text=f"Տեսնել ավելին ({count})",
                                             callback_data=StandardCallback(user_id=f"more_{user_id}",
                                                                            cat_id=category_id if category_id else '',
                                                                            sub_id=subcategory_id if subcategory_id else '').pack()))

    see_more_button.add(InlineKeyboardButton(text="🏠 Գնալ սկիզբ", callback_data="Home"))

    see_more_button.add(InlineKeyboardButton(text="👨‍🦯 Հետ", callback_data=f"cat_{category_id}"))

    return see_more_button.adjust(1).as_markup()


async def make_percent_range(percents):
    result = set()
    for number in percents:
        for start, end in RANGES:
            if start <= number < end:
                result.add(f"{start}-{end}")
                break

    return result


async def percent_range(category_id):
    percents = await rq.get_percent_range(category_id=category_id)

    percent_kb = InlineKeyboardBuilder()
    cleaned_percents = [percent[0] for percent in percents]
    ranges = await make_percent_range(percents=cleaned_percents)

    for elem in ranges:
        percent_kb.add(InlineKeyboardButton(text=f"{elem} %", callback_data=f"percent_{elem}_{category_id}"))

    percent_kb.add(InlineKeyboardButton(text="👨‍🦯 Հետ", callback_data="all_discounts"))

    return percent_kb.adjust(1).as_markup()


if __name__ == '__main__':
    pass
