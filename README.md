# Pharmacy Sales Monitoring System

## Overview

Cymbelyn Pharmacy Sales Monitoring System is a desktop application designed to streamline the process of sales and inventory management in a pharmacy setting. The system includes features for logging in as different users (Admin and Cashier), managing medicine stocks, billing customers, printing receipts and generate reports.

## Features

- **User Authentication**: Secure login for Admin and Cashier.
- **Medicine Stock Management**: Track inventory, including quantity and expiry dates.
- **Billing System**: Generate bills for customers and print receipts.
- **Report Generation**: Daily sales reports are generated and stored.

## Installation

To run this project, you need to have Python installed. You can download Python from [here](https://www.python.org/downloads/).

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/pharmacy-sales-monitoring-system.git
    cd pharmacy-sales-monitoring-system
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. In **`billing.py`**, update the assets path to reflect the location of the project on your local machine:
    ```python
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"CHANGE THIS PATH")
    ```

## Usage

To start the application, run the `run.py` file:
```bash
python run.py
```

## File Structure

- **billing.py**: Contains the Billing class and functions to handle the billing process, including adding medicines to an order and calculating the total amount.
- **run.py**: The main file to run the application. Handles user authentication, and launches the appropriate windows for Admin and Cashier roles.
- **report_data.py**: Contains functions to generate and manage reports.
- **display_stock.py**: Manages the display of current medicine stock.
- **add_transactions_db.py**: Manages transactions and performs CRUD (Create, Read, Update, Delete) operations on the medicine inventory.

## Functions Overview

### billing.py

- **`next(medicineid, Quantity)`**: Adds medicines to the order after validating the stock and expiry date.
- **`total_billing(medicineid, Quantity)`**: Calculates the total bill for the current order and generates a report.
- **`print_receipt_on_thermal(name, contactno, order, medicine_stock, total)`**: Prints the receipt on a thermal printer.

### run.py

- **`center_window(window, width, height)`**: Centers the window on the screen.
- **`read_saved_login_details()`**: Reads saved login details from a file.
- **`validate_login(username_entry, password_entry, window)`**: Validates the login credentials and opens the appropriate window based on the user role.
- **`open_admin_window()`**: Opens the Admin window with functionalities to manage orders and view expired medicines.

### `report_data.py`

- Generates and manage reports by day, month, and year using matplotlib. 

### `display_stock.py`

- Manages the display of current medicine stock.

### `add_transactions_db.py`

- Handles adding transactions and medicine inventory to the database.

## Screenshots

(Include screenshots of the main screens of your application here)
