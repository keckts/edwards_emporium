# apps/antiques/views/__init__.py
from .antique_views import *
from .wishlist_views import *

# Optional: restrict what gets exported (if you want)
__all__ = [
    name for name in dir() 
    if not name.startswith("_")
]
