import binascii
import os

from fastapi import Request, APIRouter

from . import store_to_firestore, _get_table_name
from .schemas import StkQuery, Reversal, TransactionStatus

debug = True
router = APIRouter(
    tags=['Mpesa'],
    prefix='/asepm'
)


# bill transaction
@router.post("/stk-query")
async def stk_query_api(obj: StkQuery, request: Request):
    """This endpoint is used to query mpesa given a checkout_request_id

    :return: \n
        {
            'status' : 'Success/Failed'
        }
    """
    try:
        txn_id = f'mpesa_{binascii.hexlify(os.urandom(20)).decode()}'
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(txn_id, obj.dict(), request.url.path, table_name)
        return {"status": 'Success' if result else 'Failed'}
    except Exception as ex:
        return {"status": 'Failed'}


@router.post("/reversal")
async def stk_query_api(obj: Reversal, request: Request):
    """This endpoint is used to process mpesa reversals

    :return: \n
        {
            'status' : 'Success/Failed'
        }
    """
    try:
        txn_id = f'mpesa_{binascii.hexlify(os.urandom(20)).decode()}'
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(txn_id, obj.dict(), request.url.path, table_name)
        return {"status": 'Success' if result else 'Failed'}
    except Exception as ex:
        return {"status": 'Failed'}


@router.post("/transaction-status")
async def transaction_status_api(obj: TransactionStatus, request: Request):
    """This endpoint is used to check the status of a transaction

    :return: \n
        {
            'status' : 'Success/Failed'
        }
    """
    try:
        txn_id = f'mpesa_{binascii.hexlify(os.urandom(20)).decode()}'
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(txn_id, obj.dict(), request.url.path, table_name)
        return {"status": 'Success' if result else 'Failed'}
    except Exception as ex:
        return {"status": 'Failed'}
