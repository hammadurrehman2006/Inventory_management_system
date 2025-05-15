
# Inventory Management System

## Overview

I developed this **Inventory Management System** as part of an Advanced OOP Challenge to demonstrate my Object-Oriented Programming skills. This Python application manages inventory for Electronics, Clothing, and Grocery products with:

- **Command-Line Interface (CLI)**: Traditional terminal-based operations
- **Streamlit Web Interface**: Modern browser-based management

## Key Features

### Product Management
```python
class ElectronicProduct(Product):
    def __init__(self, product_id, name, price, quantity, warranty_years, brand):
        super().__init__(product_id, name, price, quantity)
        self.warranty_years = warranty_years
        self.brand = brand
```

### Core Functionality
- ✅ Add/remove products  
- ✅ Restock inventory  
- ✅ Process sales with auto-stock updates  
- ✅ Search and filter products  
- ✅ Automatic JSON data persistence  
- ✅ Detailed operation logging  

## Installation

```bash
git clone https://github.com/hammadurrehman2006/Inventory_management_system.git
cd Inventory_management_system
pip install -r requirements.txt
```

## How to Use

**CLI Version**:
```bash
python inventory_management_system.py
```

**Web Interface**:
```bash
streamlit run app.py
```

## Project Structure

| File                          | Description                          |
|-------------------------------|--------------------------------------|
| `inventory_management_system.py` | Core logic and CLI implementation |
| `app.py`                      | Streamlit web interface             |
| `inventory.json`              | Product data storage                |
| `sales.json`                  | Transaction records                 |

## Why I Built This

As an Electronics Engineering student passionate about software development, I wanted to:
- Showcase my OOP implementation skills
- Demonstrate complete system design ability
- Create a foundation for future enhancements

## Technologies Used

- Python 3 (OOP implementation)
- Streamlit (Web UI)
- JSON (Data storage)
- Logging (Operation tracking)

## About Me

I'm Muhammad Hammad ur Rehman, an Electronics Engineering student at NED University with interests in:

- Software architecture
- Full-stack development
- Embedded systems
- AI/ML applications

[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=flat&logo=github)](https://github.com/hammadurrehman2006)
