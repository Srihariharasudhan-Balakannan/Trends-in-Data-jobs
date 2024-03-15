# imports
import smtplib
from email.message import EmailMessage
import datetime
import pytz
import streamlit as st


class EmailSender:
    def __init__(self, sender_id=st.secrets["sender_id"], password=st.secrets["password"]):
        self.sender_id = sender_id
        self.password = password

    def send_mail(self, receiver_id, exception):
        IST = pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(IST)
        subject = f"Exception occurred at {time_now.strftime('%H:%M:%S, on %d/%m/%Y')}"

        message = f"""\
        STATUS:
        During the process of data visualization, an exception occurred.
        Exception: {exception}.
        Visit https://streamlit.io/ to resolve the issue.

        Sent from the Streamlit cloud application.
        """

        # Create EmailMessage object and set content
        mail = EmailMessage()
        mail['From'] = self.sender_id
        mail['To'] = receiver_id
        mail['Subject'] = subject
        mail.set_content(message)

        try:
            # Establish a connection to the SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                # Start TLS encryption
                server.starttls()
                # Login to the sender's email account
                server.login(self.sender_id, self.password)
                # Send the email
                server.send_message(mail)
                print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")

