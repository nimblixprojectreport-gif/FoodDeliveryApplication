# QuickBite Frontend

React frontend connected to your Django food delivery backend.

## Setup

```bash
npm install
npm run dev   # opens http://localhost:3000
```

Your Django backend must be running on `http://127.0.0.1:8000`.
Vite automatically proxies all `/api/v1/...` calls to it.

## Role-Based Routing

| Role       | Home after login    | Pages                                         |
|------------|---------------------|-----------------------------------------------|
| CUSTOMER   | `/home`             | Browse restaurants, view menu, cart, checkout, orders, review |
| RESTAURANT | `/restaurant`       | Dashboard, manage menu items, update order status |
| DELIVERY   | `/delivery`         | See available orders, accept, update delivery status, history |

## Auth Flow

1. Register with username + password + role
2. Login → receives DRF Token → stored in localStorage as `qb_token`
3. All API calls send `Authorization: Token <token>` header
4. On logout → token deleted from server + localStorage

## API Endpoints Used (exact Django URLs)

```
POST /api/v1/users/register/          Register new user
POST /api/v1/users/login/             Login → returns { token }
POST /api/v1/users/logout/            Logout (deletes token)
GET  /api/v1/users/profile/           Get logged-in user profile

GET  /api/v1/restaurants/             List all approved restaurants
GET  /api/v1/restaurants/<id>/        Restaurant detail + menu
GET  /api/v1/restaurants/<id>/menu/   Menu items for restaurant
POST /api/v1/restaurants/register/    Create restaurant (RESTAURANT role)
GET  /api/v1/restaurants/manage/      Owner's own restaurant
POST /api/v1/restaurants/menu/items/add/     Add menu item
PUT  /api/v1/restaurants/menu/items/<id>/    Update menu item
DEL  /api/v1/restaurants/menu/items/<id>/    Delete menu item

GET  /api/v1/orders/cart/             Get cart
POST /api/v1/orders/cart/             Add item to cart { menu_item_id, quantity }
DEL  /api/v1/orders/cart/items/<id>/  Remove cart item
DEL  /api/v1/orders/cart/             Clear cart
POST /api/v1/orders/checkout/         Place order { delivery_address }
GET  /api/v1/orders/                  My orders list
POST /api/v1/orders/<id>/cancel/      Cancel order
PUT  /api/v1/orders/<id>/update-status/  Update order status

GET  /api/v1/delivery/status/                     My deliveries
POST /api/v1/delivery/status/                     Update availability/location
GET  /api/v1/delivery/orders/available/           Available orders to accept
POST /api/v1/delivery/orders/<id>/accept/         Accept order
POST /api/v1/delivery/<pk>/status/                Update delivery status

POST /api/v1/reviews/                 Submit review { order_id, rating, comment }
GET  /api/v1/notifications/           My notifications
```

## File Structure

```
src/
├── api/index.js              ← All API calls to Django
├── context/index.jsx         ← AuthContext + ToastContext
├── components/Navbar.jsx     ← Role-aware navbar
├── pages/
│   ├── Auth.jsx              ← Login + Register (shared)
│   ├── Profile.jsx           ← Profile (all roles)
│   ├── customer/
│   │   ├── Home.jsx          ← Restaurant listing
│   │   ├── RestaurantDetail.jsx  ← Menu + Cart + Checkout
│   │   └── Orders.jsx        ← My orders + Cancel + Review
│   ├── restaurant/
│   │   ├── Dashboard.jsx     ← Restaurant info + incoming orders
│   │   └── Menu.jsx          ← Add/Edit/Delete menu items
│   └── delivery/
│       ├── Dashboard.jsx     ← Available orders + Accept + Status
│       └── History.jsx       ← Completed deliveries
├── styles/globals.css        ← Navy blue theme
└── App.jsx                   ← Router + role-based guards
```
