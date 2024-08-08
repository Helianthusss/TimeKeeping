from fastapi import APIRouter

router = APIRouter()

def get_endpoints_routers():
    from .endpoints import employee, fingerprints, timekeepings, fingerprint_machines, salaries
    router.include_router(employee.router, prefix="/employees", tags=["employees"])
    router.include_router(fingerprints.router, prefix="/fingerprints", tags=["fingerprints"])
    router.include_router(timekeepings.router, prefix="/timekeepings", tags=["timekeepings"])
    router.include_router(fingerprint_machines.router, prefix="/fingerprint_machines", tags=["fingerprint_machines"])
    router.include_router(salaries.router, prefix="/salaries", tags=["salaries"])

get_endpoints_routers()
