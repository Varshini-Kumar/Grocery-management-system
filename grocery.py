import mysql.connector
import re
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="W7301@jqir#",
    database="grocerydb"
)
cursor = connection.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    quantity INT NOT NULL,
                    price FLOAT NOT NULL
                )''')
connection.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS billnew (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT NOT NULL,
                    product_id INT NOT NULL,
                    product_name VARCHAR(255) NOT NULL,
                    amount FLOAT NOT NULL,
                    total FLOAT NOT NULL
                )''')
connection.commit()

def add_product():
    name = product_name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    cursor.execute("INSERT INTO product (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    connection.commit()
    display_products()

def display_products():
    products_listbox.delete(0, END)
    cursor.execute("SELECT * FROM product")
    for row in cursor.fetchall():
        products_listbox.insert(END, row)

def open_product_management_window():
    product_management_window = Toplevel()
    product_management_window.title("Product Management")
    product_management_window.geometry("600x400")
    bg_image = Image.open("login.jpg")
    bg_image = bg_image.resize((600, 400))
    bg_image = bg_image.convert("RGB")
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(product_management_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    bg_label.image = bg_photo
    global products_listbox
    global product_name_entry
    global quantity_entry
    global price_entry
    
    product_name_label = Label(product_management_window, text="Product Name:", font=("bookman old style", 10, "bold"))
    product_name_label.pack()
    product_name_entry = Entry(product_management_window)
    product_name_entry.pack(pady=5)

    quantity_label = Label(product_management_window, text="Quantity:", font=("bookman old style", 10, "bold"))
    quantity_label.pack()
    quantity_entry = Entry(product_management_window)
    quantity_entry.pack(pady=5)

    price_label = Label(product_management_window, text="Price:", font=("bookman old style", 10, "bold"))
    price_label.pack()
    price_entry = Entry(product_management_window)
    price_entry.pack(pady=5)

    add_button = Button(product_management_window, text="Add Product", font=("bookman old style", 10, "bold"), command=add_product, bg="blue", fg="white")
    add_button.pack(pady=5)

    products_listbox = Listbox(product_management_window, width=50, height=10)
    products_listbox.pack(pady=10)

    display_products()

def open_billing_window():

    global product_name_entry, quantity_entry, price_entry,products_listbox,total_entry,customer_id_entry
    
    billing_window = Toplevel()
    billing_window.title("Billing")
    billing_window.geometry("700x500")
    
    
    bg_image_billing = Image.open("login.jpg")
    bg_image_billing = bg_image_billing.convert("RGB")
    bg_photo_billing = ImageTk.PhotoImage(bg_image_billing)

    bg_label = Label(billing_window, image=bg_photo_billing)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    bg_label.image = bg_photo_billing

    # Customer ID
    customer_id_label = Label(billing_window, text="Customer ID:", font=("bookman old style", 10, "bold"))
    customer_id_label.grid(row=0, column=0, padx=10, pady=5)
    customer_id_entry = Entry(billing_window)
    customer_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Product details
    product_name_label = Label(billing_window, text="Product Name:", font=("bookman old style", 10, "bold"))
    product_name_label.grid(row=1, column=0, padx=10, pady=5)
    product_name_entry = Entry(billing_window)
    product_name_entry.grid(row=1, column=1, padx=10, pady=5)

    quantity_label = Label(billing_window, text="Quantity:", font=("bookman old style", 10, "bold"))
    quantity_label.grid(row=2, column=0, padx=10, pady=5)
    quantity_entry = Entry(billing_window)
    quantity_entry.grid(row=2, column=1, padx=10, pady=5)

    price_label = Label(billing_window, text="Price:", font=("bookman old style", 10, "bold"))
    price_label.grid(row=3, column=0, padx=10, pady=5)
    price_entry = Entry(billing_window)
    price_entry.grid(row=3, column=1, padx=10, pady=5)

    add_button = Button(billing_window, text="Add Product", font=("bookman old style", 10, "bold"), command=add_product_to_bill,bg="blue",fg="white")
    add_button.grid(row=4, columnspan=2, padx=10, pady=5)

    # Listbox to display products
    products_listbox = Listbox(billing_window, width=50, height=10)
    products_listbox.grid(row=5, columnspan=2, padx=10, pady=5)

    # Calculate total
    calculate_button = Button(billing_window, text="Calculate Total", font=("bookman old style", 10, "bold"),
                          command=calculate_total, bg="blue", fg="white")

    calculate_button.grid(row=6, columnspan=2, padx=10, pady=5)

    total_label = Label(billing_window, text="Total Amount:", font=("bookman old style", 10, "bold"))
    total_label.grid(row=7, column=0, padx=10, pady=5)
    total_entry = Entry(billing_window)
    total_entry.grid(row=7, column=1, padx=10, pady=5)

    # Process billing
    process_button = Button(billing_window, text="Process Billing", font=("bookman old style", 10, "bold"), command=process_billing, bg="blue", fg="white")
    process_button.grid(row=8, columnspan=2, padx=10, pady=5)
    
def add_product_to_bill():
    global products_listbox
    product_name = product_name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
   
    if quantity.strip() and price.strip():
        amount = int(quantity) * float(price)
        products_listbox.insert(END, f"{product_name} - {quantity} - {amount:.2f}")
    else:
        messagebox.showerror("Error", "Quantity and price cannot be empty.")


def calculate_total():
    total = 0
    for item in products_listbox.get(0, END):
        parts = item.split('-')
        if len(parts) >= 3:
            amount_str = parts[2].strip().replace('', '')  # Remove the currency symbol
            try:
                amount = float(amount_str)
                total += amount
            except ValueError:
                messagebox.showerror("Error", f"Invalid amount format: {amount_str}")
                return
    total_entry.delete(0, END)
    total_entry.insert(END, f"{total:.2f}")

    
    
def process_billing():
    customer_id = customer_id_entry.get()
    total_amount = total_entry.get()
 # Replace with the actual product ID
    # Insert billing details into the database
    for item in products_listbox.get(0, END):
        product_name, quantity, _ = item.split('-')
        cursor.execute("INSERT INTO billnew (customer_id, product_name, quantity, total) VALUES (%s, %s, %s, %s)",
               (customer_id, product_name.strip(), quantity.strip(), total_amount))

    connection.commit()
    messagebox.showinfo("Success", "Billing details added successfully.")
    clear_fields()



def clear_fields():
    customer_id_entry.delete(0, END)
    products_listbox.delete(0, END)
    total_entry.delete(0, END)

def open_options_window():
    options_window = Toplevel(login_window)
    options_window.title("Options")
    options_window.geometry("400x300")
    bg_image1 = Image.open("login.jpg")
    bg_image1 = bg_image1.resize((400, 300))  
    bg_image1 = ImageTk.PhotoImage(bg_image1)
    bg_label = Label(options_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    #prod mgmt button
    product_management_button = Button(options_window, text="Product Management", font=("bookman old style", 10, "bold"), command=open_product_management_window, bg="blue", fg="white")
    product_management_button.pack(pady=(100,10))
     #billing button
    billing_button = Button(options_window, text="Billing", font=("bookman old style", 10, "bold"), command=open_billing_window, bg="blue", fg="white")
    billing_button.pack(pady=10)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin":  # Change these to your actual username and password
        open_options_window()
        # login_window.destroy() # Commented out to prevent closing the login window immediately
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Login window
login_window = Tk()
login_window.title("Login")
login_window.geometry("500x400")  # Increase the size of the window

# Background Image
bg_image = Image.open("login.jpg")
bg_image = bg_image.resize((500, 400))  # Resize the image to fit the window
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = Label(login_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Label to display "Purple Groceries"
label = Label(login_window, text="Purple Groceries", font=("bookman old style", 20, "bold", "italic"))
label.pack(pady=10)

# Username Label and Entry
username_label = Label(login_window, text="Username:", font=("bookman old style", 10, "bold"))
username_label.pack(pady=5)
username_entry = Entry(login_window)
username_entry.pack(pady=5)

# Password Label and Entry
password_label = Label(login_window, text="Password:", font=("bookman old style", 10, "bold"))
password_label.pack(pady=5)
password_entry = Entry(login_window, show="*")
password_entry.pack(pady=5)

# Login Button
login_button = Button(login_window, text="Login", font=("bookman old style", 10, "bold"), command=login, bg="blue", fg="white")
login_button.pack(pady=5)

login_window.mainloop()
