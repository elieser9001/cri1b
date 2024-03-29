from datetime import datetime

class Extensions():
    WA_PLUS_WEB = "fhkimgpddcmnleeaicdjggpedegolbkb"
    WA_PLUS_WEB2 = "llnfhpbbmindfdggckdodgceceondlnh"
    WA_PLUS_WEB_FIXED = "waplusweb"
    # ---------------------------------
    PRIME_SENDER1 = "klfaghfflijdgoljefdlofkoinndmpia"
    PRIME_SENDER2 = "mddooilhbkodhjkicllbenpphldnolla"
    PRIME_SENDER_FIXED = "primesender"
    # ---------------------------------
    WHATWEB = "ekcgkejcjdcmonfpmnljobemcbpnkamh"
    WHATWEB_FIXED = "waweb"
    # ---------------------------------
    WHATSUP_PLUS = "lpbkofhnclhhlaibcklkgaonbbmhjeco"
    WHATSUP_PLUS_FIXED = "whatsupplus"
    # ---------------------------------
    PREMIUM_SENDER = "pggchepbleikpkhffahfabfeodghbafd"
    PREMIUM_SENDER_FIXED = "premiumsender"
    # ---------------------------------
    TG_SENDER = "ebnabkoglhoeigjibcledianfkakflkn"
    TG_SENDER2 = "kchbblidjcniipdkjlbjjakgdlbfnhgh"
    TG_SENDER_FIXED = "tgsender"
    # ---------------------------------

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
        
        if (self.extension_id == Extensions.WHATSUP_PLUS or self.extension_id == Extensions.WHATSUP_PLUS_FIXED):
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
        elif (self.extension_id  == Extensions.WHATWEB or self.extension_id  == Extensions.WHATWEB_FIXED):
            response = {
                "valid": True,
                "product": "waw_premium_monthly_20_users",
                "permissions": [
                    "CONTACTS_SYNC",
                    "CRM_INTEGRATION",
                    "WEBHOOKS",
                    "SCHEDULE_BROADCAST",
                    "BROADCAST",
                    "GROUPS_TOOLS",
                    "DISABLE_READ_RECEIPTS",
                    "SMART_REPLIES",
                    "EXPORT",
                ],
                "support": "support",
                "users": [self.phone_number],
                "numbers": [self.phone_number],
                "private": 'public',
                "expiration": self.expired_time,
            }
        elif (self.extension_id  == Extensions.PRIME_SENDER1 or self.extension_id  == Extensions.PRIME_SENDER2 or self.extension_id  == Extensions.PRIME_SENDER_FIXED):
            response = {
                "plan_type": "Advance",
                "created_date": "2023-11-29",
                "expiry_date": "2099-12-14",
                "last_plan_type": "Advance",
                "subscribed_date": "2023-11-29",
                "name": self.first_name,
                "email": self.email,
                "trial_days": 15
            }
        elif (self.extension_id  == Extensions.WA_PLUS_WEB or self.extension_id == Extensions.WA_PLUS_WEB2 or Extensions.WA_PLUS_WEB_FIXED):
            response = {
                "code": 100000,
                "data": {
                    "transaction_id": "transaction123",
                    "plink_id": "plink_1MNCrsBNqRnfJH4PBxqdWfBJ",
                    "current_plan": "plink_1MNCrsBNqRnfJH4PBxqdWfBJ",
                    "joined_date": 1698865802000,
                    "service_begin_period": 1698865802000,
                    "service_end_period": 2014485002000,
                    "upcoming_payments": 2014485002000,
                    "expiration_time": 2014485002000,
                    "state": 1,
                    "pay_status": 0,  
                }
            }
        elif (self.extension_id  == Extensions.PREMIUM_SENDER or self.extension_id  == Extensions.PREMIUM_SENDER_FIXED):
            response = {
                "KEY_IS_PRO": True
            }
        elif (self.extension_id  == Extensions.TG_SENDER or self.extension_id == Extensions.TG_SENDER2 or self.extension_id == Extensions.TG_SENDER_FIXED):
            response = {
                "result": {
                    "transactionId": 11321321321321,
                    "plan": "pro_team",
                    "expireTime": 213123123123
                }
            }

        return response
