# 🛍️ E-Shop for Handmade Leather & Macrame Creations

## 📖 About the Project
This is a personal e-commerce project for a professional artisan specializing in handmade leather goods and macrame creations. The goal is to build a fully functional online store where customers can browse, purchase, and learn more about the artisan's unique products.

As a beginner developer, this project is particularly challenging, as I am building it alone using Django. However, it is an important learning experience and a significant step in my journey as a developer.

## ✨ Features
- 🛒 Product listing with categories and filters
- 🛍️ Shopping cart functionality
- 💳 Secure checkout process with Stripe
- ⚙️ Admin dashboard for product
- 📱 Responsive design for mobile and desktop


## 🛠️ Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Deployment:** Pythonanywhere - live at [leatherworkintravelingdb.com](https://www.leatherworkintravelingdb.com/fr/)

## 🚀 Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/peter-francois/leatherwork-in-traveling-db.git
   cd leatherwork-in-traveling-DB
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:

   The project uses separate requirement files:
   - `requirements/base.txt` — core dependencies
   - `requirements/dev.txt` — includes base + development tools (pytest)
   - `requirements/lock.txt` — exact versions snapshot of the full environment

   For local development, install dev dependencies:
```sh
   pip install -r requirements/dev.txt
```
   To reproduce the exact environment used during development:
```sh
   pip install -r requirements/lock.txt
```

4. Copy and fill the `.env.example` file provided as a configuration template.
   ``` bash
   cd web_shop
   cp .env.example .env
   ```
5. Apply migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```sh
   python manage.py runserver
   ```
8. Open your browser and go to `http://127.0.0.1:8000/`

## 🧪 Tests
 
The project uses [pytest](https://pytest.org) with [pytest-django](https://pytest-django.readthedocs.io) and [pytest-sugar](https://github.com/Teemu/pytest-sugar) for a clean test output.
 
### Setup
 
Make sure you have installed the dev dependencies:
```sh
pip install -r requirements/dev.txt
```
 
### Configuration
 
A `pytest.ini` file is already configured at the root of the project:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = web_shop.settings
python_files = tests.py
```
 
### Running tests
 
Run all tests:
```sh
pytest -v
```
 
Run tests for a specific app:
```sh
pytest core/tests.py -v
```
 
Run a specific test class:
```sh
pytest core/tests.py::IndexViewTest -v
```
 
Run a specific test:
```sh
pytest core/tests.py::IndexViewTest::test_returns_200 -v
```
 
### Test structure
 
Each app has its own `tests.py` file. Tests are organized by view/feature:
 
```
core/tests.py        ← homepage, contact, about, sitemaps, robots.txt
catalogue/tests.py   ← products, filters, pagination
panier/tests.py      ← cart, checkout, payment
legal/tests.py       ← cgv, cookies, legal mentions, privacy policy
```



## 🤝 Contributions
Since this is a personal learning project, contributions are not expected at the moment. However, suggestions and feedback are always welcome!

## 📩 Contact
If you have any questions or want to share advice, feel free to reach out.

---
Thank you for checking out my project! 🚀

