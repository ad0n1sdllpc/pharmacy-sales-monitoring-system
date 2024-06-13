import datetime
from tkinter import *
import json
from tkinter import messagebox

def display_expired_medicines():
    with open("data\medicine_stock.json", "r") as read_it:
        medicine_stock = json.load(read_it)
    expiredMedicines = {}
    for medicine_id in medicine_stock:
        expiry_date_list = medicine_stock[medicine_id]["expiry date"].split("-")
        expiry_date = datetime.datetime(int(expiry_date_list[0]), int(
            expiry_date_list[1]), int(expiry_date_list[2]))
        current_time = datetime.datetime.now()
        today = datetime.datetime(
            current_time.year, current_time.month, current_time.day)
        if today > expiry_date:
            key = medicine_stock[medicine_id]["expiry date"]
            value = [medicine_id, medicine_stock[medicine_id]["name"],
                     medicine_stock[medicine_id]["bin no"]]
            expiredMedicines[medicine_id] = medicine_stock[medicine_id]

    if len(expiredMedicines) > 0:
        headings = ["MEDICINE ID", "MEDICINE NAME", "BIN NUMBER"]
        row_headings = ["name", "bin no"]

        class Table:
            def __init__(self, root):
                for column_no in range(total_columns):
                    self.e = Entry(root, width=20, justify="center", fg='white',
                                   bg='#288652', font=('Arial', 12, 'bold'))
                    self.e.grid(row=0, column=column_no)
                    self.e.insert(END, headings[column_no])

                row_no = 1
                for medicine_id in expiredMedicines:
                    for column_no in range(total_columns):
                        self.e = Entry(root, width=15, justify="center",
                                       fg='black', bg='#C4E7C2', font=('Arial', 16, 'bold'))
                        self.e.grid(row=row_no, column=column_no)
                        if column_no == 0:
                            self.e.insert(END, medicine_id)
                        elif column_no == 1:
                            self.e.insert(
                                END, expiredMedicines[medicine_id]["name"])
                        else:
                            self.e.insert(
                                END, expiredMedicines[medicine_id]["bin no"])
                    row_no += 1

                # Add the text display entry below the table
                self.e = Entry(root, width=32, justify="center",
                               fg='red', bg='gainsboro', font=('Arial', 16, 'bold'))
                self.e.grid(row=row_no + 1, column=0, columnspan=total_columns)
                self.e.insert(
                    END, "Remove expired medicines from bins")

        total_rows = len(expiredMedicines)
        total_columns = 3
        visible_rows = 10
        root = Tk()
        root.title('CYMBELYN PHARMACY EXPIRED MEDICINES')
        root.configure(bg="gainsboro")

        # Create a canvas
        canvas = Canvas(root)
        canvas.pack(fill="both", expand=True)

        # Create a frame inside the canvas
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Create the table inside the frame
        t = Table(frame)

        # Make the canvas scrollable for both x and y directions
        x_scrollbar = Scrollbar(root, orient="horizontal", command=canvas.xview)
        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar = Scrollbar(canvas, command=canvas.yview)
        y_scrollbar.pack(side="right", fill="y")
        canvas.configure(xscrollcommand=x_scrollbar.set,
                         yscrollcommand=y_scrollbar.set)

        # Set the canvas scrolling region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Update the window size to fit the visible rows
        window_height = min(frame.winfo_reqheight(), visible_rows * 30)
        window_width = frame.winfo_reqwidth()
        root.geometry('{}x{}+{}+{}'.format(window_width, window_height,
                                           (root.winfo_screenwidth() - window_width) // 2,
                                           (root.winfo_screenheight() - window_height) // 2))

        root.mainloop()
    else:
        messagebox.showinfo(
            "Expired medicines review", "No expired medicines present in stock")

# Uncomment the line below to display the expired medicines
# display_expired_medicines()
