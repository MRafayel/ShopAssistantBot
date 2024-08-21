import json

from config import CATEGORY_PATH


def subcategories(category_id):
    with open(CATEGORY_PATH, "r", encoding="UTF-8") as file:
        categories = json.load(file)

    for cat in categories:
        if cat.get("ParentId") == category_id:
            return cat.get("SubCategories")


if __name__ == '__main__':
    pass
