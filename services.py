from datetime import date

class Service: 

    # svc back populates to customer using cust_id

    def __init__(self, acct_num, cust_id, balance, int_rate): 

        # TODO: value checks
        # do not support delinquency
        # quote interest rate in decimals

        self.acct_num = acct_num
        self.cust_id = cust_id
        self.balance = balance
        self.int_rate = int_rate
        self.orig_date = date.today()
   
class Loan(Service):

    # user takes out a loan with interest rate and term specified

    # monthly payments is calculated using interest rate and term, then total payments

    # user makes monthly payments until total payments is zero 

    # payments should be multiple of monthly payments - do not charge late fees

    def __init__(self, acct_num, cust_id, balance, int_rate, orig_date, term): 

        super.__init__(acct_num, cust_id, balance, int_rate, orig_date)
        
        self.term = term

        self.monthly_payments = self.balance * (self.int_rate/12) * ((1 + self.int_rate/12)**(term*12)) / (((1 + self.int_rate/12)**(term*12))- 1)

        self.total_payments = self.monthly_payments * 12 * self.term

    def monthly_pay(self, amt): 

        if amt <= 0: 

            raise ValueError("Negative payment not allowed")

        if amt % self.monthly_payments != 0: 

            raise ValueError("Incorrect payment")
    
        if self.total_payments > 0: 

            self.total_payments -= self.monthly_payments

class CreditCard(Service): 

    # interest rate and credit limit specified

    # once credit limit is fully drawn , no more withdrawal 

    # keep track of spending

    # calculate interest - daily spending * daily rate * days in billing period 
    # pay spending

        def __init__(self, acct_num, cust_id, balance, int_rate, orig_date): 
            
            super.__init__(acct_num, cust_id, balance, int_rate, orig_date)
            
            self.bill_period = 30

            self.prev_bal = 0

            self.curr_bal = 0

            self.int_bal = 0
        
            # self.running_bal = dict()
            
            # self.running_bal[0] = 0

            # self.last_int_paymt_dt = None
        
        def withdraw(self, amt): 

            if amt <= 0: 

                raise ValueError("Negative withdrawal not allowed")     

            if self.balance - amt < 0: 

                raise ValueError("Insufficient funds")

            self.balance -= amt 
            
            self.curr_bal += amt
            
            # idx = ((date.today() - self.orig_date) // self.bill_period) % 12
        
            # if idx < max(self.running_bal.keys()):

            #     raise ValueError("Balances must be cleared before account anniversary")

            # if self.balance - amt > 0: 

            #     self.balance -= amt  

            #     self.running_bal[idx] += amt
            
            # else: 

            #     raise ValueError("Insufficient funds")

        def charge_month_end_bal(self): 

            self.prev_bal += self.curr_bal
            
            self.curr_bal = 0

        def pay_balance(self, amt): 

            if amt <= 0: 

                raise ValueError("Negative payment not allowed") 

            # if self.prev_bal <= 0: 

            #     raise ValueError("Incorrect payment amount") 
            
            if self.prev_bal - amt < 0: 

                raise ValueError("Incorrect payment amount")

            self.prev_bal -= amt            
            
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

        def charge_month_end_int(self): 

            self.int_bal += (self.prev_bal) * (1 + self.int_rate / 1200.0)
            
            
        def pay_interest(self, amt): 

            if amt <= 0: 

                raise ValueError("Negative payment not allowed") 
            
            if self.int_bal - amt < 0: 

                raise ValueError("Incorrect payment amount")
            
            self.int_bal -= amt

            
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








            

            
            

        

        
        



        

            











        



    
