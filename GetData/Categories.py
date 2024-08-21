import json
import requests
import os

from config import headers, SUBCATEGORY_URL, SUBCATEGORY_PAYLOAD, CATEGORY_PATH
from datetime import datetime, timedelta
from GetData.get_categories import categories


def save_categories():
    modification_time = os.path.getmtime(CATEGORY_PATH)

    if datetime.now() - datetime.fromtimestamp(modification_time) >= timedelta(days=1):
        print("[INFO] Creating 'Categories' file")

        categories_data = categories()

        for index, category in enumerate(categories_data):
            SUBCATEGORY_PAYLOAD["parentId"] = category.get("ParentId")
            response = requests.post(url=SUBCATEGORY_URL, headers=headers, json=SUBCATEGORY_PAYLOAD)

            for subcategory in response.json().get("data").get("categories"):

                category["SubCategories"].append(
                    {
                        "SubCategoryName": subcategory.get("name"),
                        "SubCategoryId": subcategory.get("id"),
                        "SubCategoryItemCount": subcategory.get("itemCount"),
                    }
                )
            print(f"Processing {index+1}/{len(categories_data)}...")

        with open(CATEGORY_PATH, "w", encoding="UTF_8") as file:
            json.dump(categories_data, file, ensure_ascii=False, indent=4)

        print("\t --\t FILE 'Categories' CREATED")

        return True
    else:
        print("[INFO] There is no need to update 'Categories' file")
        print(f"\t--\t MODIFICATION TIME: {datetime.fromtimestamp(modification_time)}")
        print(f"\t--\t TIME PAST FROM THE MODIFICATION: {datetime.now() - datetime.fromtimestamp(modification_time)}")
        return True


if __name__ == '__main__':
    pass
