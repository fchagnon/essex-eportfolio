# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email


class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def accept(self, visitor):
        """
        Visitor pattern hook. Calls the appropriate visit_product()
        method on the passed visitor, passing self. This is what lets
        ReportVisitor implementations operate on Product without Product
        needing to know anything about reporting.
        """
        return visitor.visit_product(self)
  
class Order:
    def __init__(self, order_id, user, items):
        """
        items: list of (Product, quantity) tuples
        """
        self.order_id = order_id
        self.user = user
        self.items = items

    def accept(self, visitor):
        """
        Visitor pattern hook. Calls the appropriate visit_product()
        method on the passed visitor, passing self.
        """
        return visitor.visit_order(self)

    def total(self):
        """
        Returns the total price of the order (sum of product.price * qty
        for each item). No discount logic here - that's Strategy's job
        elsewhere, keep this method single-purpose.
        """
        total = 0
        for product, quantity in self.items:
            total += product.price * quantity
        return total
