import json
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

PRODUCTS = {
    "1": {"name": "Notebook", "price": Decimal("1500.00"), "stock": 10},
    "2": {"name": "Pen", "price": Decimal("300.00"), "stock": 25},
    "3": {"name": "Backpack", "price": Decimal("8500.00"), "stock": 5},
}
ORDERS = Path(__file__).with_name("orders.json")

def total(cart, products=PRODUCTS):
    return sum((products[pid]["price"] * qty for pid, qty in cart.items()), Decimal("0.00"))

def add_to_cart(cart, product_id, quantity, products=PRODUCTS):
    if product_id not in products: raise ValueError("Unknown product")
    if quantity <= 0: raise ValueError("Quantity must be positive")
    if cart.get(product_id, 0) + quantity > products[product_id]["stock"]:
        raise ValueError("Not enough stock")
    cart[product_id] = cart.get(product_id, 0) + quantity

def checkout(cart, customer, products=PRODUCTS):
    if not cart: raise ValueError("Cart is empty")
    if not customer.strip(): raise ValueError("Customer name required")
    for pid, qty in cart.items():
        if qty > products[pid]["stock"]: raise ValueError("Not enough stock")
    amount = total(cart, products)
    order = {"id": uuid4().hex[:10], "customer": customer.strip(), "items": dict(cart),
             "total": str(amount), "status": "pending_payment"}
    existing = json.loads(ORDERS.read_text(encoding="utf-8")) if ORDERS.exists() else []
    existing.append(order)
    ORDERS.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    for pid, qty in cart.items(): products[pid]["stock"] -= qty
    cart.clear()
    return order

def main():
    cart = {}
    print("Online Store Demo (no real payments)")
    while True:
        print("\n1 Products  2 Add to cart  3 View cart  4 Checkout  5 Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            for pid, item in PRODUCTS.items():
                print(pid, item["name"], "₦" + str(item["price"]), "Stock:", item["stock"])
        elif choice == "2":
            try:
                pid = input("Product ID: ").strip()
                qty = int(input("Quantity: "))
                add_to_cart(cart, pid, qty)
                print("Added")
            except ValueError as exc: print("Error:", exc)
        elif choice == "3": print("Cart:", cart, "Total: ₦" + str(total(cart)))
        elif choice == "4":
            try: print("Order created:", checkout(cart, input("Customer name: ")))
            except ValueError as exc: print("Error:", exc)
        elif choice == "5": break
        else: print("Invalid choice")

if __name__ == "__main__": main()
