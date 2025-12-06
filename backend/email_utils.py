"""
Small helper module to simulate email sending.

In this project, we are not using a real email service provider.
Instead, we simply print the email contents to the console so we
can demonstrate that the backend is generating the correct message.
"""


def send_registration_email(to_email: str, username: str) -> dict:
    """
    This function simulates sending a welcome email after a user registers.

    Parameters:
        to_email (str): Recipient's email address.
        username (str): The username of the new account owner.

    Returns:
        dict: A small dictionary that describes what the email would contain.
              This helps the frontend or tests show a preview if needed.
    """
    subject = "Welcome to FoodLink!"
    body = (
        f"Hi {username},\n\n"
        "Thank you for registering with FoodLink! Your account has been created "
        "successfully. You can now log in and begin using the app.\n\n"
        "Best regards,\n"
        "The FoodLink Team"
    )

    # We are just printing the “email”; this is useful during development
    print("\n[EMAIL SIMULATION - REGISTRATION]")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print("Body:")
    print(body)
    print("[END EMAIL]\n")

    return {"to": to_email, "subject": subject, "body": body}


def send_password_reset_email(to_email: str, reset_link: str) -> dict:
    """
    Simulates sending a password reset email.

    Parameters:
        to_email (str): Recipient’s email address.
        reset_link (str): A link provided to reset the user password.

    Returns:
        dict: Information that represents the email content.
    """
    subject = "FoodLink - Password Reset Request"
    body = (
        "We received a request to reset your password for FoodLink.\n\n"
        f"Use the link below to create a new password:\n{reset_link}\n\n"
        "If you did not request this, simply ignore this message.\n\n"
        "Best regards,\n"
        "The FoodLink Team"
    )

    # Instead of actually sending it, we simulate it in the console
    print("\n[EMAIL SIMULATION - PASSWORD RESET]")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print("Body:")
    print(body)
    print("[END EMAIL]\n")

    return {"to": to_email, "subject": subject, "body": body}