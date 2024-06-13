from tkinter import *
import json
from tkinter import messagebox

def display_low_stock_medicines():
    with open("data\\medicine_stock.json", "r") as read_it:
        medicine_stock = json.load(read_it)
    low_stock_medicines = []
    for medicine_id in medicine_stock:
        if medicine_stock[medicine_id]["quantity"] <= 5:
            low_stock_medicines.append(medicine_id)

    if len(low_stock_medicines) > 0:
        headings = ["MEDICINE ID", "MEDICINE NAME", "QUANTITY"]
        row_headings = ["name", "quantity"]
        visible_rows = 10
        total_columns = 3

        class Table:
            def __init__(self, root):
                for column_no in range(total_columns):
                    self.e = Entry(root, width=20, justify="center", fg='white',
                                   bg='#288652', font=('Arial', 12, 'bold'))
                    self.e.grid(row=0, column=column_no)
                    self.e.insert(END, headings[column_no])

                row_no = 1
                for medicine_id in low_stock_medicines:
                    for column_no in range(total_columns):
                        self.e = Entry(root, width=15, justify="center",
                                       fg='black', bg='#C4E7C2', font=('Arial', 16, 'bold'))
                        self.e.grid(row=row_no, column=column_no)
                        if column_no == 0:
                            self.e.insert(END, medicine_id)
                        else:
                            self.e.insert(
                                END, medicine_stock[medicine_id][row_headings[column_no-1]])
                    row_no += 1

                self.e = Entry(root, width=32, justify="center",
                               fg='red', bg='gainsboro', font=('Arial', 16, 'bold'))
                self.e.grid(row=total_rows+1, column=0, columnspan=total_columns)
                self.e.insert(
                    END, "Restock the above medicines soon")

        total_rows = len(low_stock_medicines)
        root = Tk()
        root.title('CYMBELYN PHARMACY LOW STOCK MEDICINES')
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
        messagebox.showinfo("Low stock medicines review", "No low stock medicines present in stock")

# Uncomment the line below to display the low stock medicines
# display_low_stock_medicines()
