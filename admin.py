from tkinter import ttk, messagebox
import mysql.connector
from tkinter import simpledialog
import tkinter as tk
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class AdminGUI:
    def __init__(self, root, connection, cursor):
        self.root = root
        self.root.geometry("2000x1200")
        self.root.title("Online Shop Admin Interface")
        self.root.configure(bg="#FF69B4")  # Set pink background color for the main window

        # Welcome message label with a nice style
        welcome_label_text = "Welcome Admin! 😊\nThis is your interface to make operations in your online shop."
        welcome_label = tk.Label(self.root, text=welcome_label_text, font=('Helvetica', 24, 'bold'), fg="white",
                                 bg="#FF69B4")
        welcome_label.pack(pady=20)

        # Database connection
        self.connection = connection
        self.cursor = cursor
        # Create ttk style for buttons with black text color
        style = ttk.Style()
        style.configure("TButton", foreground="white", background="#009688", padding=10)
        style.configure("TBlackButton.TButton", foreground="black", background="#009688", padding=10)

        # button to view the product information with max paid customers
        self.button_view_max_paid_product_info = ttk.Button(text="Product Information with Most Orders",command=self.view_most_ordered_product_info,style="TBlackButton.TButton", width=45)
        self.button_view_max_paid_product_info.pack(side="top", pady=5)

        # button to view the order with the maximum payment
        self.button_view_max_payment = ttk.Button(text="View Max Payment Order",command=self.view_max_payment_orders_info,style="TBlackButton.TButton", width=45)
        self.button_view_max_payment.pack(side="top", pady=5)

        # button to view user information with the maximum number of Orders
        self.button_max_Orders_user_info = ttk.Button(text="View Max Orders User Info", command=self.view_max_orders_user_info,style="TBlackButton.TButton", width=45)
        self.button_max_Orders_user_info.pack(side="top", pady=5)

        # view all Order
        self.button_view_all_Orders = ttk.Button(text="View All Orders", command=self.view_all_Orders, style="TBlackButton.TButton", width=45)
        self.button_view_all_Orders.pack(side="top", pady=5)

        # view all Product
        self.button_view_all_Product = ttk.Button(text="View All Product", command=self.view_all_Products,style="TBlackButton.TButton", width=45)
        self.button_view_all_Product.pack(side="top", pady=5)

        # calculate total payment
        self.button_calculate_total_payment = ttk.Button(text="Calculate Total Payment",  command=self.calculate_total_payment,style="TBlackButton.TButton", width=45)
        self.button_calculate_total_payment.pack(side="top", pady=5)

        # button for adding quantity
        self.button_update_quantity = ttk.Button(text="Update Quantity", command=self.update_product_quantity,style="TBlackButton.TButton", width=45)
        self.button_update_quantity.pack(side="top", pady=5)

        # button to calculate total payment for a specific day
        self.button_calculate_daily_payment = ttk.Button(text="Calculate Daily Payment",command=self.calculate_daily_payment,style="TBlackButton.TButton", width=45)
        self.button_calculate_daily_payment.pack(side="top", pady=5)

        # Add the button in your application's layout
        self.button_plot_customer_payment_chart = ttk.Button(text="Plot Customer Payment Chart",command=self.plot_customer_payment_chart,style="TBlackButton.TButton", width=45)
        self.button_plot_customer_payment_chart.pack(side="top", pady=5)

        # Add the button in your application's layout
        self.button_plot_chart = ttk.Button(text="Plot Order Chart", command=self.plot_category_order_chart,style="TBlackButton.TButton", width=45)
        self.button_plot_chart.pack(side="top", pady=5)


    ##########################################################################
    #   Here is the Code of Connection And the oparitons on query            #
    ##########################################################################
    # function to calculate the total payment
    def calculate_total_payment(self):
        try:
            # Execute the query to calculate total payment
            query = "SELECT SUM(payment) FROM Orders"
            self.cursor.execute(query)
            total_payment = self.cursor.fetchone()[0]

            # Display the total payment in a message box
            messagebox.showinfo("Total Payment", f"The total payment is: {total_payment}")
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating total payment: {str(e)}")

    ######################################################################################################
    # function to view All Orders
    def view_all_Orders(self):
        query = "SELECT * FROM Orders"
        self.execute_and_display_Orders(query)

    def execute_and_display_Orders(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        if not data:
            messagebox.showinfo("Info", "No Orders found.")
            return

        # Create and display a new window with a Treeview widget
        window = tk.Toplevel(self.root)
        window.title("Order Details")

        tree = ttk.Treeview(window)
        tree["columns"] = tuple(["Order ID", "User ID", "Product ID", "Date", "Payment"])

        for col in tree["columns"]:
            tree.column(col, anchor="w")
            tree.heading(col, text=col)

        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both")

    ##########################################################################################################
    # function to view  all Product

    def view_all_Products(self):
        query = "SELECT * FROM Product"
        self.execute_and_display_Products(query)

    def execute_and_display_Products(self, query):
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        if not data:
            messagebox.showinfo("Info", "No prooducts found.")
            return

        # Create and display a new window with a Treeview widget
        window = tk.Toplevel(self.root)
        window.title("Product Details")

        tree = ttk.Treeview(window)
        tree["columns"] = tuple(["Product ID", "Price", "category", "quantity"])

        for col in tree["columns"]:
            tree.column(col, anchor="w")
            tree.heading(col, text=col)

        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill="both")

    ################################################################################################################
    # function to View the order With Max Payment
    def view_max_payment_orders_info(self):
        try:
            # Execute the query to get orders with the maximum payment
            query = """
                    SELECT Orders.*, payment
                    FROM Orders
                    WHERE payment = (SELECT MAX(payment) FROM Orders)
                    ORDER BY payment DESC
                    """
            self.cursor.execute(query)
            max_payment_orders_info = self.cursor.fetchall()

            if max_payment_orders_info:
                # Create and display a new window with order information
                window = tk.Toplevel(self.root)
                window.title("Max Payment Orders Info")

                order_info_label = tk.Label(window, text="Orders Information with Max Payment", font=('Arial', 16), foreground="black")
                order_info_label.pack(pady=10)

                for order_info in max_payment_orders_info:
                    order_info_text = f"Order ID: {order_info[0]}\n"
                    order_info_text += f"Customer ID: {order_info[1]}\n"
                    order_info_text += f"Product ID: {order_info[2]}\n"
                    order_info_text += f"Date: {order_info[3]}\n"




                    order_info_label = tk.Label(window, text=order_info_text, font=('Arial', 14), foreground="black")
                    order_info_label.pack(pady=10)
            else:
                messagebox.showinfo("Info", "No order information found.")

        except Exception as e:
            messagebox.showerror("Error", f"Error viewing max payment orders info: {str(e)}")

    ###################################################################################################################

    ##################################################################################################
    # Function to update product quantity
    def update_product_quantity(self):
        try:
            # Create a custom dialog for product ID and quantity input
            dialog = tk.Toplevel(self.root)
            dialog.title("Update Product Quantity")
            dialog.geometry("300x200")  # Adjust the size as needed

            product_id_label = tk.Label(dialog, text="Enter Product ID:")
            product_id_entry = tk.Entry(dialog)

            quantity_change_label = tk.Label(dialog, text="Enter Quantity Change:")
            quantity_change_entry = tk.Entry(dialog)

            # Pack entry fields
            product_id_label.pack(pady=5)
            product_id_entry.pack(pady=5)

            quantity_change_label.pack(pady=5)
            quantity_change_entry.pack(pady=5)

            # OK button with black text to submit product information
            ok_button = ttk.Button(dialog, text="OK",command=lambda: self.submit_quantity_update(dialog, product_id_entry.get(),quantity_change_entry.get()), style="TBlackButton.TButton")
            ok_button.pack(pady=10)


        except Exception as e:
            messagebox.showerror("Error", f"Error updating quantity: {str(e)}")

    # Function to submit quantity update to the database
    def submit_quantity_update(self, dialog, product_id_input, quantity_change_input):
        try:
            # Check if product_id is a valid integer
            try:
                product_id = int(product_id_input)
            except ValueError:
                messagebox.showerror("Error", "Invalid product ID. Please enter a valid number.")
                return

            # Check if quantity_change is a valid integer
            try:
                quantity_change = int(quantity_change_input)
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity change. Please enter a valid number.")
                return

            # Check if the product exists
            query = "SELECT * FROM Product WHERE product_id = %s"
            self.cursor.execute(query, (product_id,))
            product = self.cursor.fetchone()

            if product:
                # Update the quantity for the specific product
                current_quantity = product[3]  # Assuming quantity is at index 3
                new_quantity = quantity_change

                # Ensure the new quantity is not negative
                if new_quantity >= 0:
                    update_query = "UPDATE Product SET quantity = %s WHERE product_id = %s"
                    self.cursor.execute(update_query, (new_quantity, product_id))
                    self.connection.commit()

                    action_type = "added" if quantity_change >= 0 else "deleted"
                    messagebox.showinfo("Success", f"Quantity {action_type} successfully! New quantity: {new_quantity}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Quantity cannot be negative. Please enter a valid quantity change.")
            else:
                messagebox.showerror("Error", "Product not found. Enter a valid product ID.")

        except Exception as e:
            messagebox.showerror("Error", f"Error updating quantity: {str(e)}")

    ##############################################################################################
    # function to calculate a payment for a specifice date
    def calculate_daily_payment(self):
        try:
            # Get the user input for the specific day
            selected_day = simpledialog.askstring("Select Day",
                                                  "Enter the date (YYYY-MM-DD) to calculate total payment for:")

            # Execute the query to calculate total payment for the specific day
            query = "SELECT SUM(payment) FROM Orders WHERE DATE(date) = %s"
            self.cursor.execute(query, (selected_day,))
            total_payment = self.cursor.fetchone()[0]

            # Display the total payment for the specific day in a message box
            if total_payment is not None:
                messagebox.showinfo("Daily Payment", f"The total payment for {selected_day} is: {total_payment}")
            else:
                messagebox.showinfo("Daily Payment", f"No payment data available for {selected_day}")

        except Exception as e:
            messagebox.showerror("Error", f"Error calculating daily payment: {str(e)}")

    ###################################################################################################################
    # function to View the User informations  how have the maximum number of Order
    def view_max_orders_user_info(self):
        try:
            # Execute the query to get the user(s) with the maximum number of orders
            query = """
                    SELECT User.*, COUNT(Orders.order_id) AS order_count
                    FROM User
                    LEFT JOIN Orders ON User.user_id = Orders.customer_id
                    GROUP BY User.user_id, User.name, User.email, User.address, User.password, User.user_type
                    HAVING order_count = (SELECT MAX(order_count) FROM (SELECT COUNT(order_id) AS order_count FROM Orders GROUP BY customer_id) AS max_orders)
                    ORDER BY order_count DESC
                    """
            self.cursor.execute(query)
            max_orders_user_info = self.cursor.fetchall()

            if max_orders_user_info:
                # Create and display a new window with user information
                window = tk.Toplevel(self.root)
                window.title("Max Orders User Info")

                user_info_label = tk.Label(window, text="User Information with Max Orders", font=('Arial', 16),
                                           foreground="black")
                user_info_label.pack(pady=10)

                for user in max_orders_user_info:
                    user_info_text = f"User ID: {user[0]}\n"
                    user_info_text += f"Name: {user[1]}\n"
                    user_info_text += f"Email: {user[2]}\n"
                    user_info_text += f"Address: {user[3]}\n"
                    user_info_text += f"User Type: {user[5]}\n"
                    user_info_text += f"Order Count: {user[6]}\n"

                    user_info_label = tk.Label(window, text=user_info_text, font=('Arial', 14), foreground="black")
                    user_info_label.pack(pady=10)
            else:
                messagebox.showinfo("Info", "No user information found.")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error viewing max orders user info: {str(e)}")

    #############################################################################################################
    # function to view the Maximum product Boughted from the users
    def view_most_ordered_product_info(self):
        try:
            # Execute the query to get all products with the maximum number of orders
            query = """
                    SELECT Product.*, COUNT(Orders.order_id) AS order_count
                    FROM Product
                    LEFT JOIN Orders ON Product.product_id = Orders.product_id
                    GROUP BY Product.product_id, Product.price, Product.category, Product.quantity 
                    HAVING order_count = (SELECT MAX(order_count) FROM (SELECT COUNT(order_id) AS order_count FROM Orders GROUP BY product_id) AS subquery)
                    ORDER BY order_count DESC
                    """
            self.cursor.execute(query)
            most_ordered_product_info = self.cursor.fetchall()

            if most_ordered_product_info:
                # Create and display a new window with product information
                window = tk.Toplevel(self.root)
                window.title("Most Ordered Product Info")

                product_info_label = tk.Label(window, text="Product Information with Most Orders", font=('Arial', 16),
                                              foreground="black")
                product_info_label.pack(pady=10)

                for product in most_ordered_product_info:
                    product_info_text = f"Product ID: {product[0]}\n"
                    product_info_text += f"Price: {product[1]}\n"
                    product_info_text += f"Category: {product[2]}\n"
                    #product_info_text += f"Order Count: {product[4]}\n"

                    product_info_label = tk.Label(window, text=product_info_text, font=('Arial', 14),
                                                  foreground="black")
                    product_info_label.pack(pady=10)
            else:
                messagebox.showinfo("Info", "No product information found.")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error viewing most ordered product info: {str(e)}")

##############################################################################################################
    def plot_customer_payment_chart(self):
        try:
            # Execute the query to get total payment by each customer
            query = "SELECT customer_id, SUM(payment) FROM Orders GROUP BY customer_id"
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            if data:
                customer_ids = [row[0] for row in data]
                total_payments = [row[1] for row in data]

                # Creating a new figure and plotting the data
                fig, ax = plt.subplots()
                ax.bar(customer_ids, total_payments)
                ax.set(xlabel='Customer ID', ylabel='Total Payment',
                       title='Total Payment by Customer')

                # Embedding the plot in the Tkinter window
                chart_window = tk.Toplevel(self.root)
                chart_window.title("Customer Payments Chart")
                canvas = FigureCanvasTkAgg(fig, master=chart_window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            else:
                messagebox.showinfo("Info", "No data available to plot.")

        except Exception as e:
            messagebox.showerror("Error", f"Error plotting customer payment chart: {str(e)}")


#############################################################################################################
    def plot_category_order_chart(self):
        try:
            # Execute the query to get the number of orders by product category
            query = """
                       SELECT Product.category, COUNT(Orders.order_id)
                       FROM Orders
                       INNER JOIN Product ON Orders.product_id = Product.product_id
                       GROUP BY Product.category
                       """
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            if data:
                categories = [row[0] for row in data]
                counts = [row[1] for row in data]

                # Creating a new figure and plotting the data
                fig, ax = plt.subplots()
                ax.bar(categories, counts)
                ax.set(xlabel='Product Category', ylabel='Number of Orders',
                       title='Number of Orders by Product Category')

                # Embedding the plot in the Tkinter window
                chart_window = tk.Toplevel(self.root)
                chart_window.title("Orders by Category Chart")
                canvas = FigureCanvasTkAgg(fig, master=chart_window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            else:
                messagebox.showinfo("Info", "No data available to plot.")

        except Exception as e:
            messagebox.showerror("Error", f"Error plotting category order chart: {str(e)}")

    ###################################################################################################################
    # [Your other methods here]

######################################################################################################
# cinnection to the DataBase
def UI():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1201319",
            database="online_shope"
        )
        cursor = connection.cursor()

        root = tk.Tk()
        app = AdminGUI(root, connection, cursor)
        root.mainloop()

    finally:
        # Close the connection when the GUI is closed
        if connection.is_connected():
            cursor.close()
            connection.close()