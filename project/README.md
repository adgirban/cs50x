# VAPIFY

#### Video Demo: 
https://www.youtube.com/watch?v=LZ1ur_ne55I

#### Description: 
This is an ecommerce website implemented with HTML, CSS, Python(Flask) and SQL. It functions as a website for only buying vapes. The buying isn't real as the ecommerce website is just a gimmick without the vapes but it ensures to store the payments in a database so that if the website comes alive then the payment API could be connected accordingly. Feel free to provide your suggestions or any bugs that I may have missed.

In helpers.py: I have used the helpers.py from the last problem set of week 10 in order to use the apology function for error handling. 

In vapes.db: The database contains 4 different tables namely: 
vape - stores all the vapes available in the store, 
users - keeps track of registered, non-registered and logged in users, 
cart - keeps track of items in cart for a particular user, 
payment - keeps record of the payment information provided by the buyer. 
Earlier in the project, I decided to implement as much as everything within the python logic but it was quite difficult. Then, I decided to use sqlite3 but it was quite difficult to use. The queries couldn't be written normally. The arguments were always limited. Then again, I decided to use the cs50 library only after which my development time sky rocketed. These tables have made life so much easier inside app.py. 

In templates: There are 7 templates: 
layout - main template, 
index - home page, 
login - name suggests, 
register - name suggests, 
cart - displays cart, 
pay - displays payment form, 
apology - error handling meme. 

In images: The images have been extracted from google with all being in .webp format as the quality of the picture is better with better refresh rates. 

For bootstrap: The grids in bootstrap allowed me to design the index page and the container allowed me to design the navigation panel.

For fontawesome: The logo for shopping cart has been used from fontawesome as they provide free and easy use of such png logos by only a including a class in a tag.

In the beginning of the project, I decided to use my own design for everything but found out it was too tedious for a single person. Then, I decided to use the Pset10's layout and format which made things a litle easier.

FEATURES:

1. User Authentication
User Registration: Users can create an account on Vapify by providing essential information.
User Login: Registered users can log in securely to access their accounts and make purchases.

2. Product Catalog
Browse Products: Explore a diverse catalog of vape products, including e-liquids, devices, and accessories.
Product Details: Each product page provides detailed information, pricing, and customer reviews.

Shopping Cart
Add to Cart: Users can add their desired products to the shopping cart for a convenient checkout experience.
Adjust Quantities: Easily modify product quantities or remove items from the shopping cart.

4. Checkout Process
Secure Checkout: Vapify ensures a secure and smooth checkout process for users.
Address Management: Users can add, edit, or delete shipping addresses for a personalized shopping experience.

TECHNOLOGIES USED:
Frontend: HTML, CSS, JavaScript, Bootstrap
Backend: Flask (Python)
Database: SQLite
Authentication: Flask-Login
ORM: Flask-SQLAlchemy

HOW TO RUN:
Clone the repository
Navigate to the project directory
Install dependencies: pip install library_name
Run the application: python app.py
Access the application in your web browser: http://localhost:xxxx

CONTRIBUTION:
Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.
