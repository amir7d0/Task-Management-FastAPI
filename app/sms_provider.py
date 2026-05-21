import os

import requests

SMSIR_SEND_URL = "https://api.sms.ir/v1/MessageSend"


def send_otp_message(phone_number: str, code: str) -> dict:
    api_key = os.getenv("SMSIR_API_KEY")
    if not api_key:
        raise RuntimeError("SMS.ir API key is not configured")

    line_number = os.getenv("SMSIR_LINE_NUMBER", "")
    message = f"کد تایید شما: {code}\nاین کد تا 5 دقیقه معتبر است."

    payload = {
        "Messages": [message],
        "MobileNumbers": [phone_number],
        "LineNumber": line_number,
        "SendDateTime": "",
        "CanContinueInCaseOfError": "true",
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-API-KEY": api_key,
    }

    response = requests.post(SMSIR_SEND_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("status") != 1:
        raise RuntimeError(f"SMS.ir send failed: {data}")
    return data
