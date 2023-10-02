Ecommerence Project

This project includes following endspoints.

    * User
        In user, i provide two endpoints.
        * signup & Login:
            User first register ourself, and then use the Login endspoints to validate the user and generate a token to authorize the user.afetr this user access all the endpoints.

    * Products:
        In products,  user can add new products.
        and use all crud operation in thats belongs to use.
        

    * Inventory:
        In inventory, user can add  in stock of the product.
        and use primary key of product as an forign key.
        use all crud operation in thats belongs to use.

    * Products Sales:
        In product sales, user can check the sales and revenu of the specific product in a specific time periods (daily, weekly, monthly, annual). peoduct ud use as an forign key. 


RUN THE PROJECTS:

    1- FIrst install the  requirements.txt file.
        " pip install -r .\\requirements.txt "

    2- Run the server with this command:
        " uvicorn main:app --reload "





