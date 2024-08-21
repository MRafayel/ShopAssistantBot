import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    'accept': 'application/json',
    'authorization': os.getenv("AUTHORIZATION"),
    'content-language': '3',
    'ostype': '1',
    'user-agent': os.getenv("USERAGENT"),
}

CATEGORY_URL = os.getenv("CATEGORY_URL")
CATEGORY_PAYLOAD = {}
CATEGORY_PATH = os.getenv("CATEGORY_PATH")

SUBCATEGORY_URL = os.getenv("SUBCATEGORY_URL")
SUBCATEGORY_PAYLOAD = {"parentId": 0}

PRODUCTS_URL = os.getenv("PRODUCTS_URL")
PRODUCTS_FILTER = os.getenv("PRODUCTS_FILTER")
PRODUCTS_PAYLOAD = {
    'categoryId': 0,
    'count': 20,
    'page': 1,
    'priceFrom': None,
    'priceTo': None,
    'countries': [],
    'categories': [],
    'brands': [],
    'search': None,
    'parentId': 0,
    'isDiscounted': True,
    'sortBy': 3,
}
PRODUCTS_PATH = os.getenv("PRODUCTS_PATH")

TOKEN = os.getenv("TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH")

NO_PICTURE_URL = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fd3%2F2e%2Fe2%2Fd32ee2053f293900f552148d4d5c660a.jpg&tbnid=31Mp4EmOMM-O8M&vet=12ahUKEwiYmZ2L6saEAxVkdqQEHRzJAMIQMygCegQIARBN..i&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2Fprogress-loading-bar-buffering-download-upload-and-loading-icon--568157309253508446%2F&docid=zbd50R5FfrrVmM&w=1960&h=1960&q=loading&ved=2ahUKEwiYmZ2L6saEAxVkdqQEHRzJAMIQMygCegQIARBN"
RANGES = [(1, 15), (15, 30), (30, 45), (45, 60), (60, 75), (75, 100)]