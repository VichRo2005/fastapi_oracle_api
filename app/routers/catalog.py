from fastapi import APIRouter, HTTPException
from app.services.catalog import get_products_by_sucursal
from app.models.catalog import Product

router = APIRouter()

@router.get("/catalog/{sucursal_id}", response_model=list[Product])
async def get_catalog(sucursal_id: int, search: str = None):
    products = get_products_by_sucursal(sucursal_id, search)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products
