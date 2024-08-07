from db import *
from services import *
from decimal import Decimal

with next(get_session()) as session: 

    action = 1

    while action != 0: 

        acct_num = input("Please enter credit card number.")

        amt = Decimal(input("Please enter amount to withdraw."))

        CreditCard.withdraw(session, acct_num, amt)

        action = int(input("Enter 1 to continue credit card withdrawal. Enter 0 to exit."))