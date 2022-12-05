import requests
import openpyxl

def test_read_files():    
    response = requests.get('http://127.0.0.1:8000/dataset/get_data')
    assert response.status_code == 200
    assert response.content != None
    
def test_upload_files():
    path_file = "C:/Users/ale/Downloads/KPMG_VI_New_raw_data_update_final.xlsx"
    excel_document = openpyxl.load_workbook(path_file)
    print(excel_document.worksheets)
    response = requests.post('http://127.0.0.1:8000/dataset/upload',
    data={"type": "multipart/form-data"},
    files={"file": excel_document})
    assert response.status_code == 200
    assert response.json()['saved'] == True
