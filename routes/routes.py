from fastapi import APIRouter, HTTPException
from config.db import *
import httpx
import requests
from schemas.schema import *

route = APIRouter()

@route.get("/callback")
async def callback(bank: str):
    """
    Handle callback after user authorization.
    """
    bank_info = get_bank_info(bank)
    code = get_auth_code(bank)
    payload = {
        "client_id": bank_info.get("CLIENT_ID"),
        "client_secret": bank_info.get("CLIENT_SECRET"),
        "redirect_uri": bank_info.get("REDIRECT_URI"),
        "grant_type": "authorization_code",
        "code": code,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(bank_info.get("TOKEN_URL"), data=payload, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to get access token: {response.json()}"
        )

@route.get("/accounts")
async def get_accounts(access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #accounts.insert_one({"endpoint": "accounts", "response": data})

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
async def get_account_transactions(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/transactions"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #transactions.insert_one({"endpoint": f"accounts/{account_id}/transactions", "response": data})
        return data
    
@route.get("/accounts/{account_id}/beneficiaries")
async def get_account_beneficiaries(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/beneficiaries"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #beneficiaries.insert_one({"endpoint": f"accounts/{account_id}/beneficiaries", "response": data})

        return data

@route.get("/accounts/{account_id}/balances")
async def get_account_balances(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/balances"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #balances.insert_one({"endpoint": f"accounts/{account_id}/balances", "response": data})

        return data


@route.get("/accounts/{account_id}/direct-debits")
async def get_account_direct_debits(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/direct-debits"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #direct_debits.insert_one({"endpoint": f"accounts/{account_id}/direct-debits", "response": data})

        return data

@route.get("/accounts/{account_id}/standing-orders")
async def get_account_standing_orders(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/standing-orders"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #standing_orders.insert_one({"endpoint": f"accounts/{account_id}/standing-orders", "response": data})

        return data

@route.get("/accounts/{account_id}/product")
async def get_account_product(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/product"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #products.insert_one({"endpoint": f"accounts/{account_id}/product", "response": data})

        return data

@route.get("/accounts/{account_id}/scheduled-payments")
async def get_account_scheduled_payments(account_id: str, access_token: str, bank: str):
    bank_info = get_bank_info(bank)
    url = f"{bank_info.get("API_BASE_URL")}/accounts/{account_id}/scheduled-payments"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        # Save to MongoDB
        #scheduled_payments.insert_one({"endpoint": f"accounts/{account_id}/scheduled-payments", "response": data})

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
