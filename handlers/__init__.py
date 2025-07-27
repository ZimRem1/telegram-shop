from .user import router as user_router
from .admin import admin_router, add_product_router
from .payments import router as payments_router

__all__ = [user_router, admin_router, payments_router]
