from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db
from app.sms_provider import send_otp_message

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/otp/send", response_model=schemas.User)
def send_otp(request: schemas.UserLoginOTP, db: Session = Depends(get_db)):
    user, otp_code = crud.create_otp(db, request.phone_number)
    try:
        send_otp_message(user.phone_number, otp_code)
    except Exception as exc:
        # Fallback to console output when SMS.ir is not configured or fails.
        print(f"[SMS.ir fallback] {exc}")
        print(f"[SMS] Sending OTP {otp_code} to {user.phone_number}")
    return user


@router.post("/otp/verify", response_model=schemas.LoginResponse)
def verify_otp(request: schemas.UserVerifyOTP, db: Session = Depends(get_db)):
    user = crud.verify_otp(db, request.phone_number, request.code)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    return schemas.LoginResponse(
        user=user,
        access_token=f"fake-token-{user.id}",
        token_type="bearer",
    )
