import binascii
import os

from fastapi import Request, APIRouter, HTTPException

from . import store_to_firestore, _get_table_name
from .schemas import kyandaTransaction, KyandaCheckTransaction, KyandaRegisterURL, TRANSACTION_TYPE

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

#Kyanda transaction API
@router.post("/transaction")
async def transaction_api(obj: kyandaTransaction, request: Request):
    """This will be called when placing a kyanda transaction whether airtime or paying a bill

    :return:\n
        { "status" : "Success/Exists/Failed/Invalid" }
    *Success* --> record was added to firestore successfully\n
    *Exists* --> record already exists\n
    *Failed* --> Exception occurred\n
    *Invalid* -->  Invalid Payload\n
    """
    # try:
    if (obj.account and obj.phone) or (obj.account is None and obj.phone is None):
        raise HTTPException(status_code=400, detail="Invalid Payload")

    if obj.account:
        signature = f'{obj.amount}{obj.account}{obj.telco}{obj.initiator_phone}{MERCHANT_ID}'
    if obj.phone:
        signature = f'{obj.amount}{obj.phone}{obj.telco}{obj.initiator_phone}{MERCHANT_ID}'

    txn_id = _get_signature(signature + obj.transaction_id)

    if obj.transaction_type == TRANSACTION_TYPE.AIRTIME_PIN and obj.telco not in ['SAFARICOM', 'AIRTEL', 'TELKOM']:
        raise HTTPException(status_code=400, detail="Invalid Telco")

    payload = {
        "MerchantID": MERCHANT_ID,
        "account": obj.account,
        "amount": obj.amount,
        "transaction_type": obj.transaction_type,
        "phone": obj.phone,
        "telco": obj.telco,
        "initiatorPhone": obj.initiator_phone,
        "signature": _get_signature(signature),
        "transaction_id": obj.transaction_id
    }

    try:
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(txn_id, payload, request.url.path, table_name)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


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
        print("ex", ex)
        return {"status": 'Failed'}


# Kyanda Register URL
@router.post("/register-url")
async def register_url_api(obj: KyandaRegisterURL, request: Request):
    """This endpoint is used to register the callback url for your application

    Args:
        obj: KyandaRegisterURL object containing callback_url

    :param request:

    :return:\n
        { "status" : "Success/Failed" }
    *Success* --> record was added to firestore successfully\n
    *Failed* --> Exception occurred\n
    """
    try:
        transaction_id = f'kyanda_{binascii.hexlify(os.urandom(20)).decode()}'
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(transaction_id, obj.dict(), request.url.path, table_name)
        return {"status": 'Success' if result else 'Failed'}
    except Exception as ex:
        print("ex", ex)
        return {"status": 'Failed'}
