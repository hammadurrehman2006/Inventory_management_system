import os
import pytest
from inventory_management_system import (
    Inventory, Sales, ElectronicProduct, ClothingProduct, GroceryProduct,
    DuplicateProductError, InsufficientStockError
)

# Sample test data
def test_add_and_get_product():
    inventory = Inventory()
    product = ElectronicProduct("e1", "Smartphone", 999.99, 10, 2, "Apple")
    inventory.add_product(product)
    assert inventory.get_product("e1").name == "Smartphone"

def test_duplicate_product():
    inventory = Inventory()
    product = ElectronicProduct("e2", "Laptop", 1299.99, 5, 3, "Dell")
    inventory.add_product(product)
    with pytest.raises(DuplicateProductError):
        inventory.add_product(product)  # Adding same again

def test_sell_product_and_sales_file_creation(tmp_path):
    # Set up temp directory
    os.chdir(tmp_path)
    inventory = Inventory()
    sales = Sales(inventory)
    product = ElectronicProduct("e3", "Tablet", 499.99, 5, 1, "Samsung")
    inventory.add_product(product)

    # Process sale
    total = sales.process_sale("e3", 2)
    assert total == 499.99 * 2
    assert os.path.exists("sales.json")

def test_insufficient_stock():
    inventory = Inventory()
    product = ElectronicProduct("e4", "Monitor", 199.99, 1, 2, "LG")
    inventory.add_product(product)
    with pytest.raises(InsufficientStockError):
        inventory.sell_product("e4", 5)

def test_remove_expired_products():
    inventory = Inventory()
    expired = GroceryProduct("g1", "Milk", 2.99, 10, "2000-01-01")  # clearly expired
    inventory.add_product(expired)
    inventory.remove_expired_products()
    assert inventory.get_product("g1") is None

def test_total_inventory_value():
    inventory = Inventory()
    inventory._products.clear()  # clear existing loaded products
    inventory.add_product(ClothingProduct("c1", "T-shirt", 19.99, 3, "M", "Cotton"))
    inventory.add_product(ElectronicProduct("c2", "Earphones", 49.99, 2, 1, "Sony"))
    total = inventory.total_inventory_value()
    assert total == pytest.approx(19.99 * 3 + 49.99 * 2, 0.01)
