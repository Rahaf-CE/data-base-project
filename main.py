import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector
import random
import string
import re
from datetime import datetime
from datetime import date
from admin import UI
from PIL import Image, ImageTk
# Function to convert Arabic numerals to Roman numerals


def arabic_to_roman(number):
    roman_numerals = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
        50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
    }
    result = ''
    for value, numeral in sorted(roman_numerals.items(), key=lambda x: x[0], reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result
##########################################################################################

# Function to check if the email is in a valid format
def is_valid_email(email):
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))


# Function to get the next user ID
def get_next_user_id():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1201319",
            database="online_shope"
        )
        cursor = connection.cursor()

        select_query = "SELECT MAX(user_id) FROM User"
        cursor.execute(select_query)

        result = cursor.fetchone()
        if result[0]:
            return int(result[0]) + 1  # Convert to int before adding 1
        else:
            return 1  # If no existing user, start from 1

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to generate a random user ID
def generate_random_user_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))


# Function for the sign-up process
def sign_up():
    name = name_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    password = password_entry.get()
    user_type = user_type_var.get()

    # Check if the email is in a valid format
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return

    user_id = get_next_user_id()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1201319",
            database="online_shope"
        )
        cursor = connection.cursor()

        insert_query = "INSERT INTO User (user_id, name, email, address, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (user_id, name, email, address, password, user_type)
        cursor.execute(insert_query, data)
        connection.commit()

        messagebox.showinfo("Success",   f"Sign up successful! Your user ID is: {user_id}. Save this ID in case you forget your password.")

        # Clear entry fields after successful sign up
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#############################################################################################################
# Function for the login process
def log_in():
    email = login_email_entry.get()
    password = login_password_entry.get()

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1201319",
            database="online_shope"
        )

        cursor = connection.cursor()

        select_query = "SELECT * FROM User WHERE email = %s AND password = %s"
        data = (email, password)
        cursor.execute(select_query, data)

        result = cursor.fetchone()

        if result:
            user_type = result[5]  # Assuming the user_type column is at index 5
            name = result[1]  # Assuming the name column is at index 1

            if user_type == "Admin":
                messagebox.showinfo("Success", f"Hello Admin {name}! Login successful!")
                root.destroy()
                UI()

            elif user_type == "Customer":
                customer_id = result[0]  # Assuming the user_id column is at index 0
                messagebox.showinfo("Success", f"Hello Customer {name}! Login successful!")

                # Modify this part to open the show_categories_window only for customers
                show_categories_window(customer_id)

                return

            # Clear entry fields after successful log in
            login_email_entry.delete(0, tk.END)
            login_password_entry.delete(0, tk.END)

        else:
            messagebox.showerror("Error", "Invalid email or password")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

##################################################################################################
# Function for the forget password process
def forget_password():
    email = simpledialog.askstring("Forget Password", "Enter your email:")
    user_id = simpledialog.askstring("Forget Password", "Enter your user ID:")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1201319",
            database="online_shope"
        )

        cursor = connection.cursor()

        select_query = "SELECT * FROM User WHERE email = %s AND user_id = %s"
        data = (email, user_id)
        cursor.execute(select_query, data)

        result = cursor.fetchone()

        if result:
            new_password = simpledialog.askstring("Forget Password", "Enter a new password:")

            update_query = "UPDATE User SET password = %s WHERE email = %s AND user_id = %s"
            update_data = (new_password, email, user_id)
            cursor.execute(update_query, update_data)
            connection.commit()

            messagebox.showinfo("Success", "Password updated successfully!")
        else:
            messagebox.showerror("Error", "Invalid email or user ID")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

#
def clear_entries():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    login_email_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)

##########################################################################################################
def show_categories_window(customer_id):
    clear_entries()
    root.withdraw()

    categories_window = tk.Toplevel(root)
    categories_window.title("Choose Category")
    categories_window.configure(bg="light yellow")
    categories_window.geometry("2000x1200")

    # Load and display a specific photo
    specific_image_path = "background_image2.png"  # Replace with the path to your image
    specific_image = Image.open(specific_image_path)
    specific_image = specific_image.resize((600, 200))  # Resize the image
    specific_photo = ImageTk.PhotoImage(specific_image)
    specific_image_label = tk.Label(categories_window, image=specific_photo)
    specific_image_label.image = specific_photo  # Keep a reference!
    specific_image_label.pack()

    def logout():
        categories_window.destroy()
        root.deiconify()

    def fetch_product_details(category):
        print(f"Fetching products for category: {category}")
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1201319",
                database="online_shope"
            )
            cursor = connection.cursor()

            select_products_query = "SELECT product_id, price FROM product WHERE category = %s"
            cursor.execute(select_products_query, (category,))
            products_data = cursor.fetchall()

            return products_data

        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Error: {}".format(err))
        finally:
            if connection:
                connection.close()

    def get_image_path(product_id):
        # Replace with your database connection details
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1201319",
            database="online_shope"
        )
        cursor = connection.cursor()
        query = "SELECT images FROM product WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0] if result else None

    def display_product_details(products_data, category):
        products_details_window = tk.Toplevel(categories_window)
        products_details_window.title("Product Details")
        products_details_window.configure(bg="lightyellow")
        products_details_window.geometry("600x800")

        for i, (product_id, price) in enumerate(products_data):
            product_label = tk.Label(products_details_window, text=f"Product ID: {product_id}\nPrice: ${price}",padx=10, pady=10)
            product_label.pack()

            # Retrieve and display the image
            image_path = get_image_path(product_id)
            if image_path:
                image = Image.open(image_path)
                image = image.resize((100, 100))  # Resize if necessary
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(products_details_window, image=photo)
                image_label.image = photo  # Keep a reference!
                image_label.pack()

        tk.Label(products_details_window, text=f"Enter Product ID to buy (Category: {category}):", padx=10,pady=10).pack()
        product_id_entry = tk.Entry(products_details_window)
        product_id_entry.pack()


        def submit_buy_request():
            selected_product_id = product_id_entry.get()

            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1201319",
                    database="online_shope"
                )
                cursor = connection.cursor()

                # Get the current date
                purchase_date = date.today()

                # Check if the product exists and belongs to the selected category
                select_category_query = "SELECT category, quantity FROM Product WHERE product_id = %s"
                cursor.execute(select_category_query, (selected_product_id,))
                product_data = cursor.fetchone()

                if not product_data:
                    messagebox.showerror("Error", "Product not found!")
                    return

                product_category, product_quantity = product_data

                if product_category != category:
                    messagebox.showerror("Error", f"Invalid Product ID for {category}!")
                    return

                if product_quantity <= 0:
                    messagebox.showerror("Error", "Product is out of stock!")
                    return

                # Assuming you have a default value for the address or handle it in the database
                select_price_query = "SELECT price FROM Product WHERE product_id = %s"
                cursor.execute(select_price_query, (selected_product_id,))
                product_price = cursor.fetchone()[0]

                # Insert the order
                insert_order_query = "INSERT INTO Orders (customer_id, product_id, date, payment) VALUES (%s, %s, %s, %s)"
                order_data = (customer_id, selected_product_id, purchase_date, product_price)
                cursor.execute(insert_order_query, order_data)

                # Update product quantity
                update_quantity_query = "UPDATE Product SET quantity = quantity - 1 WHERE product_id = %s"
                cursor.execute(update_quantity_query, (selected_product_id,))

                connection.commit()

                messagebox.showinfo("Success", "Your order has been placed successfully!")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", "Error: {}".format(err))
            finally:
                if connection:
                    connection.close()

            products_details_window.destroy()

        buy_button = tk.Button(products_details_window, text="Buy", command=submit_buy_request)
        buy_button.pack()

    def display_all_orders_window(customer_id):
        all_orders_window = tk.Toplevel(categories_window)
        all_orders_window.title("All Orders")
        all_orders_window.configure(bg="pink")
        all_orders_window.geometry("2000x1200")

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1201319",
                database="online_shope"
            )
            cursor = connection.cursor()

            select_all_orders_query = "SELECT order_id, product_id, date, payment FROM Orders WHERE customer_id = %s"
            cursor.execute(select_all_orders_query, (customer_id,))
            all_orders_data = cursor.fetchall()

            for i, (order_id, product_id, order_date, payment) in enumerate(all_orders_data):
                order_label = tk.Label(all_orders_window,text=f"Order ID: {order_id}\nProduct ID: {product_id}\nDate: {order_date}\nPayment: ${payment}",padx=10, pady=10)
                order_label.pack()

            tk.Label(all_orders_window, text="Enter Order ID to delete:", padx=10, pady=10).pack()
            order_id_entry = tk.Entry(all_orders_window)
            order_id_entry.pack()

            def submit_delete_request():
                entered_value = order_id_entry.get()

                if not entered_value.isdigit():
                    messagebox.showerror("Error", "Please enter a valid Order ID (a number).")
                    return

                selected_order_id = int(entered_value)

                try:
                    connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="1201319",
                        database="online_shope"
                    )
                    cursor = connection.cursor()

                    check_order_query = "SELECT customer_id, product_id FROM Orders WHERE order_id = %s"
                    cursor.execute(check_order_query, (selected_order_id,))
                    order_data = cursor.fetchone()

                    if not order_data or order_data[0] != customer_id:
                        messagebox.showerror("Error", "Invalid Order ID for the customer!")
                        return

                    delete_order_query = "DELETE FROM Orders WHERE order_id = %s"
                    cursor.execute(delete_order_query, (selected_order_id,))

                    # Get the product ID and quantity for the deleted order
                    product_id = order_data[1]

                    # Increase the product quantity
                    update_quantity_query = "UPDATE Product SET quantity = quantity + 1 WHERE product_id = %s"
                    cursor.execute(update_quantity_query, (product_id,))

                    connection.commit()

                    messagebox.showinfo("Success", "Order has been deleted successfully!")

                except mysql.connector.Error as err:
                    messagebox.showerror("Error", "Error: {}".format(err))
                finally:
                    if connection:
                        connection.close()

                all_orders_window.withdraw()
                all_orders_window.destroy()
                display_all_orders_window(customer_id)

            delete_button = tk.Button(all_orders_window, text="Delete", command=submit_delete_request)

            delete_button.pack()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Error: {}".format(err))
        finally:
            if connection:
                connection.close()



    def category_button_clicked(category):
        products_data = fetch_product_details(category)
        display_product_details(products_data, category)

    def logout_button_clicked():
        logout()

    button_colors = ["purple", "purple", "purple", "purple", "purple"]
    tk.Label(categories_window, text="CHOOSE THE TYPE OF BAG", font=("Helvetica", 16), pady=10, bg="white").pack()

    categories = ["laptop_bag", "hand_bag", "back_bag"]
    button_colors = ["pink", "pink", "pink"]  # Replace with your actual colors

    for i, category in enumerate(categories):
        tk.Button(categories_window, text=category, command=lambda c=category: category_button_clicked(c),width=30, height=5, bg=button_colors[i]).pack(pady=15)

    # Add Delete button
    tk.Button(categories_window, text="Delete Order", command=lambda: display_all_orders_window(customer_id),width=30, height=5, bg="green").pack(pady=15)

    # Add Logout button below the other buttons
    tk.Button(categories_window, text="Logout", command=logout_button_clicked,width=30, height=5, bg="red").pack(pady=(15, 30))
    tk.mainloop()




# Function to format the current time in Roman numerals
def get_roman_time():
    now = datetime.now()
    roman_hour = arabic_to_roman(int(now.strftime("%H")))
    roman_minute = arabic_to_roman(int(now.strftime("%M")))
    roman_time = f"{roman_hour}:{roman_minute}"
    return roman_time



#####################################################################################################################3

# Common font for all elements
common_font = ("Times New Roman", 12)

# GUI setup
root = tk.Tk()
root.title("ONLINE SHOP")

# Header with a Roman numeral-themed font
header_label = tk.Label(root, text="Reality SHOP Of Bags", font=("Times New Roman", 36, "bold"), pady=10, padx=20, fg="purple")
header_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")  # Set sticky to "w"

# Sign Up Frame
sign_up_frame = tk.Frame(root)
sign_up_frame.configure(bg="lightyellow")
tk.Label(sign_up_frame, text="Sign Up", font=("Times New Roman", 18, "bold"), pady=10).grid(row=0, column=0,columnspan=2, pady=10,sticky="w")

tk.Label(sign_up_frame, text="Name:", font=common_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
name_entry = tk.Entry(sign_up_frame)
name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(sign_up_frame, text="Email:", font=common_font).grid(row=2, column=0, padx=5, pady=5, sticky="w")
email_entry = tk.Entry(sign_up_frame)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(sign_up_frame, text="Address:", font=common_font).grid(row=3, column=0, padx=5, pady=5, sticky="w")
address_entry = tk.Entry(sign_up_frame)
address_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(sign_up_frame, text="Password:", font=common_font).grid(row=4, column=0, padx=5, pady=5, sticky="w")
password_entry = tk.Entry(sign_up_frame, show="*")
password_entry.grid(row=4, column=1, padx=5, pady=5)

# Radio button for user type
user_type_var = tk.StringVar()
user_type_var.set("Customer")  # Default selection
user_type_frame = tk.Frame(sign_up_frame)
user_type_frame.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

tk.Label(user_type_frame, text="Select User Type:", font=common_font).pack(side=tk.LEFT)
admin_radio = tk.Radiobutton(user_type_frame, text="Admin", variable=user_type_var, value="Admin", font=common_font)
admin_radio.pack(side=tk.LEFT)
customer_radio = tk.Radiobutton(user_type_frame, text="Customer", variable=user_type_var, value="Customer",font=common_font)
customer_radio.pack(side=tk.LEFT)

sign_up_button = tk.Button(sign_up_frame, text="Sign Up", command=sign_up, bg="green", fg="white", font=common_font)
sign_up_button.grid(row=6, column=1, columnspan=2, pady=10, sticky="w")

# Pack the sign_up_frame immediately after configuring it
sign_up_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")

# Login Frame
login_frame = tk.Frame(root)
login_frame.configure(bg="lightyellow")
tk.Label(login_frame, text="Login", font=("Times New Roman", 18, "bold"), pady=10).grid(row=0, column=0, columnspan=2,pady=10, sticky="w")

tk.Label(login_frame, text="Email:", font=common_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
login_email_entry = tk.Entry(login_frame)
login_email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(login_frame, text="Password:", font=common_font).grid(row=2, column=0, padx=5, pady=5, sticky="w")
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.grid(row=2, column=1, padx=5, pady=5)

login_button = tk.Button(login_frame, text="Log In", command=log_in, bg="green", fg="white", font=common_font)
login_button.grid(row=3, column=1, columnspan=2, pady=10, sticky="w")

# Pack the login_frame immediately after configuring it
login_frame.grid(row=2, column=0, padx=20, pady=20, sticky="w")

# Forget Password Button
forget_password_button = tk.Button(root, text="Forget Password", command=forget_password, bg="red", fg="white",font=common_font)
forget_password_button.grid(row=3, column=0, padx=60, pady=20, sticky="w")

# Centering the image
background_image = tk.PhotoImage(file="bb.png")
background_label = tk.Label(root, image=background_image)
background_label.grid(row=1, column=1, rowspan=3, padx=100, pady=20, sticky="e")

root.configure(bg="lightblue")
root.geometry("2000x1200")
root.mainloop()
