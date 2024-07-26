from db import *
from users import *
from accounts import *
import interface_employee as EMP
import interface_cust as CUST

role = input("Please enter 1 if you are an employee, and 2 if you are a customer.")

# drop_tables()

create_tables()

if role == '1': 

    EMP.main()

elif role == '2': 

    CUST.main()