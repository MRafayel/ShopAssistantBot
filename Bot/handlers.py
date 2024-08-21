from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hbold
import Bot.keyboard as kb
from Bot.keyboard import StandardCallback
from GetData.Products import products
import DB.requests as rq
from Bot import message_maker
from config import TOKEN, NO_PICTURE_URL


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Բարև Ձեզ, ընտրեք տարբերակներից մեկը", reply_markup=await kb.main_kb())


@router.callback_query(F.data == "choose_cat")
async def choose_category(callback: CallbackQuery):
    await callback.answer(text="Ընտրեք կատեգորիան 👀")
    await callback.message.edit_text(text="Ընտրեք Ձեր նախընտրած կատեգորիան 👀",
                                     reply_markup=await kb.get_categories(for_all=False))


@router.callback_query(F.data == "all_discounts")
async def choose_category(callback: CallbackQuery):
    await callback.answer(text="Ընտրեք կատեգորիան 👀")
    await callback.message.edit_text(text="Ընտրեք Ձեր նախընտրած կատեգորիան 👀",
                                     reply_markup=await kb.get_categories(for_all=True))


@router.callback_query(F.data == "cash")
async def choose_category(callback: CallbackQuery):
    await callback.answer(text="Ընտրեք կատեգորիան 👀")
    await callback.message.edit_text(text="Ընտրեք Ձեր նախընտրած կատեգորիան 👀",
                                     reply_markup=await kb.get_categories(for_cash=True))


@router.callback_query(F.data.startswith("allcat_"))
async def choose_discount_percent(callback: CallbackQuery):
    cat_id = callback.data.split("_")[1]
    if await rq.check_discount_existence_in_data(category_id=cat_id):
        await callback.answer(text="Ձեր ախորժակին համապատասխան զեղչի դիապազոնը 😋")
        await callback.message.edit_text(text="Որոնում․․․")

        await callback.message.edit_text(text="Ընտրեք զեղչի դիապազոնը 😋",
                                         reply_markup=await kb.percent_range(category_id=cat_id))
    else:
        await callback.answer(text="Զեղչեր չեն գործում")
        await callback.message.edit_text(text="Տվյալ պահին այս կատեգորիայում զեղչեր չեն գործում",
                                         reply_markup=await kb.go_home())


@router.callback_query(F.data.startswith("cash_"))
async def choose_discount_percent(callback: CallbackQuery):
    category_id = callback.data.split("_")[1]
    await callback.message.edit_text(text="Որոնում...")
    await callback.answer(text="Ընտրեք ենթակատեգորիան 👀")
    await callback.message.edit_text(text="Ընտրեք Ձեր նախընտրած ենթակատեգորիան 👀",
                                     reply_markup=await kb.get_subcategory(category_id=category_id))


@router.callback_query(F.data.startswith("cat_"))
async def choose_subcategory(callback: CallbackQuery):
    category_id = callback.data.split("_")[1]
    await callback.message.edit_text(text="Որոնում...")
    await callback.answer(text="Ընտրեք ենթակատեգորիան 👀")
    await callback.message.edit_text(text="Ընտրեք Ձեր նախընտրած ենթակատեգորիան 👀",
                                     reply_markup=await kb.get_subcategory(category_id=category_id))


#TODO: optimize calling products function, send_last_message, product.cat_name
@router.callback_query(StandardCallback.filter(F.sub_id.startswith("sub_")))
async def get_products(callback: CallbackQuery, callback_data: StandardCallback):
    sub_id = callback_data.sub_id.split("_")[1] if "_" in callback_data.sub_id else callback_data.sub_id
    await callback.answer(text="Կատարում ենք հարցում 🕔")
    await callback.message.edit_text(text="Որոնում...")

    if callback_data.user_id:
        user_id = callback_data.user_id.split("_")[1] if "_" in callback_data.user_id else callback_data.user_id
    else:
        products(parent_category=None, sub_category=sub_id)
        user_id = callback.from_user.id

    if await rq.check_data_existence_in_user(user_id=user_id, subcategory_id=sub_id, category_id=None):
        print("[INFO] ADDING in USER DB")
        await rq.add_data_in_user(user_id=user_id, category_id=None, subcategory_id=sub_id)

    send_last_message = True
    for _ in range(5):
        product = await rq.retrieve_product(user_id=user_id, subcategory_id=sub_id, category_id=None)

        if product:
            card = await message_maker.make_product_message(product=product)
            if _ == 0:
                await callback.message.edit_text(text=f"🔹{hbold(product.cat_name)}🔹")
                # await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
            try:
                await callback.message.answer_photo(photo=product.photo if product.photo else NO_PICTURE_URL,
                                                    caption=card)
            except TelegramBadRequest:
                await callback.message.answer_photo(photo=NO_PICTURE_URL, caption=card)
        else:
            send_last_message = False
            if _ == 0:
                await callback.message.edit_text(text="Տվյալ պահին այս կատեգորիայում զեղչեր չեն գործում",
                                                 reply_markup=await kb.go_home(category_id=callback_data.cat_id,
                                                                               back_option=True))
            else:
                await callback.message.answer(text="Տվյալ պահին այսքանը",
                                              reply_markup=await kb.go_home(category_id=callback_data.cat_id,
                                                                            back_option=True))
            break

    if send_last_message:
        count = await rq.get_count(user_id=user_id, category_id=None, subcategory_id=sub_id)
        if count:
            await callback.message.answer(text="Շարունակել, վերադառնալ սկիզբ?",
                                          reply_markup=await kb.see_more(category_id=callback_data.cat_id,
                                                                         subcategory_id=sub_id,
                                                                         user_id=user_id,
                                                                         count=count)
                                          )
        else:
            await callback.message.answer(text="Տվյալ պահին այսքանը",
                                          reply_markup=await kb.go_home(category_id=callback_data.cat_id,
                                                                        back_option=True))


#TODO: optimize calling products function, send_last_message, product.cat_name
@router.callback_query(StandardCallback.filter(F.cat_id.startswith("allsub_")))
async def all_sub_products(callback: CallbackQuery, callback_data: StandardCallback):
    cat_id = callback_data.cat_id.split("_")[1] if "_" in callback_data.cat_id else callback_data.cat_id
    await callback.answer(text="Կատարում ենք հարցում 🕔")
    await callback.message.edit_text(text="Որոնում...")
    print(f"[ALL SUB] CALLBACKDATA: {callback_data}")
    if callback_data.user_id:
        user_id = callback_data.user_id.split("_")[1] if "_" in callback_data.user_id else callback_data.user_id
    else:
        products(parent_category=cat_id, sub_category=None)
        user_id = callback.from_user.id

    if await rq.check_data_existence_in_user(user_id=user_id, category_id=cat_id, subcategory_id=None):
        print("[INFO] ADDING in USER DB")
        await rq.add_data_in_user(user_id=user_id, category_id=cat_id, subcategory_id=None)

    send_last_message = True
    for _ in range(5):
        product = await rq.retrieve_product(user_id=user_id, subcategory_id=None, category_id=cat_id)

        if product:
            card = await message_maker.make_product_message(product=product)
            if _ == 0:
                await callback.message.edit_text(text=f"🔹{hbold(product.cat_name)}🔹")
                # await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
            try:
                await callback.message.answer_photo(photo=product.photo if product.photo else NO_PICTURE_URL,
                                                    caption=card)
            except TelegramBadRequest:
                await callback.message.answer_photo(photo=NO_PICTURE_URL, caption=card)
        else:
            send_last_message = False
            if _ == 0:
                await callback.message.edit_text(text="Տվյալ պահին այս կատեգորիայում զեղչեր չեն գործում",
                                                 reply_markup=await kb.go_home(category_id=cat_id,
                                                                               back_option=True)
                                                 )
            else:
                await callback.message.answer(text="Տվյալ պահին այսքանը",
                                              reply_markup=await kb.go_home(category_id=cat_id,
                                                                            back_option=True))
            break

    if send_last_message:
        count = await rq.get_count(user_id=user_id, category_id=cat_id, subcategory_id=None)
        if count:
            await callback.message.answer(text="Շարունակել, վերադառնալ սկիզբ?",
                                          reply_markup=await kb.see_more(category_id=cat_id,
                                                                         subcategory_id=None,
                                                                         user_id=user_id,
                                                                         count=count)
                                          )
        else:
            await callback.message.answer(text="Տվյալ պահին այսքանը",
                                          reply_markup=await kb.go_home(category_id=cat_id,
                                                                        back_option=True))


@router.callback_query(StandardCallback.filter(F.user_id.startswith("more_")))
async def see_more(callback: CallbackQuery, callback_data: StandardCallback):
    # user_id = callback_data.user_id.split("_")[1]
    if callback_data.sub_id:
        await get_products(callback, callback_data)
    elif callback_data.cat_id:
        await all_sub_products(callback, callback_data)


@router.callback_query(F.data == "Home")
async def go_home(callback: CallbackQuery):
    await callback.answer(text="Գլխավոր մենյու 📄")
    await callback.message.edit_text(text="Ընտրեք տարբերակներից մեկը", reply_markup=await kb.main_kb())


@router.callback_query(F.data.startswith("Back_"))
async def go_back(callback: CallbackQuery):
    method = callback.data.split("_")[1]
    if method == "cat":
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.message.answer(text="🤔 Ընտրել կատեգորիա")


@router.callback_query(F.data.startswith("percent_"))
async def products_in_percent_range(callback: CallbackQuery):
    range_start = callback.data.split("_")[1].split("-")[0]
    range_end = callback.data.split("_")[1].split("-")[1]
    cat_id = callback.data.split("_")[2]

    if not await rq.check_data_existence_in_data(category_id=int(cat_id), subcategory_id=None):
        rq.products(parent_category=cat_id, sub_category=None)

    await callback.answer(text="Կատարում ենք հարցում 🕔")
    await callback.message.edit_text(text="Որոնում...")

    discounted_products = await rq.retrieve_discounted_products(category_id=cat_id, range_start=range_start,
                                                                range_end=range_end)
    for index, product in enumerate(discounted_products):
        card = await message_maker.make_product_message(product=product)
        if index == 0:
            await callback.message.edit_text(text=f"🔹{hbold(product.cat_name)}🔹")
        try:
            await callback.message.answer_photo(photo=product.photo if product.photo else NO_PICTURE_URL,
                                                caption=card)
        except TelegramBadRequest:
            await callback.message.answer_photo(photo=NO_PICTURE_URL, caption=card)

    await callback.message.answer(text="Տվյալ պահին այսքանը",
                                  reply_markup=await kb.go_home(category_id=cat_id,
                                                                back_for_discount=True))

if __name__ == '__main__':
    pass
