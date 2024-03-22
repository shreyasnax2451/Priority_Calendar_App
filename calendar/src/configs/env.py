from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS_SMPT = os.getenv('EMAIL_ADDRESS_SMPT')
PASSWORD_SMPT = os.getenv('PASSWORD_SMPT')