# Inventory Management System

## Overview

The **Inventory Management System** is a Python-based application crafted by **Muhammad Hammad ur Rehman**, an electronics engineering student at NED University with a passion for innovative software solutions. Built for an Advanced OOP Challenge, this project demonstrates robust Object-Oriented Programming (OOP) principles—encapsulation, inheritance, polymorphism, and abstraction. It efficiently manages Electronics, Clothing, and Grocery products through two interfaces:

- **Command-Line Interface (CLI)**: A user-friendly menu for adding, selling, searching, and managing inventory.
- **Streamlit Web Interface**: A dynamic, browser-based UI for interactive operations.

Data persists in JSON files (`inventory.json` for products, `sales.json` for sales), with operations logged to `inventory.log` for transparency. Custom exceptions ensure reliable error handling, and comprehensive documentation makes the project accessible. Explore it on GitHub: [https://github.com/hammadurrehman2006/Inventory_management_system](https://github.com/hammadurrehman2006/Inventory_management_system). Completed on May 15, 2025, this system reflects Hammad’s drive to blend engineering and software development.

## Features

- **Product Management**:
  - Abstract `Product` class with `product_id`, `name`, `price`, `quantity_in_stock`.
  - Subclasses:
    - `ElectronicProduct` (with `warranty_years`, `brand`)
    - `ClothingProduct` (with `size`, `material`)
    - `GroceryProduct` (with `expiry_date`, `is_expired()`)
  - Methods: `restock`, `sell`, `get_total_value`, `__str__`.

- **Inventory Management**:
  - Add, remove, restock, and list products.
  - Search by name or type.
  - Calculate total inventory value.
  - Remove expired grocery products.

- **Sales Processing**:
  - Process sales with automatic stock updates.
  - Log sales history with timestamps.
  - Persist sales data.

- **Error Handling**:
  - Custom exceptions: `DuplicateProductError`, `InsufficientStockError`, `InvalidProductDataError`.
  - Validates inputs (e.g., negative quantities, invalid dates).
  - Logs operations to `inventory.log`.

- **Interfaces**:
  - CLI menu for terminal-based control.
  - Streamlit UI with pages: Add Product, Manage Inventory, Process Sale, View Sales History, Inventory Summary (value, search, remove expired).

- **Data Persistence**:
  - Saves inventory and sales to JSON files.
  - Loads data automatically on startup.

## Requirements

- Python 3.6+
- Dependencies (listed in `requirements.txt`):
  - `streamlit`
  - `pandas`
- No external databases needed (uses JSON files).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hammadurrehman2006/Inventory_management_system.git
   cd Inventory_management_system
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Files**:
   - `inventory_management_system.py`: Core logic and CLI.
   - `app.py`: Streamlit interface.
   - `requirements.txt`: Dependencies.
   - `LICENSE`: MIT License.

## Usage

### Command-Line Interface (CLI)

1. **Run**:
   ```bash
   python inventory_management_system.py
   ```

2. **Menu Options**:
   - **1. Add Product**: Input details for Electronics, Clothing, or Grocery.
   - **2. Sell Product**: Enter product ID and quantity.
   - **3. Search/View Products**: Search by name, type, or list all.
   - **4. Save Inventory**: Save to `inventory.json`.
   - **5. Load Inventory**: Load from `inventory.json`.
   - **6. Remove Expired Products**: Clear expired Grocery items.
   - **7. Total Inventory Value**: Show total stock value.
   - **8. Exit**: Quit.

3. **Example**:
   ```
   Inventory Management System
   1. Add Product
   2. Sell Product
   3. Search/View Products
   4. Save Inventory
   5. Load Inventory
   6. Remove Expired Products
   7. Total Inventory Value
   8. Exit
   Enter choice: 1
   Product type (Electronic/Clothing/Grocery): Grocery
   Product ID: G001
   Name: Milk
   Price: 3.99
   Quantity: 20
   Expiry date (YYYY-MM-DD): 2025-06-01
   Product added!
   ```

### Streamlit Web Interface

1. **Run**:
   ```bash
   streamlit run app.py
   ```
   - Opens at `http://localhost:8501`.

2. **Pages**:
   - **Add Product**: Form for adding products with type-specific fields.
   - **Manage Inventory**: View, update, or remove products.
   - **Process Sale**: Select product and quantity to sell.
   - **View Sales History**: See all sales.
   - **Inventory Summary**: Check total value, search, or remove expired items.

3. **Example**:
   - In "Add Product", add a Grocery item: ID "G002", Name "Bread", Price 2.99, Quantity 30, Expiry 2025-05-20.
   - In "Process Sale", sell 10 units of "G002" (Total: $29.90).
   - In "Inventory Summary", search for "Bread" or view total value.

## File Structure

- `inventory_management_system.py`: Core logic, product classes, and CLI.
- `app.py`: Streamlit interface.
- `requirements.txt`: Python dependencies.
- `LICENSE`: MIT License.
- `README.md`: Documentation.
- `inventory.json`: Product data (auto-generated).
- `sales.json`: Sales history (auto-generated).
- `inventory.log`: Operation logs (auto-generated).

## Data Persistence

- **Inventory**: Saved to `inventory.json` after operations.
- **Sales**: Saved to `sales.json` after sales.
- **Loading**: Data loads automatically if files exist.

Example `inventory.json`:
```json
[
  {
    "product_id": "G001",
    "name": "Milk",
    "price": 3.99,
    "quantity": 20,
    "type": "GroceryProduct",
    "expiry_date": "2025-06-01"
  }
]
```

## Error Handling

- **Custom Exceptions**:
  - `DuplicateProductError`: Duplicate product IDs.
  - `InsufficientStockError`: Selling beyond stock.
  - `InvalidProductDataError`: Invalid file data.
- **Validation**: Blocks negative quantities, invalid dates, etc.
- **Logging**: Operations logged to `inventory.log`.

## Extensibility

- **New Product Types**: Add `Product` subclasses, update `Inventory.load_inventory` and `app.py`.
- **Database**: Replace JSON with SQLite by modifying `save_inventory`/`load_inventory`.
- **UI**: Add Streamlit charts with `matplotlib` or `plotly`.

## Development

- **OOP Principles**:
  - **Encapsulation**: Private attributes with properties.
  - **Inheritance**: Subclasses inherit from `Product`.
  - **Polymorphism**: Overridden `get_details` and `__str__`.
  - **Abstraction**: Abstract `Product` with `get_details`.
- **Documentation**: Docstrings for all classes/methods.
- **Author**: Muhammad Hammad ur Rehman.

## Troubleshooting

- **Streamlit Issues**: Verify `streamlit` installation (`pip install streamlit`) and run `streamlit run app.py`.
- **JSON Errors**: Delete corrupted `inventory.json` or `sales.json` and restart.
- **Input Errors**: CLI/Streamlit show error messages for invalid inputs.

## About the Author

**Muhammad Hammad ur Rehman** is an electronics engineering student at NED University, Karachi, with a passion for circuits, AI, and web development. Skilled in Python, React, and Next.js, Hammad built this system to showcase OOP expertise and practical software design. Connect on GitHub: [hammadurrehman2006](https://github.com/hammadurrehman2006).

## Contributing

Contributions are welcome! Fork the repository at [https://github.com/hammadurrehman2006/Inventory_management_system](https://github.com/hammadurrehman2006/Inventory_management_system) and submit pull requests.

## License

Licensed under the MIT License. See `LICENSE` for details.

## Contact

Reach out to **Muhammad Hammad ur Rehman** via GitHub: [hammadurrehman2006](https://github.com/hammadurrehman2006).

---

*Completed on May 15, 2025*