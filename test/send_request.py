"""
使用 requests 库来发送 POST 请求。
时间：2024/8/8 下午7:24
"""
import requests


def send_post_request():
    url = "http://localhost:40006/analyze_text"
    headers = {'Content-Type': 'application/json'}
    data = {
        "昨天晚上，我在郑州市区散步的时候，看到很多地方都贴上了疫情防控的宣传海报。"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None


# 发送请求并打印响应
response_data = send_post_request()
if response_data:
    print(response_data)
else:
    print("请求失败")
