import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from get_data import get_date, get_amount, get_category, get_description

class CSV:
    CSV_file = "finance_data.csv"
    columns = ["date","amount","category", "description"]
    format= '%d-%m-%Y'

    @classmethod
    def initialize(cls):
        try:
            pd.read_csv(cls.CSV_file)

        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns)
            df.to_string(cls.CSV_file, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'date' : date,
            'amount' :amount,
            'category': category,
            'description' :description
        }   
        with open(cls.CSV_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writerow(new_entry)
        print("Enter added successfully")

    @classmethod 
    def get_transaction(cls, start_date, end_date):
        df= pd.read_csv(cls.CSV_file)
        df["date"] = pd.to_datetime(df["date"], format= CSV.format)
        start_date = datetime.strptime(start_date, CSV.format)
        end_date = datetime.strptime(end_date, CSV.format)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction found.")
        else:
            print(f"transaction from {start_date.strftime(CSV.format)} to {end_date.strftime(CSV.format)}")
            print(filtered_df.to_string(index=False, formatters={'date' : lambda x : x.strftime(CSV.format)}))

            total_income = filtered_df[filtered_df['category']=='Income']['Amount'].sum()
            total_expense = filtered_df[filtered_df['category']=='Expense']['Amount'].sum()

            print('\nSummary.')
            print(f"Total income: ${total_income:.2f}")
            print(f"Total expense: ${total_expense:.2f}")
            print(f"Net saving : ${total_income - total_expense:.2f}")
        return filtered_df

    @classmethod
    def delete_transaction(cls):
        try:
            df=pd.read_csv(cls.CSV_file)
            if df.empty:
                print('No transaction found.')
                return
            print('\nAll transactions.')
            print(df.to_string(index=True))

            while True:
                try:
                    index_delete = int(input('Enter the number of transaction to delete: '))
                    if index_delete in df.index:
                        break
                    else:
                        print("Invalid number. Please try again")
                except ValueError:
                    print('Please enter a valid number.')

            print(df.loc[index_delete].to_string())
            confirm = input("Are you sure you want to delete this transaction?('Y' for Yes, 'N' for No)  ").upper()

            if confirm == 'Y':
                df.drop(index=index_delete, inplace=True)
                df.to_csv(cls.CSV_file,index=False)
                print("Transaction deleted successfully.")
            else:
                print('Cancelled.')

        except FileNotFoundError:
            print('The data file does not exisst. Please add transaction first.')
        except PermissionError:
            print("Permission denied. Make sure the file is not open in another program.")
        except Exception as e:
            print(f"an error occured: {e}")

def add():
    CSV.initialize_csv()
    date = get_date("PLease type in the date of the transaction (dd-mm-yyyy) or press enter fo today's date: ",allow_default= True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)


def plot_transaction(df):
    df.set_index('date',inplace = True)

    income_df= df[df['category']=="Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df= df[df['category']=="Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")	
    plt.title("Income and Expense")
    plt.grid(True)
    plt.show()

def main():
	while True:
		print("\n1. Add a new transaction")
		print("\n2. View transaction and summary within a date range")
		print("\n3. Delete a transaction")
		print("\n4. Exit")
		choice = input("Enter your choice(1-4): ")

		if choice == "1":
			add()

		elif choice == "2":
			start_date = get_date("Enter the start date (dd-mm-yyyy): ")
			end_date = get_date("Enter the end date (dd-mm-yyyy): ")
			df = CSV.get_transaction(start_date,end_date)
			if input("Do you want to see a plot? (y/n): ").lower() == "y":
				plot_transaction(df)

		elif choice == "3":
			CSV.delete_transaction()

		elif choice == "4":
			print("Exiting...")
			break

		else:
			print("Invalid choice.Enter 1, 2, 3 or 4.")




if __name__ == "__main__":
	main()



        