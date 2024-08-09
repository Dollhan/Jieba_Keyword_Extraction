"""
使用 requests 库来发送 POST 请求。
时间：2024/8/8 下午7:24
"""
import requests


def send_post_request():
    url = "http://localhost:5000/analyze_text"
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": "郑州东站最近加强了防疫措施，进出站都需要出示健康码。"
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
