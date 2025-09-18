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

def test_product_update(setup_product_dao):
    dao = setup_product_dao
    
    # Get all products and select one to update
    products = dao.select_all()
    assert len(products) > 0
    
    # Select the first product to update
    product_to_update = products[0]
    original_id = product_to_update.id
    
    # Update the product details
    product_to_update.name = 'Updated iPhone 15 Pro'
    product_to_update.brand = 'Apple Inc.'
    product_to_update.price = 1099.99
    
    # Perform the update
    dao.update(product_to_update)
    
    # Verify the update by fetching all products again
    updated_products = dao.select_all()
    updated_product = next((p for p in updated_products if p.id == original_id), None)
    
    assert updated_product is not None
    assert updated_product.name == 'Updated iPhone 15 Pro'
    assert updated_product.brand == 'Apple Inc.'
    assert updated_product.price == 1099.99
    assert updated_product.id == original_id

def test_product_delete(setup_product_dao):
    dao = setup_product_dao
    
    # Insert a specific product to delete
    test_product = Product(None, 'Test Product to Delete', 'Test Brand', 599.99)
    inserted_id = dao.insert(test_product)
    assert inserted_id is not None
    
    # Verify the product exists
    products_before = dao.select_all()
    product_exists = any(p.id == inserted_id for p in products_before)
    assert product_exists
    
    # Delete the product
    dao.delete(inserted_id)
    
    # Verify the product no longer exists
    products_after = dao.select_all()
    product_still_exists = any(p.id == inserted_id for p in products_after)
    assert not product_still_exists
    
    # Verify the count decreased by 1
    assert len(products_after) == len(products_before) - 1

def test_product_delete_nonexistent(setup_product_dao):
    dao = setup_product_dao
    
    # Try to delete a product with an ID that doesn't exist
    products_before = dao.select_all()
    nonexistent_id = 999999  # Assuming this ID doesn't exist
    
    # This should not raise an error, but also should not affect the database
    dao.delete(nonexistent_id)
    
    # Verify no products were deleted
    products_after = dao.select_all()
    assert len(products_after) == len(products_before)

def test_product_delete_all(setup_product_dao):
    dao = setup_product_dao
    
    # Ensure there are products in the database
    products_before = dao.select_all()
    assert len(products_before) > 0
    
    # Delete all products
    dao.delete_all()
    
    # Verify all products are deleted
    products_after = dao.select_all()
    assert len(products_after) == 0

def test_product_delete_all_empty_table(setup_product_dao):
    dao = setup_product_dao
    
    # First delete all products
    dao.delete_all()
    
    # Verify table is empty
    products = dao.select_all()
    assert len(products) == 0
    
    # Try to delete all again (should not cause errors)
    dao.delete_all()
    
    # Verify table is still empty
    products_after = dao.select_all()
    assert len(products_after) == 0
