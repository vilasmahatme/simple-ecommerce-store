# Simple E-Commerce Store

A beginner-friendly e-commerce website built with Django, SQLite, HTML, CSS, and JavaScript.

## Features
- Product listing page
- Product details page
- Session-based shopping cart
- Register, login, and logout
- Checkout and order creation
- Order history for logged-in users
- SQLite database (created automatically by Django)

## Requirements
- Python 3.10+
- Internet connection for the first installation of Django

## Run the project
1. Extract the ZIP file and open the `simple-ecommerce-store` folder in VS Code.
2. Create and activate a virtual environment (recommended):

   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create database tables:
   ```bash
   python manage.py migrate
   ```

5. Add sample products:
   ```bash
   python manage.py seed_products
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Open http://127.0.0.1:8000/ in your browser.

## Admin (optional)
Create an administrator:
```bash
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/ to manage products and orders.

## Notes
- Checkout creates an order in the database; this demo does not collect payment or connect to a payment gateway.
- This is a learning project. Before public deployment, configure a strong secret key, set `DEBUG = False`, configure allowed hosts, use HTTPS, and review security settings.
