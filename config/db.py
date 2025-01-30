import os
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)
MONGO_URL = os.getenv("MONGO_URL")

def NatWest():
    return {
    "CLIENT_ID": os.getenv("NATWEST_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("NATWEST_CLIENT_SECRET"),
    "REDIRECT_URI": os.getenv("NATWEST_REDIRECT_URI"),
    "AUTHORIZATION_USERNAME": os.getenv("NATWEST_AUTHORIZATION_USERNAME"),
    "TOKEN_URL": "https://ob.sandbox.natwest.com/token",
    "AUTH_URL": "https://api.sandbox.natwest.com/authorize",
    "API_BASE_URL": "https://ob.sandbox.natwest.com/open-banking/v3.1/aisp",
    }

def RBS():
    return {
        "CLIENT_ID": os.getenv("RBS_CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("RBS_CLIENT_SECRET"),
        "REDIRECT_URI": os.getenv("RBS_REDIRECT_URI"),
        "AUTHORIZATION_USERNAME": os.getenv("RBS_AUTHORIZATION_USERNAME"),
        "TOKEN_URL": "https://ob.sandbox.rbs.co.uk/token",
        "AUTH_URL": "https://api.sandbox.rbs.co.uk/authorize",
        "API_BASE_URL": "https://ob.sandbox.rbs.co.uk/open-banking/v3.1/aisp"
        }

BANK_FUNCTIONS = {
    "NatWest": NatWest,
    "RBS": RBS,
}

conn = MongoClient(MONGO_URL)

account_access_consents = conn.NatWest.account_access_consents
account_auth_tokens = conn.NatWest.account_auth_tokens
accounts = conn.NatWest.accounts
transactions = conn.NatWest.transactions
beneficiaries = conn.NatWest.beneficiaries
balances = conn.NatWest.balances
direct_debits = conn.NatWest.direct_debits
standing_orders = conn.NatWest.standing_orders
products = conn.NatWest.products
scheduled_payments = conn.NatWest.scheduled_payments
statements = conn.NatWest.statements
offers = conn.NatWest.offers
