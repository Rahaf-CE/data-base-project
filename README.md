🛍️ Online Bag Shop System (Python + Tkinter + MySQL)

📌 Overview
This is a desktop-based online shopping system developed using Python, Tkinter, and MySQL. The system supports two types of users: Admin and Customer, and offers a fully functional interface for managing products, placing orders, and tracking user data. The database backend ensures persistent storage of users, products, and orders.

🧑‍💼 Admin Features
Admins can:

📦 View all products

📄 View all orders

🧾 View users with the highest number of orders

💰 View orders with maximum payment

📊 Plot customer payments and category-based order charts

🔄 Update product quantities

💵 Calculate total and daily payments

📈 Identify most ordered products

🛒 Customer Features
Customers can:

👤 Sign up / Log in securely

👜 Browse and select bags by category (Laptop, Hand, Back bags)

🖼️ View product images and prices

🛍️ Place orders and confirm payment

❌ Cancel previously placed orders

🔑 Recover forgotten passwords

💾 Tech Stack
Component	Technology
Frontend	Tkinter (Python GUI)
Backend	MySQL
ORM	MySQL Connector
Visualization	Matplotlib
Image Handling	PIL (Pillow)

🗃️ Database Structure
User Table: user_id, name, email, address, password, user_type

Product Table: product_id, price, category, quantity, images

Orders Table: order_id, customer_id, product_id, date, payment

All CRUD operations are performed with appropriate error handling and validations.

🖼️ UI Highlights
💅 Clean and user-friendly design using Tkinter styling

🎨 Background colors, buttons, and labels match a cohesive pink/purple/yellow theme

📈 Real-time plots with Matplotlib embedded in GUI

🕒 Time display using Roman numerals for enhanced aesthetic

🚀 How to Run
✅ Make sure MySQL is installed and running on your system

🛠️ Create a MySQL database named online_shope and import the required tables (User, Product, Orders)

🧾 Install the required Python libraries:

bash
Copy
Edit
pip install mysql-connector-python pillow matplotlib
📷 Place your product images inside the project folder and ensure the images column in the database stores correct paths

🏃 Run the Python script:

bash
Copy
Edit
python main.py

📌 Future Improvements
🔐 Add password hashing and authentication

🧾 Add invoices and PDF receipts generation

🌐 Convert to web-based version using Flask or Django

📱 Mobile-friendly interface using Kivy or React Native

🗃️ Add product review system and rating

💬 Acknowledgements
This project was developed as part of a course assignment to demonstrate practical skills in GUI design, database integration, and full-stack application development in Python.
