# import json
from datetime import datetime

class Extensions():
    WHATSUP_PLUS = "lpbkofhnclhhlaibcklkgaonbbmhjeco"
    WHATWEB = "ekcgkejcjdcmonfpmnljobemcbpnkamh"

class LicenseManager:
    def __init__(self, license, extension_id, device_id, phone_number):
        self.license = license
        self.device_id = device_id
        self.phone_number = phone_number
        # self.license.id = license.id
        self.extension_id = extension_id
        # self.license.device_id = license.device_id
        self.license.key = license.key
        self.license.name = license.name
        self.license.lastname = license.lastname
        self.license.email = license.email
        self.license.phone_number = license.phone_number
        self.license.expired_time = license.expired_time
        # self.license.created_datetime = license.created_datetime
        
    def extension_data(self):
        response = {}
        
        if (self.extension_id == Extensions.WHATSUP_PLUS):
            response = {
                "cancelado": "",
                "s_status": "active",
                "users": [int(self.phone_number)],
                "lid": "141231251232132142321321",
                "plan_id": "8",
                "email": self.license.email,
                "support_number": 14123125123213214,
                "first_name": self.license.name,
                "last_name": self.license.lastname
            }

        if (self.extension_id  == Extensions.WHATWEB):
            # date_format = datetime.strptime(self.license.expired_time, "%d-%m-%Y %I:%M:%S %p")
            expired = datetime.timestamp(self.license.expired_time)
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
