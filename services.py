from db import *
from sqlalchemy import Column, DECIMAL, String, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship, validates
from datetime import date
import random
import string

class Service: 

    __abstract__ = True

    def __init__(self, acct_num, cust_id, balance, int_rate): 

        # TODO: value checks
        # TODO: change unncecessary exceptions to print error message and return
        # do not support delinquency
        # quote interest rate in decimals

        self.acct_num = acct_num
        self.cust_id = cust_id
        self.balance = balance
        self.int_rate = int_rate
        self.orig_date = date.today()
   
class Loan(Service):

    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    acct_num = Column(String(15)) # Starts with 0 followed by 9 digits, then a '-', then 4 digits
    cust_id = Column(String(10), ForeignKey('customers.user_id'))
    balance = Column(DECIMAL(10, 2))
    int_rate = Column(DECIMAL(5, 5))
    orig_date = Column(Date)
    term = Column(Integer)
    monthly_payments = Column(DECIMAL(10, 2))
    total_payments = Column(DECIMAL(10, 2))

    customer = relationship('Customer', back_populates='loan')

    # user takes out a loan with interest rate and term specified

    # monthly payments is calculated using interest rate and term, then total payments

    # user makes monthly payments until total payments is zero 

    # payments should be multiple of monthly payments - do not charge late fees

    def __init__(self, acct_num, cust_id, balance, int_rate, term): 

        super.__init__(acct_num, cust_id, balance, int_rate)
        
        self.term = term

        self.monthly_payments = self.balance * (self.int_rate/12) * ((1 + self.int_rate/12)**(term*12)) / (((1 + self.int_rate/12)**(term*12))- 1)

        self.total_payments = self.monthly_payments * 12 * self.term

    @validates('acct_num')
    def validate_acct_num(self, key, acct_num): 
        
        if len(acct_num) != 15: 

            raise Exception("Loan number must be exactly 15 characters long.")

        if acct_num[10] != '-':

            raise Exception("Loan number must have a '-' between obligor and obligation number.")
        
        try: 

            int(acct_num[0:10])
            int(acct_num[11:])
            
        except: 
            
            raise Exception("Loan number must consist of a 10 digit obligor, and '-', then a 4 digit obligation number.")

        return acct_num

    @classmethod
    def upsert(cls, session, acct_num, cust_id, balance, int_rate, term, monthly_payments=None, total_payments=None, update = False): 
        
        instance = session.query(cls).filter_by(acct_num=acct_num).first()

        # update is boolean flag

        if instance and update:

            instance.acct_num = acct_num

            instance.cust_id = cust_id

            instance.balance = balance

            instance.int_rate = int_rate   

            instance.term = term 

            instance.monthly_payments = monthly_payments

            instance.total_payments =  total_payments

        elif not instance and update: 

            raise Exception("Cannot find existing loan.")

        else:

            instance = cls(acct_num=acct_num, cust_id=cust_id, balance=balance, int_rate=int_rate, term=term)

            session.add(instance)

        session.commit()
    
        return instance

    @classmethod
    def search(cls, session, acct_num=None, cust_id=None):
            
        query = session.query(cls)

        if acct_num and cust_id: 

            raise Exception("Only support searching by loan number or customer ID")

        if acct_num:

            query = query.filter_by(acct_num=acct_num)
        
        if cust_id: 

            query = query.filter_by(cust_id=cust_id)   

        return query.all()
    
    # generate loan number
    @classmethod
    def generate_loan_num(cls):
       
        # Generate 9 random digits
        obgor = ''.join(random.choices(string.digits, k=9))

        # generate 2 random digits
        obgat = ''.join(random.choices(string.digits, k=2))

        random.shuffle(list(obgor))
        random.shuffle(list(obgat))
                    
        return '0' + ''.join(obgor) + '-' + '00' + ''.join(obgat)

    # open loan
    @classmethod
    def new_loan(cls, session, cust_id, balance, int_rate, term): 

        acct_num = cls.generate_loan_num()

        while len(cls.search(session, acct_num)) > 0: 

            acct_num = cls.generate_loan_num()
        
        new_loan = cls.upsert(session, acct_num=acct_num, cust_id=cust_id, balance=balance, int_rate=int_rate, term=term)

        # print(new_acct.account_num)
        # print(new_acct.cust_id)

        return new_loan

    def view_montly_pay(self): 

        return self.monthly_payments
    
    def make_monthly_pay(self, session, amt): 

        if amt <= 0: 

            raise ValueError("Negative payment not allowed")

        if amt % self.monthly_payments != 0: 

            raise ValueError("Incorrect payment")
    
        if self.total_payments > 0: 

            self.total_payments -= self.monthly_payments

            Loan.upsert(session, self.acct_num, self.cust_id, self.balance, self.int_rate, self.term, self.monthly_payments, self.total_payments, update = True)
        
class CreditCard(Service): 
    
    __tablename__ = 'creditcards'

    id = Column(Integer, primary_key=True)
    acct_num = Column(String(16)) # Starts 6 digits of BIN, then 10 random
    cust_id = Column(String(10), ForeignKey('customers.user_id'))
    balance = Column(DECIMAL(10, 2))
    int_rate = Column(DECIMAL(5, 5))
    orig_date = Column(Date)
    prev_bal = Column(DECIMAL(10, 2))
    curr_bal = Column(DECIMAL(10, 2))
    int_bal = Column(DECIMAL(10, 2))

    customer = relationship('Customer', back_populates='creditcard')

    # interest rate and credit limit specified

    # once credit limit is fully drawn , no more withdrawal 

    # keep track of spending

    # calculate interest - daily spending * daily rate * days in billing period 
    # pay spending

    def __init__(self, acct_num, cust_id, balance, int_rate): 
        
        super.__init__(acct_num, cust_id, balance, int_rate)

        self.prev_bal = 0

        self.curr_bal = 0

        self.int_bal = 0
    
        # self.running_bal = dict()
        
        # self.running_bal[0] = 0

        # self.last_int_paymt_dt = None

    @validates('acct_num')
    def validate_acct_num(self, key, acct_num): 
        
        if len(acct_num) != 16: 

            raise Exception("Credit card number must be exactly 16 characters long.")

        if acct_num[:6] != '110231':

            raise Exception("Credit Card first six number must be bank ID number.")
        
        try: 

            int(acct_num)
            
        except: 
            
            raise Exception("Credit card number must consist of 16 numerical digits.")

        return acct_num

    @classmethod
    def upsert(cls, session, acct_num, cust_id, balance, int_rate, prev_bal=None, curr_bal=None, int_bal=None, update = False): 
        
        instance = session.query(cls).filter_by(acct_num=acct_num).first()

        # update is boolean flag
        if instance and update:

            instance.acct_num = acct_num

            instance.cust_id = cust_id

            instance.balance = balance

            instance.int_rate = int_rate   

            instance.prev_bal=prev_bal

            instance.curr_bal=curr_bal

            instance.int_bal=int_bal

        elif not instance and update: 

            raise Exception("Cannot find existing loan.")

        else:

            instance = cls(acct_num=acct_num, cust_id=cust_id, balance=balance, int_rate=int_rate)

            session.add(instance)

        session.commit()
    
        return instance

    @classmethod
    def search(cls, session, acct_num=None, cust_id=None):
            
        query = session.query(cls)

        if acct_num and cust_id: 

            raise Exception("Only support searching by credit card number or customer ID")

        if acct_num:

            query = query.filter_by(acct_num=acct_num)
        
        if cust_id: 

            query = query.filter_by(cust_id=cust_id)   

        return query.all()

    # generate credit card number
    @classmethod
    def generate_card_num(cls):
       
        # Generate 9 random digits
        card_num = ''.join(random.choices(string.digits, k=10))

        random.shuffle(list(card_num))
                    
        return '110231' + ''.join(card_num)

    # open loan
    @classmethod
    def new_card(cls, session, cust_id, balance, int_rate): 

        acct_num = cls.generate_card_num()

        while len(cls.search(session, acct_num)) > 0: 

            acct_num = cls.generate_card_num()
        
        new_card = cls.upsert(session, acct_num=acct_num, cust_id=cust_id, balance=balance, int_rate=int_rate)

        # print(new_acct.account_num)
        # print(new_acct.cust_id)

        return new_card
    
    def withdraw(self, session, amt): 

        if amt <= 0: 

            raise ValueError("Negative withdrawal not allowed")     

        if self.balance - amt < 0: 

            raise ValueError("Insufficient funds")

        self.balance -= amt 
        
        self.curr_bal += amt

        CreditCard.upsert(session, self.acct_num, self.cust_id, self.balance, self.int_rate, self.prev_bal, self.curr_bal, self.int_bal, update=True)
        
        # idx = ((date.today() - self.orig_date) // self.bill_period) % 12
    
        # if idx < max(self.running_bal.keys()):

        #     raise ValueError("Balances must be cleared before account anniversary")

        # if self.balance - amt > 0: 

        #     self.balance -= amt  

        #     self.running_bal[idx] += amt
        
        # else: 

        #     raise ValueError("Insufficient funds")

    def charge_month_end_bal(self, session, emp , Employee): 
        
        if not isinstance(emp, Employee): 

            raise Exception("Only employee can charge monthly balance.")

        self.prev_bal += self.curr_bal
        
        self.curr_bal = 0

        CreditCard.upsert(session, self.acct_num, self.cust_id, self.balance, self.int_rate, self.prev_bal, self.curr_bal, self.int_bal, update=True)

    def view_month_end_bal(self): 

        return self.curr_bal

    def pay_balance(self, session, amt): 

        if amt <= 0: 

            raise ValueError("Negative payment not allowed") 

        # if self.prev_bal <= 0: 

        #     raise ValueError("Incorrect payment amount") 
        
        if self.prev_bal - amt < 0: 

            raise ValueError("Incorrect payment amount")

        self.prev_bal -= amt         

        CreditCard.upsert(session, self.acct_num, self.cust_id, self.balance, self.int_rate, self.prev_bal, self.curr_bal, self.int_bal, update=True)   
        
        # running_bal = sum(self.running_bal.values())

        # if running_bal > 0: 

        #     if amt > running_bal: 

        #         raise ValueError("Incorrect payment amount") 

        #     elif amt == running_bal: 

        #         idx = ((date.today() - self.orig_date) // self.bill_period) % 12

        #         self.running_bal=dict()

        #         self.running_bal[idx] = 0

        #     else: 

        #         avail_amt = amt

        #         while avail_amt > 0: 

        #             for i in sorted(self.running_bal.keys()): 

        #                 if avail_amt > self.running_bal[i]: 

        #                     avail_amt -= self.running_bal[i]

        #                     del self.running_bal[i]
                        
        #                 else: 
                            
        #                     self.running_bal[i] -= avail_amt

        #                     avail_amt = 0

        # else: 

        #     raise ValueError("Incorrect payment amount") 

    def charge_month_end_int(self, session, emp, Employee): 

        if not isinstance(emp, Employee): 

            raise Exception("Only employee can charge monthly interest.")            

        self.int_bal += (self.prev_bal) * (1 + self.int_rate / 1200.0)

        CreditCard.upsert(session, self.acct_num, self.cust_id, self.balance, self.int_rate, self.prev_bal, self.curr_bal, self.int_bal, update=True)

    def view_month_end_int(self): 

        return self.int_bal
        
    def pay_interest(self, session, amt): 

        if amt <= 0: 

            raise ValueError("Negative payment not allowed") 
        
        if self.int_bal - amt < 0: 

            raise ValueError("Incorrect payment amount")
        
        self.int_bal -= amt

        CreditCard.upsert(session, self.acct_num, self.cust_id, self.balance, self.int_rate, self.prev_bal, self.curr_bal, self.int_bal, update=True)
        
        # running_bal = sum(self.running_bal.values())

        # if running_bal <= 0: 

        #     raise ValueError("Incorrect payment amount") 
                    
        # idx = ((date.today() - self.orig_date) // self.bill_period) % 12

        # past_balance_idx = sorted(self.running_bal.keys())

        # daily_rate = self.int_rate / 360

        # total_int = 0

        # for i in past_balance_idx: 

        #     if i < (idx - 1): 

        #         total_int += self.running_bal[i] * daily_rate * 30 * (idx - 1 - i)    

        # if total_int == 0: 

        #     raise ValueError("Incorrect payment amount") 
        
        # if 








            

            
            

        

        
        



        

            











        



    
