from enum import Enum

from pydantic import BaseModel
from typing import Optional, List


class NameValue(BaseModel):
    Name: str
    Value: Optional[str] = None


class KeyValue(BaseModel):
    Key: str
    Value: Optional[str] = None


class ReferenceData(BaseModel):
    ReferenceItem: KeyValue


class ResultParameters(BaseModel):
    ResultParameter: List[KeyValue]


class CallbackResult(BaseModel):
    ResultType: int
    ResultCode: int
    ResultDesc: str
    OriginatorConversationID: str
    ConversationID: str
    TransactionID: str
    ResultParameters: ResultParameters
    ReferenceData: ReferenceData


# Africastalking Schemas
class ATCallback(BaseModel):
    phoneNumber: str
    description: str
    status: str
    requestId: str
    discount: str
    value: str


# Kyanda Schemas
class KyandaCallbackDetails(BaseModel):
    biller_Receipt: Optional[str] = None
    tokens: Optional[str] = None
    units: Optional[str] = None


class KyandaCallback(BaseModel):
    category: str
    source: str
    destination: str
    MerchantID: str
    details: KyandaCallbackDetails
    status: str
    status_code: str
    message: str
    transactionDate: str
    transactionRef: str
    amount: str


# mpesa stk callback
class CallbackMetadata(BaseModel):
    Item: List[NameValue]


class StkCallback(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: CallbackMetadata


class StkPushCallbackBody(BaseModel):
    stkCallback: StkCallback


class StkPushCallback(BaseModel):
    Body: StkPushCallbackBody


# mpesa c2b callback
class C2BCallback(BaseModel):
    TransactionType: str
    TransID: str
    TransTime: str
    TransAmount: str
    BusinessShortCode: str
    BillRefNumber: str
    InvoiceNumber: str
    OrgAccountBalance: str
    ThirdPartyTransID: str
    MSISDN: str
    FirstName: str
    MiddleName: str
    LastName: str


# mpesa transaction_status_callback
class TransactionStatusCallback(BaseModel):
    Result: CallbackResult


# mpesa reversal Callback
class ReversalCallback(BaseModel):
    Result: CallbackResult


class StkQuery(BaseModel):
    checkout_request_id: str
    callback_url: str


class Reversal(BaseModel):
    transaction_id: Optional[str]
    firebase_token: Optional[str]
    mpesa_code: str
    amount: str


class TransactionStatus(BaseModel):
    mpesa_code: str
    callback_url: str


# KYANDA
class TELCOS(str, Enum):
    KPLC_PREPAID = 'KPLC_PREPAID'
    KPLC_POSTPAID = 'KPLC_POSTPAID'
    GOTV = 'GOTV'
    DSTV = 'DSTV'
    ZUKU = 'ZUKU'
    STARTIMES = 'STARTIMES'
    NAIROBI_WTR = 'NAIROBI_WTR'
    SAFARICOM = 'SAFARICOM'
    AIRTEL = 'AIRTEL'
    TELKOM = 'TELKOM'
    EQUITEL = 'EQUITEL'
    FAIBA = 'FAIBA'
    FAIBA_B = 'FAIBA_B'


class TRANSACTION_TYPE(str, Enum):
    AIRTIME = 'airtime'
    BILL = 'bill'


class kyandaTransaction(BaseModel):
    amount: str
    account: Optional[str] = None
    phone: Optional[str] = None
    telco: TELCOS
    initiator_phone: str
    transaction_id: str
    transaction_type: TRANSACTION_TYPE


class KyandaCheckTransaction(BaseModel):
    kyanda_id: str


class KyandaRegisterURL(BaseModel):
    callback_url: str


# KREDOH
class KredohTransaction(BaseModel):
    phone_number: str
    amount: str
    transaction_type: str
    other_phone_number: Optional[str] = None
    firebase_token: Optional[str] = None
    sms_request: Optional[str] = None
    app_version: Optional[str] = None
    meter_number: Optional[str] = None
    transaction_id: Optional[str] = None
