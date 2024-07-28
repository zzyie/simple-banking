from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from accounts import Saving, Checking
from db import *
import random
import string

class User(Base): 

    # User is an abstract base class
    __abstract__ = True

    def __init__(self, first_name, middle_name, last_name, user_id): 
        
        self.first_name = first_name

        self.middle_name = middle_name

        self.last_name = last_name 

        self.user_id = user_id

class Employee(User): 
    
    # table_schema 

    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(7))
    first_name = Column(String)
    middle_name = Column(String, nullable = True)
    last_name = Column(String)

    # cls methods

    def __init__(self, first_name, middle_name, last_name, user_id): 

        super().__init__(first_name, middle_name, last_name, user_id)
        
    @classmethod
    def upsert(cls, session, first_name, middle_name, last_name, user_id, update = False): 
        
        instance = session.query(cls).filter_by(user_id=user_id).first()

        # update is boolean flag

        if instance and update:

            raise Exception("Employee already exists. Do not support employee profile update.")

            # perform update

            # instance.first_name = first_name

            # instance.middle_name = middle_name

            # instance.last_name = last_name

        else:

            instance = cls(first_name = first_name, middle_name = middle_name, last_name = last_name, user_id = user_id)

            session.add(instance)

        session.commit()
    
        return instance

    @classmethod
    def search(cls, session, user_id = None, first_name = None, last_name = None):
            
        query = session.query(cls)

        if user_id:

            query = query.filter_by(user_id = user_id)

        elif first_name and last_name:

            query = query.filter_by(first_name = first_name, last_name = last_name)

        elif not user_id and not first_name and not last_name: 

            pass
        
        else: 

            raise ValueError("Search employee by id or first and last name.")

        return query.all()
    
    @classmethod
    def generate_user_id(cls):
        # Generate one random alphabet
        alphabet = random.choice(string.ascii_uppercase)
        
        # Generate five random digits
        digits = ''.join(random.choices(string.digits, k=6))

        random.shuffle(list(digits))
                    
        return alphabet + ''.join(digits)

    @classmethod
    def check_emp_exists(cls, session, first_name, last_name, user_id): 

        res = cls.search(session, user_id=user_id)

        if len(res) != 1: 

            raise ValueError("Employee ID Error.")

        emp = res[0]

        if  (emp.first_name != first_name) or (emp.last_name != last_name):

            raise Exception("Employee name(s) does not match. Abort.")
            
        return emp
    
    @classmethod
    def new_employee(cls, session, first_name, middle_name, last_name): 

        user_id = cls.generate_user_id()

        while len(cls.search(session, user_id=user_id)) > 0: 

            user_id = cls.generate_user_id()

        new_emp = cls.upsert(session, first_name, middle_name, last_name, user_id)

        return new_emp    


class Customer(User): 

    # table_schema 
    
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(10)) # format: 8 numbers
    first_name = Column(String)
    middle_name = Column(String, nullable = True)
    last_name = Column(String)
    join_date = Column(Date)
    st_address_1 = Column(String)
    st_address_2 = Column(String, nullable = True)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)  # some zipcode starts with 0

    checking = relationship('Checking', back_populates='customer', cascade='all, delete, delete-orphan')
    saving = relationship('Saving', back_populates='customer', cascade='all, delete, delete-orphan')
    loan = relationship('Loan', back_populates='customer', cascade='all, delete, delete-orphan')
    creditcard = relationship('CreditCard', back_populates='customer', cascade='all, delete, delete-orphan')
        
    # class methods

    def __init__(self, first_name, middle_name, last_name, join_date, st_address_1, st_address_2, city, state, zip_code, user_id): 

        super().__init__(first_name, middle_name, last_name, user_id)

        self.join_date = join_date

        self.st_address_1 = st_address_1

        self.st_address_2 = st_address_2

        self.city = city

        self.state = state

        self.zip_code = zip_code 
    
    @classmethod
    def upsert(cls, session, first_name , middle_name , last_name, join_date, st_address_1, st_address_2, city, state, zip_code, user_id , update = False): 
         
        instance = session.query(cls).filter_by(user_id=user_id).first()

        if instance and update:

            # perform update
            raise Exception("Customer already exists. Do not support customer profile update.")

            # instance.first_name = first_name

            # instance.middle_name = middle_name

            # instance.last_name = last_name

            # instance.join_date = join_date

            # instance.st_address_1 = st_address_1

            # instance.st_address_2 = st_address_2

            # instance.city = city

            # instance.state = state

            # instance.zip_code = zip_code

        else:

            instance = cls(first_name = first_name, middle_name = middle_name, last_name = last_name, join_date = join_date, st_address_1 = st_address_1, st_address_2 = st_address_2, city = city, state = state, zip_code = zip_code, user_id = user_id)

            session.add(instance)

        session.commit()
    
        return instance

    @classmethod
    def search(cls, session, user_id = None, first_name = None, last_name = None):
            
        query = session.query(cls)

        if user_id:

            query = query.filter_by(user_id = user_id)

        elif first_name and last_name:

            query = query.filter_by(first_name = first_name, last_name = last_name)

        elif not user_id and not first_name and not last_name: 
            
            pass
        
        else: 
            
            raise ValueError("Search customer by id or first and last name.")
        
        return query.all()

    @classmethod
    def generate_user_id(cls):
        
        # Generate 9 random digits
        digits = ''.join(random.choices(string.digits, k=8))

        random.shuffle(list(digits))
                    
        return ''.join(digits)

    @classmethod
    def check_cust_exists(cls, session, first_name, last_name, user_id): 

        res = cls.search(session, user_id=user_id)

        if len(res) != 1: 

            raise ValueError("Customer ID Error.")

        cust = res[0]

        if  (cust.first_name != first_name) or (cust.last_name != last_name):

            raise Exception("Customer name(s) does not match. Abort.")
            
        return cust
    
    @classmethod
    def new_customer(cls, session, first_name, middle_name, last_name, join_date, st_address_1, st_address_2, city, state, zip_code): 

        user_id = cls.generate_user_id()

        while len(cls.search(session, user_id=user_id)) > 0: 

            user_id = cls.generate_user_id()

        new_cust = cls.upsert(session, first_name, middle_name, last_name, join_date, st_address_1, st_address_2, city, state, zip_code, user_id)

        return new_cust

