import requests
import json


def verify(phone, code):
    url = "https://send.smsxabar.uz/broker-api/send/"
    headers = {
        'Authorization': 'Basic Y2FtYnJpZ2U6SDI2bUdEODJ1aA==',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "messages": [
            {
                "recipient": phone,
                "message-id": "abc000000001",
                "sms": {
                    "originator": "3700",
                    "content": {
                        "text": f"Tasdiqlash kodi: {code}"
                    }
                }
            }
        ]
    })
    response = requests.post(url=url, data=payload, headers=headers)
    return response.text