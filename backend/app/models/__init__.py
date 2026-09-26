# Importar todos os modelos aqui garante que o Alembic os descubra no autogenerate
from app.models.user import User
from app.models.category import Category
from app.models.product import Product, ProductImage
from app.models.booking import Booking
from app.models.blog_post import BlogPost
from app.models.social_post import SocialPost

__all__ = ["User", "Category", "Product", "ProductImage", "Booking", "BlogPost", "SocialPost"]
