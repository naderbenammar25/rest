from suds.client import Client

url = 'http://127.0.0.1:8000/bank/soap/?wsdl'
client = Client(url)

# Create a new account
account_data = client.factory.create('Account')
account_data.account_name = 'JohnDoe'
account_data.balance = 1000
response = client.service.create_account(account_data)
print(response)

# Deposit money
transaction_data = client.factory.create('Transaction')
transaction_data.account_name = 'JohnDoe'
transaction_data.amount = 200
transaction_data.transaction_type = 'deposit'
response = client.service.deposit(transaction_data)
print(response)

# Withdraw money
transaction_data.amount = 100
transaction_data.transaction_type = 'withdrawal'
response = client.service.withdraw(transaction_data)
print(response)
