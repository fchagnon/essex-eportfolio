"""
ShopEase - main.py

Wires together concrete implementations of each layer and runs a
small demo scenario: register a user, add a product, place an order,
generate a sales report.
"""

from models import User, Product, Order
from repositories import InMemoryProductRepository, InMemoryOrderRepository
from notifications import EmailNotifier, SMSNotifier
from payment import StripeProviderFactory
from reporting import SalesReportVisitor, InventoryReportVisitor
from business_logic import UserManager, ProductCatalog, OrderProcessor


def main():
    # 1. Create the repositories (data access layer)
    #    - one InMemoryProductRepository, one InMemoryOrderRepository

    # 2. Create the business logic objects, injecting the repositories
    #    - UserManager (no dependency needed based on its __init__)
    #    - ProductCatalog(product_repository)
    #    - OrderProcessor(order_repository, payment_factory, observers)
    #      note: payment_factory should be a StripeProviderFactory() instance
    #      note: observers should be a list containing an EmailNotifier() and SMSNotifier()

    # 3. Register a user via user_manager.register(...)
    #    - construct a User object first

    # 4. Add a couple of products via product_catalog.add_product(...)
    #    - construct Product objects first, give them different stock levels
    #      (make at least one low enough to
