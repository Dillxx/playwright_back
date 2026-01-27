import requests

def login():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
        "Content-Type": "application/json;charset=UTF-8;",
        "cookie": 'Hm_lvt_e8002ef3d9e0d8274b5b74cc4a027d08=1769061271,1769130667,1769390876,1769494133; Hm_lpvt_e8002ef3d9e0d8274b5b74cc4a027d08=1769494133; HMACCOUNT=33A4AC47B36E9765'
    }

    data = {
        "phone": "18888888888",
        "password": "4N4gv06xDUeLVTWkKYUb7A==",
        "loginType": 1,
        "configAuth": True
    }
    l = data["phone"]
    url = "http://dev8.kuotian.cc/admin/api/v1/user/login"

    response = requests.post(url=url, headers=headers, json=data)
    token = response.json()["data"]["token"]
    print(token)
    return token


if __name__ == '__main__':
    token = login()