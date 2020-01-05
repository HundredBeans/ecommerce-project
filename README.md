# ecommerce-project (TEESIGNR)
## INTRODUCTION
> Teesigner is an E-Commerce that provide a place for anyone who want to sell their design in the form of T-Shirt. Teesigner will cover all the T-Shirt production and Its shipping thingy to the customers. So, sellers won't be experiencing any damnifaction

## FEATURES
* Forgot Password (This will send an E-mail which contains new randomed password for user)
* Email Notification from Teesignr@gmail.com (Gmail API)
* Cart
* Buy without Cart
* Search T-Shirt and Store
* Filter and Sort
* Cancel Order (The order will move into Cart)
* Mocking Gmail API Using Mock.Patch.Object

## Back-End Restful-API
1. Auth Blueprints
   - **POST** /auth/register (register new user with E-mail Notification)
   - **POST** /auth/login (login existing user)
   - **GET** /auth/reset (reset passwort/forgot password with E-mail Notification)
2. Toko Blueprints
   - **POST** /toko/register (register toko with E-mail Notification)
   - **POST** /toko/jual (sell stuff (logged-in))
   - **GET** /toko/cek (check toko info for user (logged-in))
   - **GET** /toko (list of toko, with 1 of their popular items)
   - **GET** /toko/<id> (show toko info with specific id)
   - **GET** /toko (list of toko with filter)
   - **PUT** /toko/edit (edit toko name and description)
   - **DELETE** /toko/edit (delete items from user's toko (logged-in))
3. Baju/Barang Blueprints
   - **GET** /baju (show all items and can be filtered or searched)
   - **GET** /baju/<id> (show item with specific id)
   - **PUT** /baju/<id> (add item with specific id to cart (logged-in))
   - **PATCH** /baju/<id> (buy item with specific id without putting it into cart (logged-in))
4. Keranjang Blueprints
   - **GET** /keranjang (show all items in cart)
   - **PUT** /keranjang (edit item in cart)
   - **DELETE** /keranjang (remove item/s from cart)
   - **PATCH** /keranjang (checkout item/s into transaction)
5. Checkout Blueprints
   - **DELETE** /checkout (Cancel order and withdraw it into cart (logged-in))
   - **POST** /checkout (confirm those order by fill out shipping details and get the detail transaction sent via E-mail (logged-in))
   - **GET** /checkout (show all order item that has been checked-out (logged-in))
6. User Blueprints
   - **PATCH** /user/edit (Change password for user (logged-in))
   - **GET** /user (show user info such as store and history of transactions)
