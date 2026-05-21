from fastapi.testclient import TestClient
from app.main import app
from app import crud


def test_user_otp_flow():
    client = TestClient(app)

    # Request an OTP for a new phone number
    response = client.post('/users/otp/send', json={'phone_number': '+15551234567'})
    assert response.status_code == 200
    data = response.json()
    assert data['phone_number'] == '+15551234567'

    # Look up the OTP that was created in the database
    from app.db import SessionLocal
    db = SessionLocal()
    user = crud.get_user_by_phone(db, '+15551234567')
    assert user is not None
    assert user.otp_code is not None
    otp_code = user.otp_code

    # Verify the OTP and receive a fake bearer token
    verify_response = client.post('/users/otp/verify', json={'phone_number': '+15551234567', 'code': otp_code})
    assert verify_response.status_code == 200
    verify_data = verify_response.json()
    assert verify_data['token_type'] == 'bearer'
    assert verify_data['user']['phone_number'] == '+15551234567'
