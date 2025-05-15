import json
import os
from datetime import datetime, date
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    filename='inventory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Custom exceptions
class InventoryError(Exception):
    """Base exception for inventory-related errors"""
    pass

class DuplicateProductError(InventoryError):
    """Raised when adding a product with a duplicate ID"""
    pass

class InsufficientStockError(InventoryError):
    """Raised when selling more than available stock"""
    pass

class InvalidProductDataError(InventoryError):
    """Raised when loading invalid product data"""
    pass

class Product(ABC):
    """Abstract base class for products"""
    def __init__(self, product_id: str, name: str, price: float, quantity: int):
        """Initialize a product with ID, name, price, and quantity"""
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity = quantity

    @property
    def product_id(self) -> str:
        """Get product ID"""
        return self._product_id

    @property
    def name(self) -> str:
        """Get product name"""
        return self._name

    @property
    def price(self) -> float:
        """Get product price"""
        return self._price

    @property
    def quantity(self) -> int:
        """Get product quantity"""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        """Set product quantity with validation"""
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value

    def restock(self, amount: int) -> None:
        """Increase stock by the specified amount"""
        if amount < 0:
            raise ValueError("Restock amount cannot be negative")
        self.quantity += amount
        logging.info(f"Restocked {self.name} by {amount} units")

    def sell(self, quantity: int) -> None:
        """Reduce stock by the specified quantity"""
        if quantity < 0:
            raise ValueError("Sell quantity cannot be negative")
        if quantity > self.quantity:
            raise InsufficientStockError(f"Insufficient stock for {self.name}. Available: {self.quantity}")
        self.quantity -= quantity
        logging.info(f"Sold {quantity} units of {self.name}")

    def get_total_value(self) -> float:
        """Calculate total value of stock (price * quantity)"""
        return self.price * self.quantity

    def __str__(self) -> str:
        """Return formatted string of product info"""
        return f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.quantity}"

    @abstractmethod
    def get_details(self) -> dict:
        """Return product details as a dictionary"""
        pass

    def to_dict(self) -> dict:
        """Convert product to dictionary for serialization"""
        return {
            'product_id': self._product_id,
            'name': self._name,
            'price': self._price,
            'quantity': self._quantity,
            'type': self.__class__.__name__
        }

class ElectronicProduct(Product):
    """Concrete class for electronic products"""
    def __init__(self, product_id: str, name: str, price: float, quantity: int, warranty_years: int, brand: str):
        """Initialize an electronic product"""
        super().__init__(product_id, name, price, quantity)
        self._warranty_years = warranty_years
        self._brand = brand

    def get_details(self) -> dict:
        """Return electronic product details"""
        return {
            'product_id': self._product_id,
            'name': self._name,
            'price': self._price,
            'quantity': self._quantity,
            'warranty_years': self._warranty_years,
            'brand': self._brand
        }

    def to_dict(self) -> dict:
        """Convert to dictionary with electronic-specific attributes"""
        base_dict = super().to_dict()
        base_dict['warranty_years'] = self._warranty_years
        base_dict['brand'] = self._brand
        return base_dict

    def __str__(self) -> str:
        """Return formatted string with electronic-specific info"""
        return f"{super().__str__()}, Warranty: {self._warranty_years} years, Brand: {self._brand}"

class ClothingProduct(Product):
    """Concrete class for clothing products"""
    def __init__(self, product_id: str, name: str, price: float, quantity: int, size: str, material: str):
        """Initialize a clothing product"""
        super().__init__(product_id, name, price, quantity)
        self._size = size
        self._material = material

    def get_details(self) -> dict:
        """Return clothing product details"""
        return {
            'product_id': self._product_id,
            'name': self._name,
            'price': self._price,
            'quantity': self._quantity,
            'size': self._size,
            'material': self._material
        }

    def to_dict(self) -> dict:
        """Convert to dictionary with clothing-specific attributes"""
        base_dict = super().to_dict()
        base_dict['size'] = self._size
        base_dict['material'] = self._material
        return base_dict

    def __str__(self) -> str:
        """Return formatted string with clothing-specific info"""
        return f"{super().__str__()}, Size: {self._size}, Material: {self._material}"

class GroceryProduct(Product):
    """Concrete class for grocery products"""
    def __init__(self, product_id: str, name: str, price: float, quantity: int, expiry_date: str):
        """Initialize a grocery product with expiry date"""
        super().__init__(product_id, name, price, quantity)
        try:
            self._expiry_date = date.fromisoformat(expiry_date)
        except ValueError:
            raise InvalidProductDataError("Invalid expiry date format. Use YYYY-MM-DD")

    def is_expired(self) -> bool:
        """Check if the grocery product is expired"""
        return date.today() > self._expiry_date

    def get_details(self) -> dict:
        """Return grocery product details"""
        return {
            'product_id': self._product_id,
            'name': self._name,
            'price': self._price,
            'quantity': self._quantity,
            'expiry_date': self._expiry_date.isoformat(),
            'is_expired': self.is_expired()
        }

    def to_dict(self) -> dict:
        """Convert to dictionary with grocery-specific attributes"""
        base_dict = super().to_dict()
        base_dict['expiry_date'] = self._expiry_date.isoformat()
        return base_dict

    def __str__(self) -> str:
        """Return formatted string with grocery-specific info"""
        return f"{super().__str__()}, Expiry: {self._expiry_date}, Expired: {self.is_expired()}"

class Inventory:
    """Manages the inventory of products"""
    def __init__(self):
        """Initialize an empty inventory"""
        self._products: Dict[str, Product] = {}
        self._data_file = 'inventory.json'
        self.load_inventory()

    def add_product(self, product: Product) -> None:
        """Add a product to the inventory"""
        if product.product_id in self._products:
            raise DuplicateProductError(f"Product with ID {product.product_id} already exists")
        self._products[product.product_id] = product
        self.save_inventory()
        logging.info(f"Added product: {product.name} (ID: {product.product_id})")

    def remove_product(self, product_id: str) -> None:
        """Remove a product from the inventory"""
        if product_id not in self._products:
            raise ValueError(f"Product with ID {product_id} not found")
        product = self._products.pop(product_id)
        self.save_inventory()
        logging.info(f"Removed product: {product.name} (ID: {product_id})")

    def search_by_name(self, name: str) -> List[Product]:
        """Search products by name (case-insensitive)"""
        return [p for p in self._products.values() if name.lower() in p.name.lower()]

    def search_by_type(self, product_type: str) -> List[Product]:
        """Search products by type"""
        return [p for p in self._products.values() if p.__class__.__name__ == product_type]

    def list_all_products(self) -> List[dict]:
        """List all products with details"""
        return [product.get_details() for product in self._products.values()]

    def sell_product(self, product_id: str, quantity: int) -> float:
        """Sell a quantity of a product and return total price"""
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        product.sell(quantity)
        self.save_inventory()
        logging.info(f"Sold {quantity} units of {product.name} (ID: {product_id})")
        return product.price * quantity

    def restock_product(self, product_id: str, quantity: int) -> None:
        """Restock a product with the specified quantity"""
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        product.restock(quantity)
        self.save_inventory()
        logging.info(f"Restocked {product.name} (ID: {product_id}) with {quantity} units")

    def total_inventory_value(self) -> float:
        """Calculate total value of all products in inventory"""
        return sum(product.get_total_value() for product in self._products.values())

    def remove_expired_products(self) -> None:
        """Remove all expired grocery products"""
        expired_ids = [p.product_id for p in self._products.values() 
                      if isinstance(p, GroceryProduct) and p.is_expired()]
        for pid in expired_ids:
            self.remove_product(pid)
        if expired_ids:
            logging.info(f"Removed expired products: {expired_ids}")

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieve a product by ID"""
        return self._products.get(product_id)

    def save_inventory(self) -> None:
        """Save inventory to JSON file"""
        try:
            with open(self._data_file, 'w') as f:
                json.dump([product.to_dict() for product in self._products.values()], f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save inventory: {str(e)}")
            raise InvalidProductDataError(f"Failed to save inventory: {str(e)}")

    def load_inventory(self) -> None:
        """Load inventory from JSON file"""
        if not os.path.exists(self._data_file):
            return
        try:
            with open(self._data_file, 'r') as f:
                data = json.load(f)
                for item in data:
                    if item['type'] == 'ElectronicProduct':
                        product = ElectronicProduct(
                            item['product_id'],
                            item['name'],
                            item['price'],
                            item['quantity'],
                            item['warranty_years'],
                            item['brand']
                        )
                    elif item['type'] == 'ClothingProduct':
                        product = ClothingProduct(
                            item['product_id'],
                            item['name'],
                            item['price'],
                            item['quantity'],
                            item['size'],
                            item['material']
                        )
                    elif item['type'] == 'GroceryProduct':
                        product = GroceryProduct(
                            item['product_id'],
                            item['name'],
                            item['price'],
                            item['quantity'],
                            item['expiry_date']
                        )
                    else:
                        raise InvalidProductDataError(f"Unknown product type: {item.get('type')}")
                    self._products[product.product_id] = product
            logging.info("Inventory loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load inventory: {str(e)}")
            raise InvalidProductDataError(f"Failed to load inventory: {str(e)}")

class Sales:
    """Manages sales operations"""
    def __init__(self, inventory: Inventory):
        """Initialize sales with an inventory"""
        self._inventory = inventory
        self._sales_log: List[dict] = []
        self._sales_file = 'sales.json'
        self.load_sales()

    def process_sale(self, product_id: str, quantity: int) -> float:
        """Process a sale and update inventory"""
        total_price = self._inventory.sell_product(product_id, quantity)
        sale_record = {
            'sale_id': f"SALE_{len(self._sales_log) + 1}",
            'product_id': product_id,
            'product_name': self._inventory.get_product(product_id).name,
            'quantity': quantity,
            'total_price': total_price,
            'timestamp': datetime.now().isoformat()
        }
        self._sales_log.append(sale_record)
        self.save_sales()
        logging.info(f"Sale processed: {sale_record['product_name']} x{quantity} for ${total_price:.2f}")
        return total_price

    def get_sales_history(self) -> List[dict]:
        """Retrieve sales history"""
        return self._sales_log

    def save_sales(self) -> None:
        """Save sales to JSON file"""
        try:
            with open(self._sales_file, 'w') as f:
                json.dump(self._sales_log, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save sales: {str(e)}")
            raise InvalidProductDataError(f"Failed to save sales: {str(e)}")

    def load_sales(self) -> None:
        """Load sales from JSON file"""
        if not os.path.exists(self._sales_file):
            return
        try:
            with open(self._sales_file, 'r') as f:
                self._sales_log = json.load(f)
            logging.info("Sales history loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load sales: {str(e)}")
            raise InvalidProductDataError(f"Failed to load sales: {str(e)}")

def cli_menu():
    """Run a CLI menu for inventory management"""
    inventory = Inventory()
    sales = Sales(inventory)
    
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Sell Product")
        print("3. Search/View Products")
        print("4. Save Inventory")
        print("5. Load Inventory")
        print("6. Remove Expired Products")
        print("7. Total Inventory Value")
        print("8. Exit")
        choice = input("Enter choice: ")
        
        try:
            if choice == "1":
                product_type = input("Product type (Electronic/Clothing/Grocery): ")
                product_id = input("Product ID: ")
                name = input("Name: ")
                price = float(input("Price: "))
                quantity = int(input("Quantity: "))
                
                if product_type == "Electronic":
                    warranty_years = int(input("Warranty years: "))
                    brand = input("Brand: ")
                    product = ElectronicProduct(product_id, name, price, quantity, warranty_years, brand)
                elif product_type == "Clothing":
                    size = input("Size: ")
                    material = input("Material: ")
                    product = ClothingProduct(product_id, name, price, quantity, size, material)
                elif product_type == "Grocery":
                    expiry_date = input("Expiry date (YYYY-MM-DD): ")
                    product = GroceryProduct(product_id, name, price, quantity, expiry_date)
                else:
                    print("Invalid product type")
                    continue
                inventory.add_product(product)
                print("Product added!")
            
            elif choice == "2":
                product_id = input("Product ID: ")
                quantity = int(input("Quantity: "))
                total = sales.process_sale(product_id, quantity)
                print(f"Sale processed! Total: ${total:.2f}")
            
            elif choice == "3":
                print("\nSearch by: 1. Name, 2. Type, 3. List All")
                search_choice = input("Choice: ")
                if search_choice == "1":
                    name = input("Enter name: ")
                    results = inventory.search_by_name(name)
                    for p in results:
                        print(p)
                elif search_choice == "2":
                    p_type = input("Enter type (Electronic/Clothing/Grocery): ")
                    results = inventory.search_by_type(p_type)
                    for p in results:
                        print(p)
                elif search_choice == "3":
                    for p in inventory.list_all_products():
                        print(p)
                else:
                    print("Invalid choice")
            
            elif choice == "4":
                inventory.save_inventory()
                print("Inventory saved!")
            
            elif choice == "5":
                inventory.load_inventory()
                print("Inventory loaded!")
            
            elif choice == "6":
                inventory.remove_expired_products()
                print("Expired products removed!")
            
            elif choice == "7":
                value = inventory.total_inventory_value()
                print(f"Total inventory value: ${value:.2f}")
            
            elif choice == "8":
                break
            
            else:
                print("Invalid choice")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    cli_menu()