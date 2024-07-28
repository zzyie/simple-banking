from sqlalchemy import Column, DECIMAL, String, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates
# from sqlalchemy.exc import ValidationError
# from users import Employee
from db import *
from datetime import date
import random
import string

class Account(Base): 

    # Account is an abstract class

    __abstract__ = True

    def __init__(self, account_num, cust_id):

        self.account_num = account_num
        # print(f"in initial constructor: {account_num}")
        self.cust_id = cust_id
        # print(f"in initial constructor: {cust_id}")
        # self.balance = 0.00
        # self.open_date = date.today()

    # def view_balance(self):
    #     return self.balance

class Checking(Account): 

    __tablename__ = 'checkings'

    id = Column(Integer, primary_key=True)
    account_num = Column(String(10)) # Starts with D, follow by 9 numeric digits
    cust_id = Column(String(10), ForeignKey('customers.user_id'))
    balance = Column(DECIMAL(10, 2))
    int_rate = Column(DECIMAL(5, 5))
    open_date = Column(Date)

    customer = relationship('Customer', back_populates='checking')

    def __init__(self, account_num, cust_id):

        super().__init__(account_num, cust_id)

        # print(f"in checking constructor: {self.account_num}")

        # print(f"in checking constructor: {self.cust_id}")

        self.balance = 0.00

        self.open_date = date.today()

        self.int_rate = 0.001    

    @validates('account_num')
    def validate_account_num(self, key, account_num): 
        
        if len(account_num) != 10: 

            raise Exception("Checking account number must be exactly 10 characters long.")

        if account_num[0] != 'D':

            raise Exception("Checking account number must start with letter D.")
        
        try: 

            int(account_num[1:])
            
        except: 
            
            raise Exception("Checking account number must consists of 9 numerical characters after letter D.")

        return account_num

    @classmethod
    def upsert(cls, session, account_num, cust_id, balance=0.00, int_rate=0.001, update = False): 
        
        instance = session.query(cls).filter_by(account_num=account_num).first()

        # update is boolean flag

        if instance and update:

            instance.acccout_num = account_num

            instance.cust_id = cust_id

            instance.balance = balance

            instance.int_rate = int_rate     

        elif not instance and update: 

            raise Exception("Cannot find existing checking account.")

        else:

            instance = cls(account_num=account_num, cust_id=cust_id)

            session.add(instance)

        session.commit()
    
        return instance

    @classmethod
    def search(cls, session, account_num=None, cust_id = None):
            
        query = session.query(cls)

        if account_num and cust_id: 

            raise Exception("Only support searching by account number or customer ID")

        if account_num:

            query = query.filter_by(account_num=account_num)
        
        if cust_id: 

            query = query.filter_by(cust_id=cust_id)   

        return query.all()
    
    # generate account_number
    @classmethod
    def generate_acct_num(cls):
       
        # Generate five random digits
        digits = ''.join(random.choices(string.digits, k=9))

        random.shuffle(list(digits))
                    
        return 'D' + ''.join(digits)

    # open accounts
    @classmethod
    def new_account(cls, session, cust_id): 

        acct_num = cls.generate_acct_num()

        while len(cls.search(session, acct_num)) > 0: 

            acct_num = cls.generate_acct_num()
        
        new_acct = cls.upsert(session, account_num=acct_num, cust_id=cust_id)

        # print(new_acct.account_num)
        # print(new_acct.cust_id)

        return new_acct   

    def deposit(self, amt, session):

        if amt < 0 : 
            
            print("Negative deposit not allowed")
            return

        self.balance += amt

        Checking.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , update = True)

    # used by an employee to pay interest to accounts at month end
    def pay_interest(self, emp, Employee, session):

        if not isinstance(emp, Employee): 

            raise Exception("Only employee can pay interest to accounts.")

        self.balance *= (1 + self.int_rate/12)

        Checking.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , update = True)

    def withdraw(self, amt, session): 

        if amt < 0: 
            
            print("Negative withdrawal not allowed")    
            return

        if self.balance - amt < 0: 

            print("Insufficient balance.")    
            return

        self.balance -= amt

        Checking.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , update = True)

class Saving(Account):

    __tablename__ = 'savings'

    id = Column(Integer, primary_key=True)
    account_num = Column(String(10)) # Starts with S, follow by 9 numeric digits
    cust_id = Column(String(10), ForeignKey('customers.user_id'))
    balance = Column(DECIMAL(10, 2))
    int_rate = Column(DECIMAL(5, 5))
    open_date = Column(Date)
    withdrawal_limit = Column(Integer)
    withdrawal_count = Column(Integer)

    customer = relationship('Customer', back_populates='saving')

    def __init__(self, account_num, cust_id):

        super().__init__(account_num, cust_id)

        self.balance = 0.00

        self.open_date = date.today()        

        self.int_rate = 0.045        

        self.withdrawal_limit = 20
        
        self.withdrawal_count = 0
    
    @validates('account_num')
    def validate_account_num(self, key, account_num): 
        
        if len(account_num) != 10: 

            raise Exception("Savings account number must be exactly 10 characters long.")

        if account_num[0] != 'S':

            raise Exception("Savings account number must start with letter S.")
        
        try: 

            int(account_num[1:])
            
        except: 
            
            raise Exception("Savings account number must consists of 9 numerical characters after letter S.")

        return account_num

    @classmethod
    def upsert(cls, session, account_num, cust_id, balance=0.00, int_rate=0.045, withdrawal_limit=20, withdrawal_count=0, update = False): 
        
        instance = session.query(cls).filter_by(account_num=account_num).first()

        # update is boolean flag

        if instance and update:

            instance.acccout_num = account_num

            instance.cust_id = cust_id

            instance.balance = balance

            instance.int_rate = int_rate

            instance.withdrawal_limit = withdrawal_limit

            instance.withdrawal_count = withdrawal_count

        elif not instance and update: 

            raise Exception("Cannot find existing saving account.")

        else:

            instance = cls(account_num=account_num, cust_id=cust_id)

            session.add(instance)

        session.commit()
    
        return instance

    @classmethod
    def search(cls, session, account_num=None, cust_id = None):
            
        query = session.query(cls)

        if account_num and cust_id: 

            raise Exception("Only support searching by account number or customer ID")

        if account_num:

            query = query.filter_by(account_num=account_num)
        
        if cust_id: 

            query = query.filter_by(cust_id=cust_id)        

        return query.all()

    # generate account_number
    @classmethod
    def generate_acct_num(cls):
       
        # Generate five random digits
        digits = ''.join(random.choices(string.digits, k=9))

        random.shuffle(list(digits))
                    
        return 'S' + ''.join(digits)

    # open accounts
    @classmethod
    def new_account(cls, session, cust_id): 

        acct_num = cls.generate_acct_num()

        while len(cls.search(session, acct_num)) > 0: 

            acct_num = cls.generate_acct_num()

        new_acct = cls.upsert(session, account_num=acct_num, cust_id=cust_id)

        return new_acct   

    def deposit(self, amt, session):

        if amt < 0 : 
            
            print("Negative deposit not allowed")
            return

        self.balance += amt

        Saving.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , self.withdrawal_limit, self.withdrawal_count, update = True)

    # used by an employee to pay interest to accounts at month end
    def pay_interest(self, emp, Employee, session):

        if not isinstance(emp, Employee): 

            raise Exception("Only employee can pay interest to accounts.")

        self.balance *= (1 + self.int_rate/12)

        Saving.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , self.withdrawal_limit, self.withdrawal_count, update = True)

    def withdraw(self, amt, session): 

        if amt < 0: 
            
            print("Negative withdrawal not allowed")    
            return
        
        if self.withdrawal_count < self.withdrawal_limit: 

            self.balance -= amt

            self.withdrawal_count += 1

            Saving.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , self.withdrawal_limit, self.withdrawal_count, update = True)

        if self.balance - amt < 0: 

            print("Insufficient balance.")    
            return

        else: 
            
            print("Withdrawal limit exceeded") 
            return
        
    # zero out withdrawal count every anniversary 
    def update_withdrawal_ct(self, emp, Employee, session):

        if not isinstance(emp, Employee): 

            raise Exception("Only employee can pay interest to accounts.")

        def check_anni():

            today = date.today()

            return (self.open_date.year < today.year) and (self.open_date.month == today.month) and (self.open_date.date == today.date)
                
        if check_anni():

            self.withdrawal_count = 0

            Saving.upsert(session, self.account_num, self.cust_id, self.balance, self.int_rate , self.withdrawal_limit, self.withdrawal_count, update = True)

def view_accounts(session, cust_id=None, saving=False): 
    
    # return a nested list of checking accounts followed by savings account

    accounts= []

    if not saving:

        accounts += Checking.search(session, cust_id = cust_id)

    accounts += Saving.search(session, cust_id = cust_id)

    return accounts


