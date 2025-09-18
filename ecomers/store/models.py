from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    price_cents = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def price_display(self) -> str:
        return f"${self.price_cents / 100:.2f}"


class Order(TimeStampedModel):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Order #{self.id} - {self.full_name}"

    @property
    def total_cents(self) -> int:
        return sum(item.total_cents for item in self.items.all())

    @property
    def total_display(self) -> str:
        return f"${self.total_cents / 100:.2f}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_cents = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.product.title} x {self.quantity}"

    @property
    def total_cents(self) -> int:
        return self.price_cents * self.quantity

    @property
    def total_display(self) -> str:
        return f"${self.total_cents / 100:.2f}"

# Create your models here.
