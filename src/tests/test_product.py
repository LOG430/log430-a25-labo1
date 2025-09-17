from ..daos.product_dao import ProductDAO
from ..models.product import Product
import pytest

@pytest.fixture(scope="module")
def setup_product_dao():
    """Set up ProductDAO and clean up test data"""
    dao = ProductDAO()
    
    # Clean up any existing test data
    dao.delete_all()
    
    # Insert some initial test data
    dao.insert(Product(None, 'iPhone 15', 'Apple', 999.99))
    dao.insert(Product(None, 'Galaxy S24', 'Samsung', 899.99))
    dao.insert(Product(None, 'Pixel 8', 'Google', 699.99))
    
    yield dao
    
    # Clean up after tests
    dao.delete_all()
    dao.close()

def test_product_select(setup_product_dao):
    dao = setup_product_dao
    products = dao.select_all()
    assert len(products) >= 3
    
    # Check that products have the expected attributes
    for product in products:
        assert hasattr(product, 'id')
        assert hasattr(product, 'name')
        assert hasattr(product, 'brand')
        assert hasattr(product, 'price')
        assert product.id is not None
        assert product.name is not None
        assert product.brand is not None
        assert product.price is not None

def test_product_insert(setup_product_dao):
    dao = setup_product_dao
    # Create a new product
    new_product = Product(None, 'MacBook Pro', 'Apple', 1999.99)
    
    # Insert the product
    inserted_id = dao.insert(new_product)
    assert inserted_id is not None
    
    # Verify the product was inserted
    products = dao.select_all()
    product_names = [p.name for p in products]
    assert 'MacBook Pro' in product_names
    
    # Find the inserted product and verify its details
    inserted_product = next((p for p in products if p.name == 'MacBook Pro'), None)
    assert inserted_product is not None
    assert inserted_product.brand == 'Apple'
    assert inserted_product.price == 1999.99
