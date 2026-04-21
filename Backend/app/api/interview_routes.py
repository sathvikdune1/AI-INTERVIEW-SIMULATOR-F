from fastapi import APIRouter
from Backend.app.api import results

router = APIRouter()
router.include_router(results.router)

