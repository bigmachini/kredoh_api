import binascii
import os

from fastapi import Request, APIRouter

from . import store_to_firestore, _get_table_name
from .schemas import KredohTransaction

debug = True
router = APIRouter(
    tags=['Kredoh'],
    prefix='/kredoh'
)


# bill transaction
@router.post("/transaction")
async def kredoh_api(kredoh_transaction: KredohTransaction, request: Request):
    """
    This will be called when initiating a kredoh transaction

    :return: \n
        {
            'status' : 'Success'
        }
    """
    try:
        txn_id = f'kredoh_{binascii.hexlify(os.urandom(20)).decode()}'
        kredoh_transaction.transaction_id = txn_id
        table_name = _get_table_name(request.url.path)
        result = store_to_firestore(txn_id, kredoh_transaction.dict(), request.url.path, table_name)
        return {"status": 'Success' if result else 'Exists'}
    except Exception as ex:
        return {"status": 'Failed'}
