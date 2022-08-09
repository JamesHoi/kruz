import urllib3
urllib3.disable_warnings()
import requests
import json


FILE_NAME = "data.txt"

def upload(info):
    url = "https://file.io/?title="+FILE_NAME
    mHeaders={}
    mHeaders["Host"]= "file.io"
    mHeaders["Origin"]= "https://www.file.io"
    mHeaders["Referer"]= "https://www.file.io/"
    mDatas={}

    data = json.dumps({
        "ipv6_ip":info.ipv6_ip,"src_port":info.src_port,
        "external_ip":info.external_ip,"external_port":info.external_port})
    mFiles={}
    mFiles[FILE_NAME]=data

    proxies = {
        "http": None,
        "https": None,
    }
    response = requests.request("POST", url, headers=mHeaders, data=mDatas,files=mFiles,proxies=proxies,verify=False)
    assert response.status_code == 200
    key = json.loads(response.text.encode('utf-8'))['key']
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
    return json.loads(response.text)