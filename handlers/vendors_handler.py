from fastapi import APIRouter
from utilities.dependencies import db_dependency, token_dependency
from models.vendors_model import VendorsModel

router = APIRouter(prefix="/vendors", tags=["vendors"])

vendor = VendorsModel()

@router.post("/")
async def upgrade_to_vendor(db: db_dependency, token: token_dependency):
    return await vendor.upgrade_to_vendor(db, token)