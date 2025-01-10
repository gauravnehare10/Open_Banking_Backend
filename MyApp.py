import requests
import json


BASE_URL = "http://127.0.0.1:8000"

def callback():
    URL = f"{BASE_URL}/callback"
    res = requests.get(URL)
    data = res.json()
    return data

def accounts(access_token):
    URL = f"{BASE_URL}/accounts?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)
    return data["Data"]["Account"][0]["AccountId"]


def accounts_by_id(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)
    

def transactions(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/transactions?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)

def beneficiaries(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/beneficiaries?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def balances(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/balances?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def direct_debits(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/direct-debits?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def standing_orders(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/standing-orders?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def products(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/product?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def scheduled_payments(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/scheduled-payments?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def statements(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/statements?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


def offers(account_id, access_token):
    URL = f"{BASE_URL}/accounts/{account_id}/offers?access_token={access_token}"
    res = requests.get(URL)
    data = res.json()
    print(data)


access_token = callback()
account_id = accounts(access_token)

accounts_by_id(account_id, access_token)
transactions(account_id, access_token)
beneficiaries(account_id, access_token)
balances(account_id, access_token)
direct_debits(account_id, access_token)
standing_orders(account_id, access_token)
products(account_id, access_token)
scheduled_payments(account_id, access_token)
statements(account_id, access_token)
offers(account_id, access_token)
