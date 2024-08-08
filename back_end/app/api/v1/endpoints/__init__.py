from .employee import router as employees_router
from .fingerprints import router as fingerprints_router
from .timekeepings import router as timekeepings_router
from .fingerprint_machines import router as fingerprint_machines_router
from .salaries import router as salaries_router

__all__ = [
    "employees_router",
    "fingerprints_router",
    "timekeepings_router",
    "fingerprint_machines_router",
    "salaries_router"
]
