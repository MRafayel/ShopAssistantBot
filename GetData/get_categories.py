import requests

from config import headers, CATEGORY_URL, CATEGORY_PAYLOAD


def categories():
    response = requests.post(url=CATEGORY_URL, headers=headers, json=CATEGORY_PAYLOAD)
    cleaned_data = []
    print(response.json())
    for category in response.json().get("data").get("categories"):
        cleaned_data.append(
            {
                "ParentName": category.get("name"),
                "ParentId": category.get("id"),
                "ParentItemCount": category.get("itemCount"),
                "ParentPhoto": category.get("photo"),
                "SubCategories": []
            }
        )

    return cleaned_data


if __name__ == '__main__':
    pass
    # categories()
