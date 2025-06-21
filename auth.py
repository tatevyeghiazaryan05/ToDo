from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status, Form

import main
from schemas import UserLoginSchema, VerificationCodeSchema
from security import pwd_context, create_access_token
from email_service import send_verification_email, generate_verification_code


authrouter = APIRouter()


@authrouter.post("/api/user/auth/sign-up")
def user_signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    try:
        main.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if main.cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error")

    try:
        hashed_password = pwd_context.hash(password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error hashing password")

    try:
        main.cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s) RETURNING id
        """, (name, email, hashed_password))
        user_id = main.cursor.fetchone()[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting user")

    main.conn.commit()

    code = generate_verification_code()

    try:
        main.cursor.execute("""INSERT INTO verificationcode (code, user_id) VALUES (%s, %s)""",
                            (code, user_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting verification code")

    main.conn.commit()

    try:
        email_sent = send_verification_email(email, code)
        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send verification email.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending verification email")

    return {"message": "Verification code sent to your email. Please verify within 15 minutes."}


@authrouter.post("/api/user/auth/verify")
def verify_user(verification_data: VerificationCodeSchema):
    try:
        main.cursor.execute("SELECT id FROM users WHERE email = %s", (verification_data.email,))
        user = main.cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error")

    try:
        if not user:
            raise HTTPException(status_code=400, detail="User not found.")
        user_id = user[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user")

    try:
        main.cursor.execute("""SELECT * FROM verificationcode 
                            WHERE user_id = %s AND code = %s""",
                            (user_id, verification_data.code))
        data = main.cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error")

    try:
        if not data:
            raise HTTPException(status_code=400, detail="Invalid verification code.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching verification code")

    created_at = data['created_at']
    expiration_time = created_at + timedelta(minutes=15)
    if datetime.now() > expiration_time:
        try:
            main.cursor.execute("DELETE FROM verificationcode WHERE id = %s", (data.get("id"),))
            main.conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting expired code")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired after 15 minutes."
        )

    try:
        main.cursor.execute("""UPDATE users SET verified=%s WHERE id=%s""",
                            ("true", user_id))
        main.conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user as verified")

    try:
        main.cursor.execute("DELETE FROM verificationcode WHERE id = %s", (data.get("id"),))
        main.conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting verification code")

    return "Email verified successfully!"


@authrouter.post("/api/user/auth/login")
def user_login(login_data: UserLoginSchema):
    email = login_data.email
    password = login_data.password

    try:
        main.cursor.execute("""SELECT * FROM users WHERE email = %s""", (email,))
        user = main.cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error")

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found!"
        )

    try:
        user = dict(user)
        user_password_db = user.get("password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing user data")

    try:
        if not pwd_context.verify(password, user_password_db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Password is not correct!"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Password verification error")

    try:
        user_id_db = user.get("id")
        user_email_db = user.get("email")

        token = create_access_token({"id": user_id_db, "email": user_email_db})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token creation error")

    return {"access_token": token}
