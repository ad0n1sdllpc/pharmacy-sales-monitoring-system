from tkinter import *
import sqlite3
from functools import partial
import tkinter.messagebox
from pathlib import Path
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width - width) / 2)
    y_coordinate = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def read_saved_login_details():
    file1 = open("data/login_details.txt", "r+")
    saved_login_details_draft = file1.read().split()
    saved_login_details = {}
    for i in range(0, len(saved_login_details_draft), 2):
        if saved_login_details_draft[i] not in saved_login_details:
            username = saved_login_details_draft[i]
            password = saved_login_details_draft[i + 1]
            saved_login_details[username] = password
    file1.close()
    return saved_login_details


def open_admin_window():
    admin_window = Toplevel()
    admin_window.geometry("1000x550")
    admin_window.configure(bg="#FFFEFE")
    center_window(admin_window, 1000, 550)

    admin_canvas = Canvas(
        admin_window,
        bg="#FFFEFE",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    admin_canvas.place(x=0, y=0)

    dashboard_button_bg = PhotoImage(
        file=relative_to_assets("dashboard_button_bg.png"))
    canvas_dashboard_button_bg = admin_canvas.create_image(
        597.0,
        300.0,
        image=dashboard_button_bg
    )

    import billing.billing as bill
    order_button = PhotoImage(
        file=relative_to_assets("order_button.png"))
    btn_order = Button(
        admin_canvas,
        image=order_button,
        borderwidth=0,
        highlightthickness=0,
        command=bill.Billing,
        relief="flat"
    )
    btn_order.place(
        x=240.0,
        y=72.0,
        width=714.0,
        height=60.0
    )

    # button_image_2 = PhotoImage(
    #     file=relative_to_assets("logout_btn.png"))
    # logout_btn = Button(
    #     admin_canvas,
    #     image=button_image_2,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: print("button_2 clicked"),
    #     relief="flat"
    # )
    # logout_btn.place(
    #     x=900.0,
    #     y=15.0,
    #     width=87.0,
    #     height=40.0
    # )

    import display_stock.display_expired_medicines as exp
    view_expired_med_button = PhotoImage(
        file=relative_to_assets("view_expired_med_button.png"))
    btn_view_expired_med = Button(
        admin_canvas,
        image=view_expired_med_button,
        borderwidth=0,
        highlightthickness=0,
        command=exp.display_expired_medicines,
        relief="flat"
    )
    btn_view_expired_med.place(
        x=240.0,
        y=138.0,
        width=714.0,
        height=60.0
    )

    import display_stock.display_low_stock_medicine as low
    low_stock_button = PhotoImage(
        file=relative_to_assets("low_stock_button.png"))
    btn_low_stock = Button(
        admin_canvas,
        image=low_stock_button,
        borderwidth=0,
        highlightthickness=0,
        command=low.display_low_stock_medicines,
        relief="flat"
    )
    btn_low_stock.place(
        x=240.0,
        y=204.0,
        width=714.0,
        height=60.0
    )

    import display_stock.display_stock as stock
    current_stock_button = PhotoImage(
        file=relative_to_assets("current_stock_button.png"))
    btn_current_stock = Button(
        admin_canvas,
        image=current_stock_button,
        borderwidth=0,
        highlightthickness=0,
        command=stock.display_stock,
        relief="flat"
    )
    btn_current_stock.place(
        x=240.0,
        y=270.0,
        width=714.0,
        height=60.0
    )

    import report_generation.report_data as report
    annual_sales_button = PhotoImage(
        file=relative_to_assets("annual_sales_button.png"))
    btn_annual_sales = Button(
        admin_canvas,
        image=annual_sales_button,
        borderwidth=0,
        highlightthickness=0,
        command=report.report_gen_annual,
        relief="flat"
    )
    btn_annual_sales.place(
        x=240.0,
        y=336.0,
        width=714.0,
        height=60.0
    )
    month_wise_button = PhotoImage(
        file=relative_to_assets("month_wise_button.png"))
    btn_month_wise = Button(
        admin_canvas,
        image=month_wise_button,
        borderwidth=0,
        highlightthickness=0,
        command=report.report_gen_monthly,
        relief="flat"
    )
    btn_month_wise.place(
        x=240.0,
        y=402.0,
        width=714.0,
        height=60.0
    )

    day_wise_button = PhotoImage(
        file=relative_to_assets("day_wise_button.png"))
    btn_day_wise = Button(
        admin_canvas,
        image=day_wise_button,
        borderwidth=0,
        highlightthickness=0,
        command=report.report_gen_daily,
        relief="flat"
    )
    btn_day_wise.place(
        x=240.0,
        y=468.0,
        width=714.0,
        height=60.0
    )

    dashboard_pharma_img = PhotoImage(
        file=relative_to_assets("dashboard_pharma_img.png"))
    img_dashboard_pharma = admin_canvas.create_image(
        96.0,
        274.0,
        image=dashboard_pharma_img
    )

    admin_canvas.create_text(
        336.0,
        8.0,
        anchor="nw",
        text="CYMBELYN  PHARMACY",
        fill="#288652",
        font=("Lato Bold", 48 * -1)
    )

    admin_window.resizable(False, False)
    admin_window.mainloop()


def open_cashier_window():
    admin_window = Toplevel()
    admin_window.geometry("1000x550")
    admin_window.configure(bg="#FFFEFE")
    center_window(admin_window, 1000, 550)

    admin_canvas = Canvas(
        admin_window,
        bg="#FFFEFE",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    admin_canvas.place(x=0, y=0)

    dashboard_button_bg = PhotoImage(
        file=relative_to_assets("dashboard_button_bg.png"))
    canvas_dashboard_button_bg = admin_canvas.create_image(
        597.0,
        300.0,
        image=dashboard_button_bg
    )

    import billing.billing as bill
    order_button = PhotoImage(
        file=relative_to_assets("order_button.png"))
    btn_order = Button(
        admin_canvas,
        image=order_button,
        borderwidth=0,
        highlightthickness=0,
        command=bill.Billing,
        relief="flat"
    )
    btn_order.place(
        x=240.0,
        y=72.0,
        width=714.0,
        height=60.0
    )

    import display_stock.display_expired_medicines as exp
    view_expired_med_button = PhotoImage(
        file=relative_to_assets("view_expired_med_button.png"))
    btn_view_expired_med = Button(
        admin_canvas,
        image=view_expired_med_button,
        borderwidth=0,
        highlightthickness=0,
        command=exp.display_expired_medicines,
        relief="flat"
    )
    btn_view_expired_med.place(
        x=240.0,
        y=138.0,
        width=714.0,
        height=60.0
    )

    import display_stock.display_low_stock_medicine as low
    low_stock_button = PhotoImage(
        file=relative_to_assets("low_stock_button.png"))
    btn_low_stock = Button(
        admin_canvas,
        image=low_stock_button,
        borderwidth=0,
        highlightthickness=0,
        command=low.display_low_stock_medicines,
        relief="flat"
    )
    btn_low_stock.place(
        x=240.0,
        y=204.0,
        width=714.0,
        height=60.0
    )

    import display_stock.display_stock as stock
    current_stock_button = PhotoImage(
        file=relative_to_assets("current_stock_button.png"))
    btn_current_stock = Button(
        admin_canvas,
        image=current_stock_button,
        borderwidth=0,
        highlightthickness=0,
        command=stock.display_stock,
        relief="flat"
    )
    btn_current_stock.place(
        x=240.0,
        y=270.0,
        width=714.0,
        height=60.0
    )

    dashboard_pharma_img = PhotoImage(
        file=relative_to_assets("dashboard_pharma_img.png"))
    img_dashboard_pharma = admin_canvas.create_image(
        96.0,
        274.0,
        image=dashboard_pharma_img
    )

    admin_canvas.create_text(
        336.0,
        8.0,
        anchor="nw",
        text="CYMBELYN  PHARMACY",
        fill="#288652",
        font=("Lato Bold", 48 * -1)
    )

    admin_window.resizable(False, False)
    admin_window.mainloop()


def create_login_window():
    window = Tk()
    window.title("Cymbelyn Pharmacy System")
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")
    center_window(window, 1000, 550)

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    login_rectangle = PhotoImage(
        file=relative_to_assets("login_rectangle.png"))
    image_1 = canvas.create_image(
        631.0,
        252.0,
        image=login_rectangle
    )

    pharma_image = PhotoImage(
        file=relative_to_assets("pharma_image.png"))
    image_2 = canvas.create_image(
        161.0,
        275.0,
        image=pharma_image
    )

    textbox_rectangle_bg1 = PhotoImage(
        file=relative_to_assets("textbox_rectangle_bg1.png"))
    image_3 = canvas.create_image(
        613.0,
        394.0,
        image=textbox_rectangle_bg1
    )

    textbox_rectangle_bg2 = PhotoImage(
        file=relative_to_assets("textbox_rectangle_bg2.png"))
    image_4 = canvas.create_image(
        613.0,
        285.0,
        image=textbox_rectangle_bg2
    )

    canvas.create_text(
        480.0,
        367.0,
        anchor="nw",
        text="Password:",
        fill="#288652",
        font=("Inter Bold", 20 * -1)
    )

    canvas.create_text(
        480.0,
        258.0,
        anchor="nw",
        text="User:",
        fill="#288652",
        font=("Inter Bold", 20 * -1)
    )

    password_text_box = PhotoImage(
        file=relative_to_assets("password_text_box.png"))
    password_bg_1 = canvas.create_image(
        616.5,
        409.5,
        image=password_text_box
    )
    password_text_box = Entry(
        bd=0,
        bg="#EAEAEA",
        fg="#000716",
        highlightthickness=0,
        show='*',
        font=("Inter", 17)
    )
    password_text_box.place(
        x=452.0,
        y=395.0,
        width=329.0,
        height=27.0
    )

    user_combo_box = CTkComboBox(master=window, width=329, height=33,
                                    values=["Choose user", "Admin", "Cashier"],
                                    button_color="#2A8C55", border_color="#2A8C55", border_width=2,
                                    button_hover_color="#207244",
                                    dropdown_hover_color="#207244", dropdown_fg_color="#2A8C55",

                                    dropdown_text_color="#fff",
                                    font=("Inter", 17)
                                    )
    user_combo_box.configure(values=["Admin", "Cashier"], text_color="black")
    user_combo_box.place(
        x=452.0,
        y=286.0,
    )



    password_icon = PhotoImage(
        file=relative_to_assets("password_icon.png"))
    image_5 = canvas.create_image(
        459.0,
        377.0,
        image=password_icon
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("login_button.png"))
    validate_login_partial = partial(validate_login, user_combo_box, password_text_box, window)
    login_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=validate_login_partial,
        relief="flat"
    )
    login_button.place(
        x=452.0,
        y=474.0,
        width=359.0,
        height=40.0
    )

    user_icon = PhotoImage(
        file=relative_to_assets("user_icon.png"))
    image_6 = canvas.create_image(
        460.0,
        267.0,
        image=user_icon
    )

    pharma_icon = PhotoImage(
        file=relative_to_assets("pharma_icon.png"))
    image_7 = canvas.create_image(
        854.0,
        146.0,
        image=pharma_icon
    )

    canvas.create_text(
        482.0,
        99.0,
        anchor="nw",
        text="YMBELYN\n    PHARMACY",
        fill="#FFFFFF",
        font=("Poppins Bold", 36 * -1)
    )

    canvas.create_text(
        421.0,
        56.0,
        anchor="nw",
        text="C",
        fill="#FFFFFF",
        font=("Inter ExtraBold", 80 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


def validate_login(username_entry, password_entry, window):
    """Validates the login credentials."""
    username_entered = username_entry.get()
    password_entered = password_entry.get()

    saved_login_details = read_saved_login_details()

    if username_entered in saved_login_details:
        if password_entered == saved_login_details[username_entered]:
            if username_entered == "Admin":
                window.withdraw()
                open_admin_window()
            elif username_entered == "Cashier":
                window.withdraw()
                open_cashier_window()

            # Close the login window
            window.destroy()
        else:
            tkinter.messagebox.showinfo("LOGIN", "INVALID PASSWORD", icon='warning')
    else:
        tkinter.messagebox.showinfo("LOGIN", "INVALID USERNAME", icon='warning')



if __name__ == "__main__":
    create_login_window()
