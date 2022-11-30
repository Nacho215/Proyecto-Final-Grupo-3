from fastapi import APIRouter, status, UploadFile, File
from repository import functionality

# Define router with sets
router = APIRouter(
    prefix="/dataset",
    tags=["DataSet"]
)


@router.post('/upload')
def upload_file(file: UploadFile = File(...)):
   return functionality.uploadFile(file)

@router.get('/customers')
def customersData():
    return None

@router.get('/transactions')
def transactionsData():
    return None

@router.get('/targetCustomers')
def targetCustomersData():
    return None

@router.get('/products')
def productsData():
    return None