import bcrypt
import random
import string
from config import Config
from email.message import EmailMessage
import ssl
import smtplib

def generate_otp(email,num_digits=6):
    """
    Generate a random OTP (One Time Password) consisting of digits and letters.
    :param num_digits: Number of digits in the OTP (default is 6)
    :return: OTP in bcrypt format
    """
    
    otp = ''.join(random.choices(string.ascii_letters + string.digits, k=num_digits))
    otp_bytes = otp.encode('utf-8')
    bcrypt_hash = bcrypt.hashpw(otp_bytes, bcrypt.gensalt())
    send_otp(email,otp)
    return bcrypt_hash.decode('utf-8')


def check_otp(otp, bcrypt_hash):
    """
    Check if the provided OTP matches the given bcrypt hash.
    :param otp: The OTP provided by the user
    :param bcrypt_hash: The bcrypt hash of the correct OTP
    :return: True if the OTP matches the bcrypt hash, False otherwise
    """
    
    otp_bytes = otp.encode('utf-8')
    return bcrypt.checkpw(otp_bytes, bcrypt_hash.encode('utf-8'))

def send_otp(email,otp):
    email_sender=Config.Email
    email_password=Config.MAIL_KEY
    email_reciver=email
    subject='testing a mail'

    body="this is testing otp pls check"+" "+str(otp)

    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_reciver
    em['subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context==context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())
def SendTYmessage(email):
    email_sender=Config.Email
    email_password=Config.MAIL_KEY
    email_receiver = email
    subject = 'Thanks for contacting us'
    
    # HTML-formatted body
    body = """
        <h2>Stocks Sales</h2>
        <p>This is a testing mail for thanking the customer.</p>
        <hr>
        <i>Please provide a valid email format for sending messages to the customer.</i>
    """

    # Create the EmailMessage object
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    
    # Set the content type to HTML
    em.add_header('Content-Type', 'text/html')
    
    # Set the body of the email
    em.set_payload(body)

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Establish a connection to the SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_sender, email_password)
        server.send_message(em)
