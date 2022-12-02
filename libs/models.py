'''
Here you will create the class or classes
that refer to the tables in the database.
'''
import db
from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import date


class Product(db.Base):
    '''
    This class is associated to the products
    table of the customer_transaction
    '''
    # Name of the associated table
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String)
    product_line = Column(String)
    product_class = Column(String)
    product_size = Column(String)
    transactions_products = relationship('Transaction')

    def __init__(
        self, product_id: int, brand: str, product_line: str,
        product_class: str, product_size: str
            ) -> None:
        # Method constructor of class
        self.product_id = product_id
        self.brand = brand
        self.product_line = product_line
        self.product_class = product_class
        self.product_size = product_size

    def __repr__(self):
        # Overwriting repr, to represent the following.
        return f'Product ({self.product_id}, {self.brand})'

    def __str__(self):
        # Overwriting str, to show this class name.
        return self.brand


class Customer(db.Base):
    '''
    This class is associated to the current_customers
    table table of the customer_transaction
    '''
    # Name of the associated table
    __tablename__ = 'current_customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    gender = Column(String)
    past_3_years_bike_related_purchases = Column(Integer)
    birth_date = Column(Date)
    age = Column(Float)
    job_title = Column(String)
    job_industry_category = Column(String)
    wealth_segment = Column(String)
    deceased_indicator = Column(String)
    owns_car = Column(Boolean)
    tenure = Column(Float)
    address = Column(String)
    postcode = Column(Integer)
    state = Column(String)
    country = Column(String)
    property_valuation = Column(Integer)
    transactions_customers = relationship('Transaction')

    def __init__(
        self, customer_id: int, name: str, gender: str,
        past_3_years_bike_related_purchases: int, birth_date: date, age: float,
        job_title: str, job_industry_category: str, wealth_segment: str,
        deceased_indicator: str, owns_car: bool, tenure: float, address: str,
        postcode: int, state: str, country: str, property_valuation: int
            ) -> None:
        # Method constructor of class
        self.customer_id = customer_id
        self.name = name
        self.gender = gender
        self.past_3_years_bike_related_purchases = \
            past_3_years_bike_related_purchases
        self.birth_date = birth_date
        self.age = age
        self.job_title = job_title
        self.job_industry_category = job_industry_category
        self.wealth_segment = wealth_segment
        self.deceased_indicator = deceased_indicator
        self.owns_car = owns_car
        self.tenure = tenure
        self.address = address
        self.postcode = postcode
        self.state = state
        self.country = country
        self.property_valuation = property_valuation

    def __repr__(self):
        # Overwriting repr, to represent the following.
        return f'Current Customer ({self.customer_id}, {self.name})'

    def __str__(self):
        # Overwriting str, to show this class name.
        return self.name


class NewCustomer(db.Base):
    '''
    This class is associated to the target_customers
    table table of the customer_transaction
    '''
    # Name of the associated table
    __tablename__ = 'target_customers'

    target_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    past_3_years_bike_related_purchases = Column(Integer)
    birth_date = Column(Date)
    job_title = Column(String)
    job_industry_category = Column(String)
    wealth_segment = Column(String)
    deceased_indicator = Column(String)
    owns_car = Column(Boolean)
    tenure = Column(Float)
    address = Column(String)
    postcode = Column(Integer)
    state = Column(String)
    country = Column(String)
    property_valuation = Column(Integer)

    def __init__(
        self, target_id: int, first_name: str, last_name: str, gender: str,
        past_3_years_bike_related_purchases: int, birth_date: date,
        job_title: str, job_industry_category: str, wealth_segment: str,
        deceased_indicator: str, owns_car: bool, tenure: float, address: str,
        postcode: int, state: str, country: str, property_valuation: int
            ) -> None:
        # Method constructor of class
        self.target_id = target_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.past_3_years_bike_related_purchases = \
            past_3_years_bike_related_purchases
        self.birth_date = birth_date
        self.job_title = job_title
        self.job_industry_category = job_industry_category
        self.wealth_segment = wealth_segment
        self.deceased_indicator = deceased_indicator
        self.owns_car = owns_car
        self.tenure = tenure
        self.address = address
        self.postcode = postcode
        self.state = state
        self.country = country
        self.property_valuation = property_valuation

    def __repr__(self):
        # Overwriting repr, to represent the following.
        return f'New Customer ({self.first_name}, {self.last_name})'

    def __str__(self):
        # Overwriting str, to show this class name.
        return self.first_name + ' ' + self.last_name


class Transaction(db.Base):
    '''
    This class is associated to the transactions
    table table of the customer_transaction
    '''
    # Name of the associated table
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('current_customers.customer_id'))
    transaction_date = Column(Date)
    online_order = Column(Boolean)
    order_status = Column(String)
    list_price = Column(Float)
    standard_cost = Column(Float)
    product_first_sold_date = Column(Float)
    product_id = Column(Integer, ForeignKey('products.product_id'))

    def __init__(
        self, transaction_id: int, customer_id: int, transaction_date: date,
        online_order: bool, order_status: str, list_price: float,
        standard_cost: float, product_first_sold_date: float,
        product_id: int
            ) -> None:
        # Method constructor of class
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.transaction_date = transaction_date
        self.online_order = online_order
        self.order_status = order_status
        self.list_price = list_price
        self.standard_cost = standard_cost
        self.product_first_sold_date = product_first_sold_date
        self.product_id = product_id

    def __repr__(self):
        # Overwriting repr, to represent the following.
        return f'Transaction ({self.transaction_id})'
