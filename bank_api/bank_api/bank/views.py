from sqlite3 import Date
from django.shortcuts import render

from spyne import Application, rpc, ServiceBase, ComplexModel, Unicode, Decimal
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class Account(ComplexModel):
    account_name = Unicode
    balance = Decimal

class Transaction(ComplexModel):
    account_name = Unicode
    rib = Unicode
    amount = Decimal
    transaction_type = Unicode  # Can be 'deposit' or 'withdraw'
    creationDate = Date


class BankService(ServiceBase):
    @rpc(Account, _returns=Unicode)
    def create_account(ctx, account):
        # create account
        return f"Account {account.account_name} created with balance {account.balance}"

    @rpc(Transaction, _returns=Unicode)
    def deposit(ctx, transaction):
        # deposit money
        return f"Deposited {transaction.amount} to {transaction.account_name}"

    @rpc(Transaction, _returns=Unicode)
    def withdraw(ctx, transaction):
        # withdraw money
        return f"Withdrew {transaction.amount} from {transaction.account_name}"

application = Application([BankService],
                          tns='bank.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
django_app = DjangoApplication(application)
soap_app = csrf_exempt(django_app)

def soap_service(request):
    return HttpResponse(soap_app(request))
