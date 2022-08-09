import urllib3
urllib3.disable_warnings()
import requests
import time
import json
import os


FILE_NAME = "data.txt"
DATA = "hello world"

def upload(filename):
    url = "https://file.io/?title="+filename
    mHeaders={}
    mHeaders["Host"]= "file.io"
    mHeaders["Origin"]= "https://www.file.io"
    mHeaders["Referer"]= "https://www.file.io/"
    mDatas={}
    mFiles={}
    mFiles[filename]=DATA

    proxies = {
        "http": None,
        "https": None,
    }
    response = requests.request("POST", url, headers=mHeaders, data=mDatas,files=mFiles,proxies=proxies,verify=False)
    assert response.status_code == 200
    key = json.loads(response.text.encode('utf8'))['key']
    return key

def download(key):
    url = f"https://file.io/{key}"

    mHeaders={}
    mHeaders["Host"]= "file.io"
    mHeaders["Referer"]= "https://www.file.io/"
    mDatas=""
    proxies = {
        "http": None,
        "https": None,
    }
    response = requests.request("GET", url, headers=mHeaders, data=mDatas,proxies=proxies,verify=False)
    assert response.status_code == 200
    assert response.text == DATA

def test_code():
    tmp = time.time()
    key = upload(FILE_NAME)
    print(time.time()-tmp)
    download(key)
    print(time.time()-tmp)

test_code()