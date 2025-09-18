# Ecomers (Django)

Minimal e-commerce starter built with Django 5: products, categories, session cart, and simple templates.

## Requirements
- Python 3.13+
- pip

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver 0.0.0.0:8000
```

Then open http://localhost:8000

## Admin
```bash
python manage.py createsuperuser
```

## Features
- Categories and products with slugs, price display
- Session-based cart (add/remove, subtotal)
- Pages: home, products, product detail, cart, checkout template
- Responsive templates via Pico.css CDN

## Project Structure
- `store/models.py`: Category, Product, Order, OrderItem
- `store/views.py`: product list/detail, cart, checkout
- `templates/`: base and pages

## Deploy notes
- Static and media configured; Whitenoise enabled for static files
- Use `DEBUG=False` and set `ALLOWED_HOSTS` in production