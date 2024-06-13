from tkinter import *
import tkinter.messagebox
from functools import partial
import json
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox

from customtkinter import CTkComboBox
from matplotlib.figure import Figure
import pandas as pd
import sqlite3
import matplotlib.patheffects as pe
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Toplevel, Canvas, Entry, Button, PhotoImage, messagebox
import tkinter
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, date
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from functools import partial
from tkinter import messagebox

OUTPUT_PATH = Path(__file__).parent
#replace this path to your folder path
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Projects\Python\Cymbelyn_Pharmacy_Sales_Monitoring_System\assets\frame0")


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width - width) / 2)
    y_coordinate = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


import matplotlib.pyplot as plt


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width - width) / 2)
    y_coordinate = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def report_gen_annual():
    # Connect to the SQLite database
    conn = sqlite3.connect('data/transactions.db')
    cursor = conn.cursor()

    # Fetch data from the transactions table
    cursor.execute('''
        SELECT strftime('%Y', transaction_date) AS year, SUM(amount) AS total_sales
        FROM transactions
        GROUP BY year
    ''')
    annual_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    if not annual_data:
        print("No data available for the annual report.")
        return

    # Unpack the fetched data
    years, total_sales = zip(*annual_data)

    # Adding some design elements
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size

    # Example gradient background
    ax.imshow([[0, 0], [1, 1]], cmap='Blues', interpolation='bicubic', aspect='auto',
              extent=ax.get_xlim() + ax.get_ylim(), alpha=0.1)

    # Fill the area under the line plot with a translucent blue color
    ax.fill_between(years, total_sales, color='skyblue', alpha=0.3)

    # Plotting the line with shadow effect
    ax.plot(years, total_sales, marker='o', color='navy', linestyle='-', linewidth=2, markersize=8,
            label='Total Sales', path_effects=[pe.withStroke(linewidth=5, foreground='w')])

    # Data labels
    for i, txt in enumerate(total_sales):
        ax.annotate(f'{txt:.2f}', (years[i], total_sales[i]), textcoords="offset points", xytext=(0, 10), ha='center')

    ax.set_title("ANNUAL SALES REPORT", fontsize=16, fontweight='bold', color='navy', fontname='Arial')  # Title styling
    ax.set_ylabel("Sales in pesos", fontsize=12, fontweight='bold', color='darkgreen',
                  fontname='Arial')  # Y-axis label styling
    ax.set_xlabel("Years", fontsize=12, fontweight='bold', color='darkgreen', fontname='Arial')  # X-axis label styling

    ax.grid(True, linestyle='--', alpha=0.7)  # Add grid lines
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45, ha='right')  # Rotate x-axis labels for better readability

    # Add legend for better clarity
    ax.legend()

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Annual Sales Report")

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Center the window
    center_window(root, 1000, 600)

    # Start the Tkinter main loop
    root.mainloop()


def report_gen_monthly():
    monthly_report_window_toplevel = Toplevel()
    monthly_report_window_toplevel.geometry("1000x550")
    monthly_report_window_toplevel.configure(bg="#FFFFFF")
    center_window(monthly_report_window_toplevel, 1000, 550)

    monthly_report_canvas = Canvas(
        monthly_report_window_toplevel,
        bg="#FFFEFE",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    monthly_report_canvas.place(x=0, y=0)

    def check_year():
        # Get the selected value from the ComboBox
        year_input = yearCombo.get()

        # Validate the entered year
        if year_input == "Enter year":
            messagebox.showerror("Monthly Sales Report", "Please select a valid year.")
            return

        if not year_input.isdigit() or len(year_input) != 4:
            messagebox.showerror("Monthly Sales Report", "Invalid year entered. Please enter a valid 4-digit year.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect('data/transactions.db')
        cursor = conn.cursor()

        # Fetch data from the transactions table for the entered year
        cursor.execute('''
            SELECT strftime('%Y-%m', transaction_date) AS month_year, SUM(amount) AS total_sales
            FROM transactions
            WHERE strftime('%Y', transaction_date) = ?
            GROUP BY month_year
        ''', (year_input,))

        monthly_data = cursor.fetchall()

        # Close the database connection
        conn.close()

        if not monthly_data:
            messagebox.showinfo("Monthly Sales Report", f"No data available for the year {year_input}.")
            return

        # Unpack the fetched data
        months, total_sales = zip(*monthly_data)

        month_names = [datetime.strptime(month, "%Y-%m").strftime("%B") for month in months]

        # Create a new canvas for embedding the updated plot
        new_canvas = FigureCanvasTkAgg(plt.figure(figsize=(10, 6)), master=monthly_report_window_toplevel)
        new_canvas.get_tk_widget().pack()

        # Adding design elements
        ax = new_canvas.figure.add_subplot(111)

        # Example gradient background
        ax.imshow([[0, 0], [1, 1]], cmap='Blues', interpolation='bicubic', aspect='auto',
                  extent=ax.get_xlim() + ax.get_ylim(), alpha=0.1)

        # Fill the area under the line plot with a translucent blue color
        ax.fill_between(months, total_sales, color='skyblue', alpha=0.3)

        # Plotting the line with shadow effect
        ax.plot(months, total_sales, marker='o', color='navy', linestyle='-', linewidth=2, markersize=8,
                label='Total Sales', path_effects=[pe.withStroke(linewidth=5, foreground='w')])

        # Data labels
        for i, txt in enumerate(total_sales):
            ax.annotate(f'{txt:.2f}', (months[i], total_sales[i]), textcoords="offset points", xytext=(0, 10),
                        ha='center')

        ax.set_title(f"MONTHLY SALES REPORT FOR {year_input}", fontsize=16, fontweight='bold', color='navy')
        ax.set_ylabel("Sales in pesos", fontsize=12, fontweight='bold', color='darkgreen')
        ax.set_xlabel("Months", fontsize=12, fontweight='bold', color='darkgreen')

        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xticks(months)
        ax.set_xticklabels(month_names, rotation=45, ha='right')

        plt.tight_layout()
        new_canvas.draw()

    dashboard_pharma_img = PhotoImage(
        file=relative_to_assets("dashboard_pharma_img.png"))
    img_dashboard_pharma = monthly_report_canvas.create_image(
        96.0,
        274.0,
        image=dashboard_pharma_img
    )
    brand_txt_img = PhotoImage(
        file=relative_to_assets("brand_txt_img.png"))
    image_4 = monthly_report_canvas.create_image(
        524.0,
        46.0,
        image=brand_txt_img
    )
    month_rp_side_txt = PhotoImage(
        file=relative_to_assets("month_rp_side_txt.png"))
    image_5 = monthly_report_canvas.create_image(
        954.0,
        175.0,
        image=month_rp_side_txt
    )
    month_rp_bg = PhotoImage(
        file=relative_to_assets("month_rp_bg.png"))
    image_2 = monthly_report_canvas.create_image(
        599.0,
        274.0,
        image=month_rp_bg
    )
    monthly_rp_icon = PhotoImage(
        file=relative_to_assets("monthly_rp_icon.png"))
    image_3 = monthly_report_canvas.create_image(
        841.0,
        400.0,
        image=monthly_rp_icon
    )
    monthly_report_canvas.create_text(
        452.0,
        125.0,
        anchor="nw",
        text="Enter year to see its\nmonthly sales report",
        fill="#FFFFFF",
        font=("Lato SemiBold", 32 * -1)
    )
    year = tkinter.StringVar()
    # monthly_rp_txt_box = PhotoImage(
    #     file=relative_to_assets("monthly_rp_txt_box.png"))
    # entry_bg_1 = monthly_report_canvas.create_image(
    #     598.5,
    #     253.0,
    #     image=monthly_rp_txt_box
    # )
    # yearEntry = Entry(
    #     monthly_report_canvas,
    #     bd=0,
    #     bg="#D9D9D9",
    #     fg="#000716",
    #     highlightthickness=0,
    #     textvariable=year,
    #     font=("Inter", 17),
    #     justify="center"
    # )
    # yearEntry.place(
    #     x=440.0,
    #     y=231.0,
    #     width=317.0,
    #     height=42.0
    # )

    yearCombo = CTkComboBox(
        master=monthly_report_window_toplevel,
        width=317,
        height=42,
        values=["Enter year", "2023", "2022", "2021", "2020", "2019",
                "2018", "2017", "2016", "2015", "2014", "2013", "2012",
                "2011", "2010"],
        button_color="#2A8C55",
        border_color="#2A8C55",
        border_width=2,
        button_hover_color="#207244",
        dropdown_hover_color="#207244",
        dropdown_fg_color="#2A8C55",
        dropdown_text_color="#fff",
        font=("Inter", 17)
    )
    yearCombo.configure(
        values=["2023", "2022", "2021", "2020", "2019",
                "2018", "2017", "2016", "2015", "2014", "2013",
                "2012", "2011", "2010"],
        text_color="black"
    )
    yearCombo.place(
        x=440.0,
        y=231.0,
    )

    # check_year = partial(check_year, year)
    monthly_rp_btn = PhotoImage(
        file=relative_to_assets("monthly_rp_btn.png"))
    monthlyReportLoginButton = Button(
        monthly_report_canvas,
        image=monthly_rp_btn,
        borderwidth=0,
        highlightthickness=0,
        command=check_year,
        relief="flat"
    )
    monthlyReportLoginButton.place(
        x=480.0,
        y=366.0,
        width=219.0,
        height=44.0
    )
    monthly_report_window_toplevel.resizable(False, False)
    monthly_report_window_toplevel.mainloop()


# report_gen_monthly()


def report_gen_daily():  # function to generate daily report of given month in given year
    daily_report_window = Toplevel()
    daily_report_window.geometry("1000x550")
    daily_report_window.configure(bg="#FFFEFE")
    center_window(daily_report_window, 1000, 550)

    daily_report_canvas = Canvas(
        daily_report_window,
        bg="#FFFEFE",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    daily_report_canvas.place(x=0, y=0)
    daily_rp_bg = PhotoImage(
        file=relative_to_assets("daily_rp_bg.png"))
    image_1 = daily_report_canvas.create_image(
        530.0,
        274.0,
        image=daily_rp_bg
    )
    daily_rp_icon = PhotoImage(
        file=relative_to_assets("daily_rp_icon.png"))
    image_2 = daily_report_canvas.create_image(
        818.0,
        394.0,
        image=daily_rp_icon
    )
    daily_txt_img = PhotoImage(
        file=relative_to_assets("daily_txt_img.png"))
    image_3 = daily_report_canvas.create_image(
        956.0,
        156.0,
        image=daily_txt_img
    )
    dashboard_pharma_img = PhotoImage(
        file=relative_to_assets("dashboard_pharma_img.png"))
    img_dashboard_pharma = daily_report_canvas.create_image(
        96.0,
        274.0,
        image=dashboard_pharma_img
    )
    brand_txt_img = PhotoImage(
        file=relative_to_assets("brand_txt_img.png"))
    image_4 = daily_report_canvas.create_image(
        524.0,
        46.0,
        image=brand_txt_img
    )

    def check_year_and_month(year_combo, month_combo):
        year_input = year_combo.get()
        month_input = month_combo.get()

        invalid_year = False
        for i in year_input:
            if not i.isdigit():
                invalid_year = True

        if not invalid_year and len(year_input) == 4 and date.today().year >= int(year_input) > 2014:
            conn = sqlite3.connect('data/transactions.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT strftime('%d', transaction_date) AS day, SUM(amount) AS total_sales
                FROM transactions
                WHERE strftime('%Y', transaction_date) = ? AND strftime('%m', transaction_date) = ?
                GROUP BY day
            ''', (year_input, month_input.zfill(2)))

            daily_data = cursor.fetchall()
            conn.close()

            from tkinter import messagebox

            if not daily_data:
                messagebox.showinfo("Daily Sales Report", f"No data available for {month_input} {year_input}.")
                return

            dates, total_sales = zip(*daily_data)

            # Matplotlib plot design
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow([[0, 0], [1, 1]], cmap='Blues', interpolation='bicubic', aspect='auto',
                      extent=ax.get_xlim() + ax.get_ylim(), alpha=0.1)
            ax.fill_between(dates, total_sales, color='skyblue', alpha=0.3)
            ax.plot(dates, total_sales, marker='o', color='navy', linestyle='-', linewidth=2, markersize=8,
                    label='Total Sales', path_effects=[pe.withStroke(linewidth=5, foreground='w')])

            for i, txt in enumerate(total_sales):
                ax.annotate(f'{txt:.2f}', (dates[i], total_sales[i]), textcoords="offset points", xytext=(0, 10),
                            ha='center')

            ax.set_title(f"DAILY SALES REPORT FOR {month_input.upper()} of {year_input}", fontsize=16,
                         fontweight='bold',
                         color='navy')
            ax.set_ylabel("Sales in pesos", fontsize=12, fontweight='bold', color='darkgreen')
            ax.set_xlabel("Days", fontsize=12, fontweight='bold', color='darkgreen')

            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_xticks(dates)
            ax.set_xticklabels(dates, rotation=45, ha='right')

            plt.tight_layout()
            plt.show()
        else:
            from tkinter import messagebox
            messagebox.showerror("DAILY REPORT INPUT ERROR", "Invalid year entered")
            return

    daily_report_canvas.create_text(
        553.0,
        145.0,
        anchor="nw",
        text="Year",
        fill="#FFFFFF",
        font=("Lato SemiBold", 32 * -1)
    )
    year = tkinter.StringVar()
    yearCombo = CTkComboBox(
        master=daily_report_window,
        width=205,
        height=40,
        values=["Enter year", "2023", "2022", "2021", "2020", "2019",
                "2018", "2017", "2016", "2015", "2014", "2013", "2012",
                "2011", "2010"],
        button_color="#2A8C55",
        border_color="#2A8C55",
        border_width=2,
        button_hover_color="#207244",
        dropdown_hover_color="#207244",
        dropdown_fg_color="#2A8C55",
        dropdown_text_color="#fff",
        font=("Inter", 17)
    )
    yearCombo.configure(
        values=["2023", "2022", "2021", "2020", "2019",
                "2018", "2017", "2016", "2015", "2014", "2013",
                "2012", "2011", "2010"],
        text_color="black"
    )
    yearCombo.place(
        x=558.0,
        y=193.0,
    )

    daily_report_canvas.create_text(
        302.0,
        145.0,
        anchor="nw",
        text="Month",
        fill="#FFFFFF",
        font=("Lato SemiBold", 32 * -1)
    )
    month = tkinter.StringVar()
    monthCombo = CTkComboBox(
        master=daily_report_window,
        width=205,
        height=40,
        values=["Enter month", "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10", "11", "12"],
        button_color="#2A8C55",
        border_color="#2A8C55",
        border_width=2,
        button_hover_color="#207244",
        dropdown_hover_color="#207244",
        dropdown_fg_color="#2A8C55",
        dropdown_text_color="#fff",
        font=("Inter", 17)
    )
    monthCombo.configure(
        values=["1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10", "11", "12"],
        text_color="black"
    )
    monthCombo.place(
        x=307.0,
        y=193.0,
    )

    # monthEntry = CTkComboBox(
    #     master=daily_report_window,
    #     width=205,
    #     height=40,
    #     values=["Enter year", "2023", "2022", "2021", "2020", "2019",
    #             "2018", "2017", "2016", "2015", "2014", "2013", "2012",
    #             "2011", "2010"],
    #     button_color="#2A8C55",
    #     border_color="#2A8C55",
    #     border_width=2,
    #     button_hover_color="#207244",
    #     dropdown_hover_color="#207244",
    #     dropdown_fg_color="#2A8C55",
    #     dropdown_text_color="#fff",
    #     font=("Inter", 17)
    # )
    # monthEntry.configure(
    #     values=["1", "2", "3", "4", "5",
    #             "6", "7", "8", "9", "10", "11",
    #             "12"],
    #     text_color="black"
    # )
    # monthEntry.place(
    #     x=307.0,
    #     y=193.0,
    # )


    daily_rp_btn = PhotoImage(
        file=relative_to_assets("daily_rp_btn.png"))
    check_year_and_month_button = Button(
        daily_report_canvas,
        image=daily_rp_btn,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: check_year_and_month(yearCombo, monthCombo),
        relief="flat"
    )
    check_year_and_month_button.place(
        x=420.0,
        y=366.0,
        width=219.0,
        height=44.0
    )
    daily_report_window.resizable(False, False)
    center_window(daily_report_window, 1000, 550)
    daily_report_window.mainloop()
# report_gen_daily()
