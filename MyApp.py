import requests
import json


BASE_URL = "http://127.0.0.1:8000"


def callback(bank):
    URL = f"{BASE_URL}/callback"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)
    return data

def accounts(access_token, bank):
    URL = f"{BASE_URL}/accounts?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)
    return data["Data"]["Account"][0]["AccountId"]

def accounts_by_id(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)
    

def transactions(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/transactions?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def beneficiaries(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/beneficiaries?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def balances(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/balances?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def direct_debits(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/direct-debits?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def standing_orders(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/standing-orders?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def products(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/product?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def scheduled_payments(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/scheduled-payments?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def statements(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/statements?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)


def offers(account_id, access_token, bank):
    URL = f"{BASE_URL}/accounts/{account_id}/offers?access_token={access_token}"
    res = requests.get(URL, {'bank': bank})
    data = res.json()
    print(data)



bank = "NatWest"
access_token = callback(bank)
account_id = accounts(access_token, bank)

accounts_by_id(account_id, access_token, bank)
transactions(account_id, access_token, bank)
beneficiaries(account_id, access_token, bank)
balances(account_id, access_token, bank)
direct_debits(account_id, access_token, bank)
standing_orders(account_id, access_token, bank)
products(account_id, access_token, bank)
scheduled_payments(account_id, access_token, bank)
statements(account_id, access_token, bank)
offers(account_id, access_token, bank)


