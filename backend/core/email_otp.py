import smtplib
from email.message import EmailMessage

def send_delivery_otp(receiver_email):
    try:
        msg = EmailMessage()

        msg["Subject"] = "Delivery OTP"
        msg["From"] = "foodtech@gmail.com"
        msg["To"] = receiver_email

        msg.set_content("Your OTP is 123456")

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                "vu.241fa04d69@gmail.com",
                "ibzxwxhgxjvbslgz"
            )

            smtp.send_message(msg)

        print("Email Sent Successfully")

        return "123456"

    except Exception as e:
        print("FULL ERROR:", str(e))
        return None