import streamlit as st
from inventory_management_system import Inventory, Sales, ElectronicProduct, ClothingProduct, GroceryProduct
import pandas as pd
from datetime import date

# Initialize session state for inventory and sales
if 'inventory' not in st.session_state:
    st.session_state.inventory = Inventory()
    st.session_state.sales = Sales(st.session_state.inventory)

# Streamlit app
st.title("Inventory Management System")

# Sidebar for navigation
page = st.sidebar.selectbox("Select Page", ["Add Product", "Manage Inventory", "Process Sale", "View Sales History", "Inventory Summary"])

if page == "Add Product":
    st.header("Add New Product")
    product_type = st.selectbox("Product Type", ["Electronic", "Clothing", "Grocery"])
    
    with st.form("add_product_form"):
        product_id = st.text_input("Product ID")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.01, step=0.01)
        quantity = st.number_input("Quantity", min_value=0, step=1)
        
        if product_type == "Electronic":
            warranty_years = st.number_input("Warranty (Years)", min_value=0, step=1)
            brand = st.text_input("Brand")
        elif product_type == "Clothing":
            size = st.selectbox("Size", ["S", "M", "L", "XL"])
            material = st.text_input("Material")
        else:  # Grocery
            expiry_date = st.date_input("Expiry Date", min_value=date.today())
        
        submit = st.form_submit_button("Add Product")
        
        if submit:
            try:
                if product_type == "Electronic":
                    product = ElectronicProduct(product_id, name, price, quantity, warranty_years, brand)
                elif product_type == "Clothing":
                    product = ClothingProduct(product_id, name, price, quantity, size, material)
                else:
                    product = GroceryProduct(product_id, name, price, quantity, expiry_date.isoformat())
                st.session_state.inventory.add_product(product)
                st.success(f"Added {name} to inventory!")
            except Exception as e:
                st.error(str(e))

elif page == "Manage Inventory":
    st.header("Manage Inventory")
    
    # Display inventory
    products = st.session_state.inventory.list_all_products()
    if products:
        df = pd.DataFrame(products)
        st.dataframe(df)
        
        # Update or remove product
        st.subheader("Update or Remove Product")
        product_id = st.selectbox("Select Product ID", [p['product_id'] for p in products])
        
        with st.form("manage_product_form"):
            new_quantity = st.number_input("New Quantity", min_value=0, step=1)
            update = st.form_submit_button("Update Stock")
            remove = st.form_submit_button("Remove Product")
            
            if update:
                try:
                    st.session_state.inventory.restock_product(product_id, new_quantity - st.session_state.inventory.get_product(product_id).quantity)
                    st.success(f"Updated stock for {product_id}")
                except Exception as e:
                    st.error(str(e))
            
            if remove:
                try:
                    st.session_state.inventory.remove_product(product_id)
                    st.success(f"Removed product {product_id}")
                except Exception as e:
                    st.error(str(e))
    else:
        st.info("No products in inventory.")

elif page == "Process Sale":
    st.header("Process Sale")
    
    products = st.session_state.inventory.list_all_products()
    if products:
        product_id = st.selectbox("Select Product ID", [p['product_id'] for p in products])
        quantity = st.number_input("Quantity", min_value=1, step=1)
        
        if st.button("Process Sale"):
            try:
                total = st.session_state.sales.process_sale(product_id, quantity)
                st.success(f"Sale processed! Total: ${total:.2f}")
            except Exception as e:
                st.error(str(e))
    else:
        st.info("No products available for sale.")

elif page == "View Sales History":
    st.header("Sales History")
    
    sales = st.session_state.sales.get_sales_history()
    if sales:
        df = pd.DataFrame(sales)
        st.dataframe(df)
    else:
        st.info("No sales recorded.")

elif page == "Inventory Summary":
    st.header("Inventory Summary")
    
    # Total inventory value
    total_value = st.session_state.inventory.total_inventory_value()
    st.write(f"**Total Inventory Value**: ${total_value:.2f}")
    
    # Remove expired products
    if st.button("Remove Expired Products"):
        try:
            st.session_state.inventory.remove_expired_products()
            st.success("Expired products removed!")
        except Exception as e:
            st.error(str(e))
    
    # Search by name
    st.subheader("Search by Name")
    search_name = st.text_input("Enter product name")
    if search_name:
        results = st.session_state.inventory.search_by_name(search_name)
        if results:
            df = pd.DataFrame([p.get_details() for p in results])
            st.dataframe(df)
        else:
            st.info("No products found.")
    
    # Search by type
    st.subheader("Search by Type")
    product_type = st.selectbox("Select Product Type", ["ElectronicProduct", "ClothingProduct", "GroceryProduct"])
    if st.button("Search"):
        results = st.session_state.inventory.search_by_type(product_type)
        if results:
            df = pd.DataFrame([p.get_details() for p in results])
            st.dataframe(df)
        else:
            st.info("No products found.")