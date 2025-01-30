from fastapi import APIRouter, HTTPException
from config.db import *
import httpx
import requests
from schemas.schema import *
import uuid

route = APIRouter()

@route.get("/callback")
async def callback(bank: str):
    """
    Handle callback after user authorization.
    """
    userId = "12345"
    bank_info = get_bank_info(bank)
    consent = get_auth_consent(bank, userId)
    payload = {
        "client_id": bank_info.get("CLIENT_ID"),
        "client_secret": bank_info.get("CLIENT_SECRET"),
        "redirect_uri": bank_info.get("REDIRECT_URI"),
        "grant_type": "authorization_code",
        "code": consent["code"],
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(bank_info.get("TOKEN_URL"), data=payload, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        token_data["_id"] = str(uuid.uuid4())
        token_data["userId"] = userId
        token_data["bank"] = bank
        account_auth_tokens.insert_one(token_data)
        access_token = token_data["access_token"]
        return access_token
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to get access token: {response.json()}"
        )

@route.get("/account-access-consent")
async def get_account_access_consent(bank):
    userId = '12345'
    access_token = fetch_access_token(userId, bank)
    bank_info = get_bank_info(bank)
    consent_id = get_consent_id(userId)
    url = f"{bank_info.get("API_BASE_URL")}/account-access-consents/{consent_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]

        account_access_consents.update_one({"ConsentId": consent_id}, {"$set": data}, upsert=True)
        user_account_consent_data = account_access_consents.find_one({"ConsentId": consent_id})
        return user_account_consent_data

@route.get("/accounts")
async def get_accounts(bank: str):
    userId = '12345'
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["Account"]
        # Save to MongoDB
        for account in data:
            account["_id"] = account.pop("AccountId", None)
            account["userId"] = userId
            accounts.insert_one(account)

        return data

@route.get("/accounts/{account_id}")
async def get_account_details(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #accounts.insert_one({"endpoint": f"accounts/{account_id}", "response": data})

        return data


@route.get("/accounts/{account_id}/transactions")
async def get_account_transactions(account_id: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/transactions"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["Transaction"]
        # Save to MongoDB
        for transaction in data:
            transaction["_id"] = transaction.pop("TransactionId", None)
            transaction["userId"] = userId
            transactions.insert_one(transaction)
        return data
    
@route.get("/accounts/{account_id}/beneficiaries")
async def get_account_beneficiaries(account_id: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/beneficiaries"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["Beneficiary"]
        # Save to MongoDB
        for beneficiary in data:
            beneficiary["_id"] = beneficiary.pop("BeneficiaryId", None)
            beneficiary["userId"] = userId
            beneficiaries.insert_one(beneficiary)

        return data

@route.get("/accounts/{account_id}/balances")
async def get_account_balances(account_id: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/balances"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["Balance"]
        # Save to MongoDB
        for balance in data:
            balance["_id"] = str(uuid.uuid4())
            balance["userId"] = userId
            balances.insert_one(balance)

        return data


@route.get("/accounts/{account_id}/direct-debits")
async def get_account_direct_debits(account_id: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/direct-debits"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["DirectDebit"]
        # Save to MongoDB
        for direct_debit in data:
            direct_debit["_id"] = str(uuid.uuid4())
            direct_debit["userId"] = userId
            direct_debits.insert_one(direct_debit)
        return data

@route.get("/accounts/{account_id}/standing-orders")
async def get_account_standing_orders(account_id: str, access_token: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/standing-orders"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["StandingOrder"]
        # Save to MongoDB
        for standing_order in data:
            standing_order["_id"] = str(uuid.uuid4())
            standing_order["userId"] = userId
            standing_orders.insert_one(standing_order)
        return data

@route.get("/accounts/{account_id}/product")
async def get_account_product(account_id: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/product"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["Product"]
        # Save to MongoDB
        for product in data:
            product["_id"] = product.pop("ProductId", None)
            product["userId"] = userId
            products.insert_one(product)

        return data

@route.get("/accounts/{account_id}/scheduled-payments")
async def get_account_scheduled_payments(account_id: str, bank: str):
    userId = "12345"
    access_token = fetch_access_token(userId)
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/scheduled-payments"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()["Data"]["ScheduledPayment"]
        # Save to MongoDB
        for scheduled_payment in data:
            scheduled_payment["_id"] = str(uuid.uuid4())
            scheduled_payment["userId"] = userId
            scheduled_payments.insert_one(scheduled_payment)

        return data

@route.get("/accounts/{account_id}/statements")
async def get_account_statements(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/statements"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #statements.insert_one({"endpoint": f"accounts/{account_id}/statements", "response": data})

        return data

@route.get("/accounts/{account_id}/offers")
async def get_account_offers(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #offers.insert_one({"endpoint": f"accounts/{account_id}/offers", "response": data})

        return data
