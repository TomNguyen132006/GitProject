from datetime import datetime

data_format = '%d-%m-%Y'
categories={"I":Income, "Expense": Expense}

def get_date(prompt, allow_default = False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(data_format)
    try:
        valid_date= datetime.strptime(date_str, data_format)
        return valid_date.strftime(data_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)
    
def get_amount():
    try:
        amount= float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be non-negative and non-zero value.")
            return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter for category ('I' for Income or 'E' for Expense):").upper()
    if category in categories:
        return categories[category]

    print("Invalid category. Please enter 'I' for income or 'E' for Expense: ")
    return get_category()   

def get_description():
	return input("Add a description (optional): ")