from fastapi import APIRouter
from app.api import results

router = APIRouter()
router.include_router(results.router)

