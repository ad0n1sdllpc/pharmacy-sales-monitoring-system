from tkinter import *
import json
import sqlite3
from datetime import datetime, date
from tkinter import messagebox
from functools import partial
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path
from turtle import bgcolor
from fpdf import FPDF
import tkinter as tk
import win32print

order = {}
total = 0

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Projects\Python\Cymbelyn_Pharmacy_Sales_Monitoring_System\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width - width) / 2)
    y_coordinate = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

def print_receipt_on_thermal(name, contactno, order, medicine_stock, total):
    # Create a window for the receipt
    receipt_window = tk.Toplevel()
    receipt_window.title('Receipt')

    # Add "Cymbelyn Pharmacy" at the top
    tk.Label(receipt_window, text="Cymbelyn Pharmacy", font=('Arial', 16, 'bold')).pack()

    # Add customer details
    customer_details = f"\nCustomer Name: {name}\nCustomer No: {contactno}\n"
    tk.Label(receipt_window, text=customer_details).pack()

    # Add table headers
    headings = ["MEDICINE NAME", "QUANTITY", "COST PER UNIT", "AMOUNT"]
    header_text = "{:<20} {:<10} {:<15} {:<15}".format(*headings)
    tk.Label(receipt_window, text=header_text, font=('Arial', 12, 'bold')).pack()

    # Add table data
    for medicine_id, quantity in order.items():
        medicine_data = [
            medicine_stock[medicine_id]["name"],
            str(quantity),
            str(medicine_stock[medicine_id]["cost"]),
            str(quantity * medicine_stock[medicine_id]["cost"])
        ]
        row_text = "{:<20} {:<10} {:<15} {:<15}".format(*medicine_data)
        tk.Label(receipt_window, text=row_text).pack()

    # Add total
    total_text = f"\nTotal = {total}"
    tk.Label(receipt_window, text=total_text, font=('Arial', 12, 'bold')).pack()

    # Print the receipt on the thermal printer
    printer_name = win32print.GetDefaultPrinter()
    text_to_print = "Cymbelyn Pharmacy\n" + customer_details + header_text + "\n"
    for medicine_id, quantity in order.items():
        medicine_data = [
            medicine_stock[medicine_id]["name"],
            str(quantity),
            str(medicine_stock[medicine_id]["cost"]),
            str(quantity * medicine_stock[medicine_id]["cost"])
        ]
        row_text = "{:<20} {:<10} {:<15} {:<15}".format(*medicine_data)
        text_to_print += row_text + "\n"
    text_to_print += total_text + "\n"

    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        hdc = win32print.CreateDC("WINSPOOL", printer_name, 0, {})
        win32print.StartDoc(hdc, {"Title": "Receipt"})
        win32print.StartPage(hdc)
        win32print.WritePrinter(hPrinter, text_to_print.encode('utf-8'))
        win32print.EndPage(hdc)
        win32print.EndDoc(hdc)
        win32print.ClosePrinter(hPrinter)
        receipt_window.destroy()  # Close the receipt window after printing
    except Exception as e:
        print(f"Error printing receipt: {e}")
        tk.messagebox.showerror("Print Error", "Error printing receipt. Check printer connection.")


def print_receipt(name, contactno, order, medicine_stock, total):
    pdf = FPDF()
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Add customer details
    pdf.cell(200, 10, txt=f"Customer Name: {name}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Contact No: {contactno}", ln=True, align='L')

    # Add table headers
    headings = ["MEDICINE NAME", "QUANTITY", "COST PER UNIT", "AMOUNT"]
    pdf.set_fill_color(255, 165, 0)
    for heading in headings:
        pdf.cell(50, 10, txt=heading, border=1, fill=True)

    pdf.ln()

    # Add table data
    for medicine_id, quantity in order.items():
        pdf.cell(50, 10, txt=medicine_stock[medicine_id]["name"], border=1)
        pdf.cell(50, 10, txt=str(quantity), border=1)
        pdf.cell(50, 10, txt=str(medicine_stock[medicine_id]["cost"]), border=1)
        pdf.cell(50, 10, txt=str(quantity * medicine_stock[medicine_id]["cost"]), border=1)
        pdf.ln()

    # Add total
    pdf.cell(150, 10, txt=f"Total = {total}", border=1, fill=True)

    # Save the PDF
    pdf.output("receipt.pdf")

    # Open the PDF file
    import os
    os.system("start receipt.pdf")  # Open the PDF file using the default PDF viewer

def display_stock(order_canvas):
    with open(r"data\medicine_stock.json", "r") as read_it:
        medicine_stock = json.load(read_it)

    class Table:
        def __init__(self, root):
            self.create_table(root)

        def create_table(self, root):
            total_rows = len(medicine_stock)
            total_columns = 6
            table_columns = ["MEDICINE ID", "MEDICINE NAME", "QUANTITY", "BIN NUMBER", "EXPIRY DATE", "COST"]

            # Creating Treeview
            self.table = ttk.Treeview(master=root, columns=table_columns, show="headings")

            for column in table_columns:
                self.table.heading(column=column, text=column, anchor='center')
                self.table.column(column=column, width=120, anchor='center')  # Adjust the width as needed

            # Sort the rows alphabetically based on "MEDICINE NAME" column
            sorted_data = sorted(medicine_stock.items(), key=lambda x: x[1]["name"])

            for product_id, details in sorted_data:
                row_data = [product_id, details["name"], details["quantity"], details["bin no"], details["expiry date"],
                            details["cost"]]
                self.table.insert(parent="", index="end", values=row_data, tags=('oddrow',))

            # Applying styles to Treeview
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview", background="light green", fieldbackground="light green", foreground="#288652")
            style.configure("Treeview.Heading", background="#288652", fieldbackground="#288652", foreground="white")
            style.map("Treeview", background=[("selected", "#288652")])
            style.configure("Treeview.oddrow", background="lightgray")  # Set background color for odd rows
            # Set background color for odd rows

            self.table.tag_configure('oddrow', background='lightgray')

            self.table.pack(fill='both', expand=True)  # Pack the table to fill the available space

    # Create a frame on order_canvas to hold the table
    table_frame = Frame(order_canvas, bg="#FFFEFE", bd=0, highlightthickness=0, relief="ridge")
    table_frame.place(x=244.0, y=113.0, width=958.0 - 244.0, height=329.0 - 113.0)

    t = Table(table_frame)


def Billing():
    order_window = Toplevel()
    order_window.geometry("1000x550")
    order_window.configure(bg="#FFFEFE")
    center_window(order_window, 1000, 550)



    order_canvas = Canvas(
        order_window,
        bg="#FFFEFE",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    order_canvas.place(x=0, y=0)

    bg_order = PhotoImage(
        file=relative_to_assets("bg_med_qty.png"))
    image_1 = order_canvas.create_image(
        586.0,
        424.0,
        image=bg_order
    )
    dashboard_pharma_img = PhotoImage(
        file=relative_to_assets("dashboard_pharma_img.png"))
    img_dashboard_pharma = order_canvas.create_image(
        96.0,
        274.0,
        image=dashboard_pharma_img
    )

    order_canvas.create_text(
        244.0,
        71.0,
        anchor="nw",
        text="Name :",
        fill="#288652",
        font=("Inter Medium", 24 * -1)
    )
    name = StringVar()
    name_txt_box = PhotoImage(
        file=relative_to_assets("name_entry.png"))
    entry_bg_4 = order_canvas.create_image(
        448.5,
        83.0,
        image=name_txt_box
    )
    nameEntry = Entry(
        order_canvas,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        textvariable=name,
        font=("Inter", 17)
    )
    nameEntry.place(
        x=339.0,
        y=66.0,
        width=219.0,
        height=32.0
    )
    order_canvas.create_text(
        576.0,
        66.0,
        anchor="nw",
        text="Contact No :",
        fill="#288652",
        font=("Inter Medium", 24 * -1)
    )
    contactno = StringVar()
    contact_no = PhotoImage(
        file=relative_to_assets("contact_no_entry.png"))
    entry_bg_3 = order_canvas.create_image(
        843.5,
        83.0,
        image=contact_no
    )
    contactno = Entry(
        order_canvas,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        textvariable=contactno,
        font=("Inter", 17)

    )
    contactno.place(
        x=734.0,
        y=66.0,
        width=219.0,
        height=32.0
    )
    order_canvas.create_text(
        244.0,
        336.0,
        anchor="nw",
        text="Enter the order below:",
        fill="#288652",
        font=("Inter Medium", 24 * -1)
    )
    order_canvas.create_text(
        311.0,
        374.0,
        anchor="nw",
        text="Medicine ID :",
        fill="#F5F5F5",
        font=("Lato MediumItalic", 32 * -1)
    )
    medicineid = StringVar()
    order_med_id = PhotoImage(
        file=relative_to_assets("order_med_id_txtbox.png"))
    entry_bg_1 = order_canvas.create_image(
        410.0,
        441.0,
        image=order_med_id
    )
    medicineidEntry = Entry(
        order_canvas,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        textvariable=medicineid,
        font=("Inter", 17)
    )
    medicineidEntry.place(
        x=271.0,
        y=419.0,
        width=256.0,
        height=42.0
    )
    order_canvas.create_text(
        705.0,
        374.0,
        anchor="nw",
        text="Quantity :",
        fill="#F5F5F5",
        font=("Lato MediumItalic", 32 * -1)
    )
    Quantity = StringVar()
    order_quantity = PhotoImage(
        file=relative_to_assets("order_quantity_id_txtbox.png"))
    entry_bg_2 = order_canvas.create_image(
        758.0,
        441.0,
        image=order_quantity
    )
    quantityEntry = Entry(
        order_canvas,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        justify="center",
        textvariable=Quantity,
        font=("Inter", 17)
    )
    quantityEntry.place(
        x=645.0,
        y=419.0,
        width=256.0,
        height=42.0
    )

    def reset(txt):
        quantityEntry.delete(0, END)
        quantityEntry.insert(0, txt)
        medicineidEntry.delete(0, END)
        medicineidEntry.insert(0, txt)

    def next(medicineid, Quantity):
        medicine_id = medicineid.get()
        quantity = Quantity.get()
        reset("")
        global order
        global total
        import datetime
        with open(r"data\\medicine_stock.json", "r") as read_it:
            medicine_stock = json.load(read_it)
        if medicine_id not in medicine_stock:
            messagebox.showerror("CYMBELYN PHARMACY BILLING ERROR", "INVALID MEDICINE ID")
        else:
            if quantity.isdigit():
                if medicine_stock[medicine_id]["quantity"] >= int(quantity):
                    expiry_date_list = medicine_stock[medicine_id]["expiry date"].split("-")
                    expiry_date = datetime.datetime(int(expiry_date_list[0]), int(expiry_date_list[1]),
                                                    int(expiry_date_list[2]))
                    current_time = datetime.datetime.now()
                    today = datetime.datetime(
                        current_time.year, current_time.month, current_time.day)
                    if today < expiry_date:
                        if medicine_id not in order:
                            order[medicine_id] = int(quantity)
                        else:
                            order[medicine_id] += int(quantity)
                        total += medicine_stock[medicine_id]["cost"] * int(quantity)
                        medicine_stock[medicine_id]["quantity"] -= int(quantity)
                        with open(r"data\\medicine_stock.json", "w") as p:
                            json.dump(medicine_stock, p)
                        bin_no = medicine_stock[medicine_id]["bin no"]
                        messagebox.showinfo("CYMBELYN PHARMACY BILLING ERROR", f"Medicine available in {bin_no} bin no")
                    else:
                        messagebox.showerror("CYMBELYN PHARMACY BILLING ERROR",
                                             "Medicine unavailable")
                else:
                    temp = medicine_stock[medicine_id]["quantity"]
                    messagebox.showerror("CYMBELYN PHARMACY BILLING ERROR",
                                         f"Not enough stock available!\nOnly {temp} stock available")

    Next = partial(next, medicineid, Quantity)
    button_image_2 = PhotoImage(
        file=relative_to_assets("total_btn.png"))
    nextButton = Button(
        order_canvas,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=Next,
        relief="flat"
    )
    nextButton.place(
        x=236.0,
        y=492.0,
        width=327.0,
        height=44.0
    )

    def total_billing(medicineid, Quantity):

        next(medicineid, Quantity)
        with open(r"data\\medicine_stock.json", "r") as read_it:
            medicine_stock = json.load(read_it)
        global total
        with open(r"data\\report_data.json", "r") as f:
            dates = json.load(f)
        from datetime import date
        today = date.today()
        if total != 0:
            if str(today) not in dates:
                dates[str(today)] = str(total)
            else:
                dates[str(today)] += str(total)
            with open(r"data\\report_data.json", "w") as f:
                json.dump(dates, f)
            headings = ["MEDICINE NAME", "QUANTITY", "COST PER UNIT", "AMOUNT"]
            row_headings = ["name", "quantity", "cost", "amount"]

            class Table:
                def __init__(self, root):
                    self.e = Entry(root, width=25, justify="left", fg='black', font=('Arial', 12, 'bold'))
                    self.e.grid(row=0, column=0)
                    self.e.insert(END, f"Customer Name:{name.get()}")
                    self.e = Entry(root, width=25, justify="left", fg='black', font=('Arial', 12, 'bold'))
                    self.e.grid(row=0, column=3)
                    self.e.insert(END, f"Customer No:{contactno.get()}")
                    for j in range(0, total_columns):
                        self.e = Entry(root, width=20, justify="center", fg='black',
                                       bg='darkorange', font=('Arial', 12, 'bold'))
                        self.e.grid(row=2, column=j)
                        self.e.insert(END, headings[j])
                    for index, i in enumerate(order):
                        for j in range(0, total_columns):
                            self.e = Entry(root, width=17, justify="center",
                                           fg='black', bg='tan', font=('Arial', 16, 'bold'))
                            self.e.grid(row=index + 3, column=j)
                            if j == 3:
                                self.e.insert(END, str(medicine_stock[i]["cost"] * order[i]))
                            elif j == 1:
                                self.e.insert(END, order[i])
                            else:
                                self.e.insert(END, str(medicine_stock[i][row_headings[j]]))
                    self.e = Entry(root, width=17, justify="center",
                                   fg='white', bg='red', font=('Arial', 16, 'bold'))
                    self.e.grid(row=total_rows + 3, column=3)
                    self.e.insert(END, f"Total ={total}")

                    confirmation = messagebox.askquestion("Print Receipt", "Do you want to print the receipt?")
                    if confirmation == 'yes':
                        # Call the print_receipt_on_thermal function
                        print_receipt_on_thermal(name.get(), contactno.get(), order, medicine_stock, total)
                    # confirmation = messagebox.askquestion("Print Receipt", "Do you want to print the receipt?")
                    # if confirmation == 'yes':
                    #     # Call the print_receipt function
                    #     print_receipt(name.get(), contactno.get(), order, medicine_stock, total)

            # Connect to the SQLite database
            conn = sqlite3.connect('data/transactions.db')
            cursor = conn.cursor()

            # Get the current date and time
            now = datetime.now()
            transaction_date = now.strftime("%Y-%m-%d %H:%M")

            for medicine_id, quantity in order.items():
                # Calculate the amount
                amount = quantity * medicine_stock[medicine_id]["cost"]

                # Insert the transaction details into the database
                cursor.execute('''
                        INSERT INTO transactions (medicine_id, medicine_name, quantity, amount, transaction_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (medicine_id, medicine_stock[medicine_id]["name"], quantity, amount, transaction_date))

                # Commit the changes and close the connection
            conn.commit()
            conn.close()


            total_rows = len(order)
            total_columns = 4

            root = Toplevel(order_window)
            root.title('CYMBELYN PHARMACY BILL')
            t = Table(root)
            root.mainloop()
        else:
            messagebox.showinfo("Billing", "No items added for billing")

    Total = partial(total_billing, medicineid, Quantity)
    button_image_1 = PhotoImage(
        file=relative_to_assets("order_view_btn.png"))
    totalButton = Button(
        order_canvas,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=Total,
        relief="flat"
    )
    totalButton.place(
        x=609.0,
        y=492.0,
        width=327.0,
        height=44.0
    )
    order_canvas.create_text(
        336.0,
        1.0,
        anchor="nw",
        text="CYMBELYN  PHARMACY",
        fill="#288652",
        font=("Poppins Bold", 48 * -1)
    )
    order_canvas.create_rectangle(
        244.0,
        113.0,
        958.0,
        329.0,
        fill="#288652",
        outline="")

    display_stock(order_canvas)

    order_window.resizable(False, False)
    order_window.mainloop()

# Billing()
