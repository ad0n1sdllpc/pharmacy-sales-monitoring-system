from tkinter import *
import json

def display_stock():
    with open("data\medicine_stock.json", "r") as read_it:
        medicine_stock = json.load(read_it)
    headings = ["MEDICINE ID", "MEDICINE NAME",
                "QUANTITY", "BIN NUMBER", "EXPIRY DATE", "COST"]
    row_headings = ["name", "quantity", "bin no", "expiry date", "cost"]
    medicine_ids = [id for id in medicine_stock]

    # Set the limit for visible rows
    visible_rows = 10
    total_columns = 6

    class Table:
        def __init__(self, root):
            for j in range(0, total_columns):
                self.e = Entry(root, width=20, justify="center", fg='white',
                               bg='#288652', font=('Arial', 12, 'bold'))
                self.e.grid(row=0, column=j)
                self.e.insert(END, headings[j])

            for i in range(0, len(medicine_stock)):
                self.e = Entry(root, justify="center", width=20,
                               fg='white', font=('Arial', 16, 'bold'))
                self.e.grid(row=i+1, column=0)
                self.e.insert(END, medicine_ids[i])
                self.e.config(bg='#288652')  # Set the background color for the row header

                for j in range(1, total_columns):
                    self.e = Entry(root, justify="center", width=15,
                                   fg='black', bg='#C4E7C2', font=('Arial', 16, 'bold'))
                    self.e.grid(row=i+1, column=j)
                    self.e.insert(
                        END, medicine_stock[medicine_ids[i]][row_headings[j-1]])

    root = Tk()
    root.title('CYMBELYN PHARMACY STOCK DISPLAY')
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
    canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

    # Set the canvas scrolling region
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Update the window size to fit the visible rows
    window_height = min(frame.winfo_reqheight(), visible_rows * 30)  # Assuming each row has height 30
    window_width = frame.winfo_reqwidth()
    root.geometry('{}x{}+{}+{}'.format(window_width, window_height,
                                        (root.winfo_screenwidth() - window_width) // 2,
                                        (root.winfo_screenheight() - window_height) // 2))

    root.mainloop()

# Uncomment the line below to display the stock
# display_stock()
