from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = "Seed database with sample categories and products"

    def handle(self, *args, **options):
        categories = [
            ("Shoes", "Comfortable footwear for all occasions"),
            ("Bags", "Stylish bags and backpacks"),
            ("Accessories", "Watches, hats, and more"),
        ]
        created_categories = []
        for name, _ in categories:
            cat, _ = Category.objects.get_or_create(name=name)
            created_categories.append(cat)

        products = [
            ("Classic Sneakers", 6999, "Timeless design and comfort.", "Shoes"),
            ("Trail Runners", 8999, "Grip and support for the outdoors.", "Shoes"),
            ("Leather Backpack", 12999, "Durable and spacious.", "Bags"),
            ("Canvas Tote", 3999, "Lightweight everyday tote.", "Bags"),
            ("Analog Watch", 7499, "Elegant minimal face.", "Accessories"),
            ("Baseball Cap", 1999, "Adjustable and breathable.", "Accessories"),
        ]
        for title, price_cents, desc, cat_name in products:
            category = Category.objects.get(name=cat_name)
            Product.objects.get_or_create(
                title=title,
                defaults={
                    'category': category,
                    'price_cents': price_cents,
                    'description': desc,
                    'in_stock': True,
                }
            )
        self.stdout.write(self.style.SUCCESS("Seed data inserted."))

