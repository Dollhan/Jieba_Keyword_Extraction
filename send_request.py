"""
输入内容
时间：2024/8/8 下午7:24
"""
import requests


def send_post_request():
    url = "http://localhost:5000/analyze_text"
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": "今天早上我去郑大一附院，发现健康码变成了红码。"
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