import binascii
import os

from fastapi import Request, APIRouter
import time

from . import store_to_firestore, _get_table_name
from .schemas import kyandaBillTransaction, KyandaCheckTransaction

debug = True
router = APIRouter(
    tags=['Kyanda'],
    prefix='/kyanda'
)

MERCHANT_ID = 'kredoh'
API_KEY = ''  # app_secret['kyanda_api']['api_key']


def _get_signature(message):
    import hashlib
    import hmac
    message = bytes(message, 'utf-8')
    secret = bytes(API_KEY, 'utf-8')
    signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
    return signature


# bill transaction
@router.post("/bill-transaction")
async def bill_transaction_api(bill_transaction: kyandaBillTransaction, request: Request):
    """
    This will be called when placing a kyanda bill transaction

    :return: \n
        {
            'status' : 'Success'
        }
    """
    try:
        signature = f'{bill_transaction.amount}{bill_transaction.account}{bill_transaction.telco}{bill_transaction.initiator_phone}{MERCHANT_ID}'
        txn_id = _get_signature(signature + bill_transaction.transaction_id)

        payload = {
            "MerchantID": MERCHANT_ID,
            "account": bill_transaction.account,
            "amount": bill_transaction.amount,
            "telco": bill_transaction.telco,
            "initiatorPhone": bill_transaction.initiator_phone,
            "signature": _get_signature(signature),
            "transaction_id": bill_transaction.transaction_id
        }

        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(txn_id, payload, request.url.path, table_name)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}


# check balance
@router.get("/check-balance")
async def check_balance_api(request: Request):
    """
    This endpoint will be used to get the balance for kyanda account \n
    :return:\n
        { "status" : "Success/Failed" }
    *Success* --> record was added to firestore successfully\n
    *Failed* --> Exception occurred
    """
    try:
        transaction_id = f'kyanda_{binascii.hexlify(os.urandom(20)).decode()}'

        payload = {
            "MerchantID": MERCHANT_ID,
            "signature": _get_signature(MERCHANT_ID),
            "transaction_id": transaction_id
        }
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(transaction_id, payload, request.url.path, table_name)
        return {"status": 'Success' if result else 'Failed'}
    except Exception as ex:
        return {"status": 'Failed'}


# Check Transaction
@router.post("/check-transaction")
async def check_transaction_api(obj: KyandaCheckTransaction, request: Request):
    """This endpoint is used to check the status of a transactions

    Args:
        obj: KyandaCheckTransaction object containing kyanda_id

    :param request:

    :return:\n
        { "status" : "Success/Failed" }
    *Success* --> record was added to firestore successfully\n
    *Failed* --> Exception occurred
    """
    try:
        transaction_id = f'kyanda_{binascii.hexlify(os.urandom(20)).decode()}'
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(transaction_id, obj.dict(), request.url.path, table_name)
        return {"status": 'Success' if result else 'Failed'}
    except Exception as ex:
        print("ex",ex)
        return {"status": 'Failed'}
