# import json
from datetime import datetime

class Extensions():
    WHATSUP_PLUS = "lpbkofhnclhhlaibcklkgaonbbmhjeco"
    WHATWEB = "ekcgkejcjdcmonfpmnljobemcbpnkamh"

class LicenseManager:
    def __init__(
        self,
        email,
        first_name,
        last_name,
        extension_id,
        device_id,
        phone_number
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.extension_id = extension_id
        self.device_id = device_id
        self.phone_number = phone_number
        self.expired_time = "2299-12-25 14:30:00.000000"

    def extension_data(self):
        response = {}
        
        if (self.extension_id == Extensions.WHATSUP_PLUS):
            response = {
                "cancelado": "",
                "s_status": "active",
                "users": [int(self.phone_number)],
                "lid": "141231251232132142321321",
                "plan_id": "8",
                "email": self.email,
                "support_number": 14123125123213214,
                "first_name": self.first_name,
                "last_name": self.last_name
            }
        if (self.extension_id  == Extensions.WHATWEB):
            # date_format = datetime.strptime(self.license.expired_time, "%d-%m-%Y %I:%M:%S %p")
            expired = datetime.timestamp(self.expired_time)
            response = {
                "valid": True,
                "product": "waw_premium_monthly_20_users",
                "permissions": ["CONTACTS_SYNC"],
                "support": "support",
                "users": [self.phone_number],
                "numbers": [self.phone_number],
                "private": 'public',
                "expiration": expired,
            }

        # return json.dumps(response)
        return response
