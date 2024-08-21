# Telegram Bot Project

This project is a Telegram bot that allows users to browse categories and subcategories of products, as well as view discounts and product details. It utilizes the `aiogram` library for Telegram bot functionality and integrates with a database for product management.

## Attention! Project Is Currently Work In Progress

This project is currently under construction. Some features may not work as intended, and further updates are needed to improve functionality and stability.

## Features

- Fetches and displays categories and subcategories of products.
- Allows users to select categories to view discounted products.
- Supports displaying detailed information about each product.
- Saves category and product information in a local database.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a configuration file named config.py in the root directory and set the following variables:
  ```bash
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    DATABASE_PATH = 'sqlite:///your_database_name.db'
    CATEGORY_URL = 'YOUR_CATEGORY_API_URL'
    SUBCATEGORY_URL = 'YOUR_SUBCATEGORY_API_URL'
    PRODUCTS_URL = 'YOUR_PRODUCTS_API_URL'
    RANGES = [(0, 10), (10, 20), (20, 30)]  # Discount ranges
  ```
## Project Structure
```
├── Bot
│   ├── handlers.py            # Handles bot commands and callbacks
│   ├── keyboard.py            # Defines inline keyboards for user interaction
│   ├── message_maker.py       # Creates formatted messages for products
│   └── __init__.py            # Initializes the Bot package
├── GetData
│   ├── get_categories.py      # Fetches categories from an API
│   ├── get_subcategory.py     # Retrieves subcategories from saved categories
│   ├── Categories.py          # Manages category saving and updating
│   ├── Products.py            # Fetches and saves product data
│   └── __init__.py            # Initializes the GetData package
├── DB
│   ├── database.py            # Database setup and session management
│   ├── ProductsDB.py          # Defines Product model for SQLAlchemy
│   ├── requests.py            # Handles database requests and queries
│   ├── __init__.py            # Initializes the DB package
│   └── file.sqlite            # SQLite database file for storing data
├── config.py                  # Configuration file for API URLs and database settings
└── run.py                     # Entry point for running the bot
```
## Usage
1. Run the bot:
```bash
   python run.py
```
2. Open Telegram and search for your bot using the username you set when creating the bot.
3. Start a chat and use the commands provided by the bot to navigate through categories, subcategories, and products.