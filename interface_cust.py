from users import Customer
from accounts import *
from datetime import date
from db import *
from decimal import Decimal

def show_accounts(session, cust_id): 

    accts = view_accounts(session, cust_id)

    acct_dict = dict()

    if len(accts) == 0: 

        print("Customer has no account on file.")

    else:           
        
        for acct in accts: 

            acct_dict[acct.account_num] = acct

            print(f"Account Number: {acct.account_num}")
            print(f"Balance: {acct.balance}")
            print(f"APR: {acct.int_rate}")
            print(f"Open Date: {acct.open_date}")

            if isinstance(acct, Saving): 
                print(f"Withdrawals per year: {acct.withdrawal_count} / {acct.withdrawal_limit}")

            print("\n")
    
    return acct_dict

def open_new_account(session, cust_id): 

    acct_type = '/'    
    new_account = None

    while acct_type != '0': 
        
        acct_type = input("Would you like to open a savings account (S) or checking account (D)?")

        if acct_type == 'D': 
            
            new_account = Checking.new_account(session, cust_id)
            acct_type = '0'

        elif acct_type == 'S': 

            new_account = Saving.new_account(session, cust_id)
            acct_type = '0'
    
        else: 

            print("Sorry, that isn't one of the choices, please try again.")
            
    print("Account has been successfully created.")
    print(f"Account number: {new_account.account_num}")
    print(f"Open date: {new_account.open_date}")
    print(f"Balance: {new_account.balance}")
    print(f"APR: {new_account.int_rate}")

    if isinstance(new_account, Saving): 
    
        print(f"Withdrawals per year: {new_account.withdrawal_count} / {new_account.withdrawal_limit}")
        
    with open(cust_id + ".txt", "a") as file:

        # Write data to the file
        file.write("\n")
        file.write(f"Account number: {new_account.account_num}\n")
        file.write(f"Open date: {new_account.open_date}\n")
        file.write(f"Balance: {new_account.balance}\n")        
        file.write(f"APR: {new_account.int_rate}\n")
        
        if isinstance(new_account, Saving): 
            
                file.write(f"Withdrawals per year: {new_account.withdrawal_count} / {new_account.withdrawal_limit}")

    return 

def make_deposit(session, acct): 

    prev_balance = acct.balance
    
    amt = Decimal(input("How much would you like deposit into account?"))
                            
    acct.deposit(amt, session)

    print(f"Previous balance: {prev_balance}")
    print(f"Current balance: {acct.balance}")

def make_withdrawal(session, acct): 

    prev_balance = acct.balance
    
    amt = Decimal(input("How much would you like to withdraw from your account?"))
                            
    acct.withdraw(amt, session)

    print(f"Previous balance: {prev_balance}")
    print(f"Current balance: {acct.balance}")

def main(): 

    with next(get_session()) as session: 

        first_name = input("Please enter your first name.")

        last_name = input("Please enter your last name.")

        cust = Customer.search(session, first_name = first_name, last_name = last_name)

        if not cust: 
            
            # print('name match: ' + str(len(emp)))

            print('Setting you up as a new customer...')

            middle_name = input("Please enter your middle name, if applicable.")

            st_address_1 = input("Please enter street address line 1, if applicable.")
            
            st_address_2 = input("Please enter street address line 2, if applicable.")
            
            city = input("Please enter city, if applicable.")
            
            state = input("Please enter state initials, if applicable.")
            
            zip_code = input("Please enter zipcode, if applicable.")

            join_date = date.today()
            
            new_cust = Customer.new_customer(session, first_name, middle_name, last_name, join_date, st_address_1, st_address_2, city, state, zip_code)

            if new_cust: 

                print('New customer set up successfully. Your customer id is: ' + str(new_cust.user_id))

                with open(new_cust.user_id + ".txt", "w") as file:

                    # Write data to the file
                    file.write(f"first_name: {new_cust.first_name}\n")
                    file.write(f"middle_name: {new_cust.middle_name}\n")
                    file.write(f"last_name: {new_cust.last_name}\n")
                    file.write(f"user_id: {new_cust.user_id}\n")
                
            else: 
                
                raise Exception('New customer set up error. Abort')
        
        else: 
            
            user_id = input("Please enter your customer ID.")

            cust = Customer.check_cust_exists(session, first_name, last_name, user_id)

            if cust: 

                print("Welcome back " + cust.first_name)

                # # make dictionary of function to call
                # options = {1: show_accounts}

                choice = 1
                while choice != 0:

                    # menu 
                    print("What would you like to do?")
                    print("1. Manage accounts")
                    print("2. Manage services")
                    print("0. Exit")

                    choice = int(input(">> "))
                    
                    if choice == 1: 

                        acct_dict = show_accounts(session, cust.user_id)

                        if len(acct_dict) == 0: 
                            
                            print("Would you like to open a new account?")
                            
                            open_acct_choice = input("Please enter Y (Yes) or N (No).")

                            if open_acct_choice == "Y": 

                                open_new_account(session, cust.user_id)
                        
                        else: 

                            # make deposit, withdrawal
                            instructions = "Which account would you like to manage? Please enter account number if you would like to manage existing account. \n Enter (O) if you would like to open a new account. \n Enter (X) to return to previous screen."

                            acct_num_input = input(instructions)

                            if acct_num_input == 'O': 

                                open_new_account(session, cust.user_id)

                            elif acct_num_input == 'X': 
                                pass
                            
                            else: 

                                acct = acct_dict[acct_num_input]

                                acct_action_input = input("Would you like to make a deposit (D) or withdrawal (W)?")

                                if acct_action_input == "D": 

                                    make_deposit(session, acct)

                                if acct_action_input == "W": 

                                    make_withdrawal(session, acct)

                    if choice == 2: 
                        
                        pass

                    else: 

                        print("Sorry, that isn't one of the choices, please try again.")
                    

                print("Have a good day. See you soon.")                

            else: 
                
                raise Exception("Customer ID error. Abort.")
            

if __name__ == "__main__":
    
    main()

