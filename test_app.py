import unittest
from decimal import Decimal
from app import add_to_cart, total

class StoreTests(unittest.TestCase):
    def setUp(self): self.cart = {}; self.products={"1":{"name":"Book","price":Decimal("5.00"),"stock":2}}
    def test_cart_total(self):
        add_to_cart(self.cart, "1", 2, self.products)
        self.assertEqual(total(self.cart, self.products), Decimal("10.00"))
    def test_stock_limit(self):
        with self.assertRaises(ValueError): add_to_cart(self.cart, "1", 3, self.products)
    def test_unknown_product(self):
        with self.assertRaises(ValueError): add_to_cart(self.cart, "2", 1, self.products)

if __name__ == "__main__": unittest.main()
