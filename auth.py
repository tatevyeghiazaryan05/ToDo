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

        hashed_password = pwd_context.hash(password)

        main.cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s) RETURNING id
        """, (name, email, hashed_password))
        user_id = main.cursor.fetchone()[0]
        main.conn.commit()

        code = generate_verification_code()

        main.cursor.execute("""INSERT INTO verificationcode 
                            (code, user_id) VALUES (%s, %s)""",
                            (code, user_id))
        main.conn.commit()

        email_sent = send_verification_email(email, code)
        if not email_sent:
            raise HTTPException(status_code=500, detail="Failed to send verification email.")

        return {"message": "Verification code sent to your email. Please verify within 15 minutes."}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sign-up error: {str(e)}"
        )


@authrouter.post("/api/user/auth/verify")
def verify_user(verification_data: VerificationCodeSchema):
    try:
        main.cursor.execute("SELECT id FROM verificationcode WHERE email = %s",
                            (verification_data.email,))
        user = main.cursor.fetchone()

        if not user:
            raise HTTPException(status_code=400, detail="User not found.")
        user_id = user[0]

        main.cursor.execute("""SELECT * FROM verificationcode 
                            WHERE user_id = %s AND code = %s""",
                            (user_id, verification_data.code))
        data = main.cursor.fetchone()

        if not data:
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        created_at = data['created_at']

        expiration_time = created_at + timedelta(minutes=15)
        if datetime.now() > expiration_time:
            main.cursor.execute("DELETE FROM verificationcode WHERE id = %s", (data.get("id"),))
            main.conn.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired after 15 minutes."
            )

        main.cursor.execute("""Update users SET verified=%s WHERE user_id=%s""",
                            ("true", user_id))
        main.conn.commit()

        main.cursor.execute("DELETE FROM verificationcode WHERE id = %s", (data.get("id"),))
        main.conn.commit()

        return "Email verified successfully!"

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}"
        )


@authrouter.post("/api/user/auth/login")
def user_login(login_data: UserLoginSchema):
    try:
        email = login_data.email
        password = login_data.password

        main.cursor.execute("""SELECT * FROM users WHERE  email = %s""",
                            (email,))

        user = main.cursor.fetchone()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found!"
            )

        user = dict(user)
        user_password_db = user.get("password")

        if not pwd_context.verify(password, user_password_db):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="password is not correct!!"
            )

        else:
            user_id_db = user.get("id")
            user_email_db = user.get("email")

        token = create_access_token({"id": user_id_db,
                                    "email": user_email_db})
        return {"access_token": token}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )
