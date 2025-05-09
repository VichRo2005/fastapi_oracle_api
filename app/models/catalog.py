from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    nombre_producto: str
    desc_producto: str
    precio: int
    imagen: str

#class ProductList(BaseModel):
#   products: List[Product]
