
from users import Employee, Customer
from accounts import *
from services import *
from db import *
import logging

def show_accounts(session): 

    accts = view_accounts(session)

    # acct_dict = dict()

    if len(accts) == 0: 

        print("No accounts.")

    else:           
        
        for acct in accts: 

            # acct_dict[acct.account_num] = acct

            print(f"Account Number: {acct.account_num}")
            print(f"Account owner: {acct.cust_id}")
            print(f"Balance: {acct.balance}")
            print(f"APR: {acct.int_rate}")
            print(f"Open Date: {acct.open_date}")

            if isinstance(acct, Saving): 
                print(f"Withdrawals per year: {acct.withdrawal_count} / {acct.withdrawal_limit}")

            print("\n")
    
    # return acct_dict

def pay_interest(session, emp, Employee): 

    accts = view_accounts(session)

    if len(accts) == 0: 

        print("No accounts.")

    for acct in accts: 

        print(f"Account Number: {acct.account_num}")
        print(f"Previous Balance: {acct.balance}")
        acct.pay_interest(emp, Employee, session)
        print(f"Current Balance: {acct.balance}")
        logging.info(f"Paid interest for account {acct.account_num}")

def update_withdrawal_count(session, emp, Employee): 

    accts = view_accounts(session, saving=True)

    if len(accts) == 0: 

        print("No saving accounts.")

    for acct in accts: 

        print(f"Account Number: {acct.account_num}")
        print(f"Previous Withdrawal Count: {acct.withdrawal_count}")
        acct.update_withdrawal_ct(emp, Employee, session)
        print(f"Previous Withdrawal Count: {acct.withdrawal_count}")
        logging.info(f"Updated withdrawal count for account {acct.account_num}")

def show_services(session): 

    services = view_services(session)

    if len(services) == 0: 

        print("No services.")

    else:           
        
        for svc in services: 

            print(f"Service number: {svc.acct_num}")
            print(f"Origination date: {svc.orig_date}")
            print(f"Balance: {svc.balance}")
            print(f"APR: {svc.int_rate}")

            if isinstance(svc, Loan): 
                print(f"Term: {svc.term}")

            print("\n")

def charge_credit_cards(session, emp, Employee): 

    cards = view_services(session, creditCard=True)

    if len(cards) == 0: 

        print("No credit cards.")
        
    else: 

        for card in cards: 
            
            print(f"Service number: {card.acct_num}")
            print(f"Previous balance: {card.prev_bal}")
            print(f"Current balance: {card.curr_bal}")
            print(f"Current interest: {card.int_bal}")
            print("After charging...")
            card.charge_month_end_bal(session, emp, Employee)
            card.charge_month_end_int(session, emp, Employee)
            print(f"Previous balance: {card.prev_bal}")
            print(f"Current balance: {card.curr_bal}")
            print(f"Current interest: {card.int_bal}")
            print("\n")

            logging.info(f"Charged credit card {card.acct_num}")

def main(): 

    with next(get_session()) as session: 

        first_name = input("Please enter your first name.")

        last_name = input("Please enter your last name.")

        emp = Employee.search(session, first_name = first_name, last_name = last_name)

        if not emp: 
            
            # print('name match: ' + str(len(emp)))

            print('Setting you up as a new employee...')

            middle_name = input("Please enter your middle name, if applicable.")
            
            new_emp = Employee.new_employee(session, first_name, middle_name, last_name)

            if new_emp: 

                print('New employee set up successfully. Your employee id is: ' + str(new_emp.user_id))

                with open(new_emp.first_name + '_' + new_emp.last_name + ".txt", "w") as file:

                    # Write data to the file
                    file.write("middle_name: " + new_emp.middle_name)
                    file.write("\n")
                    file.write("user_id: " + new_emp.user_id)
                
            else: 
                
                raise Exception('New employee set up error. Abort')
        
        else: 
            
            # for i in emp: 
            #     print(i.first_name)
            #     print(i.middle_name)
            #     print(i.last_name)
            #     print(i.user_id)

            user_id = input("Please enter your employee ID.")

            # res = Employee.search(session, user_id = user_id))

            # session.delete(session.query(Employee).filter_by(id=1).first())
            # session.commit()

            # print("deleted.")

            emp = Employee.check_emp_exists(session, first_name, last_name, user_id)

            if emp: 

                print("Welcome back " + emp.first_name)

            else: 
                
                raise Exception("Employee ID error. Abort.")
            
            choice = 1
            while choice != 0:

                # menu 
                print("What would you like to do?")
                print("1. Manage accounts.")
                print("2. Manage services.")
                print("0. Exit")

                choice = int(input(">> "))

                if choice == 1: 

                    account_action = 1

                    while account_action != 0:

                        print("1. View accounts.")
                        print("2. Deposit interest to all accounts.")
                        print("3. Update withdrawal counts for saving accounts.")
                        print("0. Exit")

                        account_action = int(input(">> "))

                        if account_action == 1: 

                            show_accounts(session)

                        elif account_action == 2:

                            pay_interest(session, emp, Employee)

                        elif account_action == 3:

                            update_withdrawal_count(session, emp, Employee)

                        elif account_action == 0: 

                            pass

                        else: 

                            print("Sorry, that isn't one of the choices, please try again.")
                
                elif choice == 2: 

                    while svc_action != 0:

                        print("1. View services.")
                        print("2. Charge credit cards.")
                        print("0. Exit")

                        svc_action = int(input(">> "))

                        if svc_action == 1: 

                            show_services(session)

                        elif svc_action == 2:

                            charge_credit_cards(session, emp, Employee)

                        elif svc_action == 0: 

                            pass

                        else: 

                            print("Sorry, that isn't one of the choices, please try again.")

                elif choice == 0: 

                    pass

                else: 

                    print("Sorry, that isn't one of the choices, please try again.")

if __name__ == "__main__":
    
    main()

