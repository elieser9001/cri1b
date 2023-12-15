import requests
from datetime import datetime, timedelta

def fetch_json(wc_endpoint):
    url = f"https://cri1.com/wp-json/wc/v3/{wc_endpoint}"
    response = requests.get(url, auth=("Developer", "Developer_2023$"))
    try:
        r_json = response.json()
    except:
        return None

    return r_json

def get_users_data():
    # json_data = fetch_json(f"customers?email={email}&role=all")
    json_data = fetch_json(f"customers?role=all")
    
    return json_data

def get_user_membership(user_id):
    user_membership = fetch_json(f"memberships/members?customer={user_id}")

    return user_membership

def search_email_in_metadata(email, user_data):
    try:
        user_profile_emails = list(filter(lambda item: item["key"][:36] == "_wc_memberships_profile_field_correo", user_data["meta_data"]))

        email_found = (len(list(filter(lambda item: item["value"] == email, user_profile_emails))) > 0)

        return email_found
    except:
        return False

def email_to_customer_id_and_devices(email):
    try:
        users_data = fetch_json(f"customers?role=all")
        
        for user_data in users_data:
            if user_data["email"] != email:
                if search_email_in_metadata(email, user_data):
                    return {
                        "customer_id": user_data["id"],
                        "first_name": user_data["first_name"],
                        "last_name": user_data["last_name"],
                        "company_name": user_data["billing"]["company"],
                        "max_devices": int(list(filter(lambda item: item["key"] == "_wc_memberships_profile_field_sesiones_activas", user_data["meta_data"]))[0]["value"])
                        }
            else:
                max_devices_linked = list(filter(lambda item: item["key"] == "_wc_memberships_profile_field_sesiones_activas", user_data["meta_data"]))[0]["value"]

                return {
                    "customer_id": user_data["id"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "company_name": user_data["billing"]["company"],
                    "max_devices": int(max_devices_linked) if len(max_devices_linked) > 0 else 3
                }

        return None
    except Exception as e:
        print(e)
        return None

def get_cri1_license(email: str):
    try:
        result = email_to_customer_id_and_devices(email)
        
        if result:
            user_membership = get_user_membership(result["customer_id"])
            user_membership = user_membership[0]
            
            if user_membership["status"] == "active":
                return {
                    "customer_id": result["customer_id"],
                    "user_first_name": result["first_name"],
                    "user_last_name": result["last_name"],
                    "company_name": result["company_name"],
                    "max_devices": result["max_devices"],
                    "valid_license":  True
                }
            else:
                return {
                    "customer_id": "",
                    "user_first_name": "",
                    "user_last_name": "",
                    "company_name": "",
                    "max_devices": 0,
                    "valid_license":  False
                }
        else:
            return {
                    "customer_id": "",
                    "user_first_name": "",
                    "user_last_name": "",
                    "company_name": "",
                    "max_devices": 0,
                    "valid_license":  False
            }
    except Exception as e:
        print(e)
        return {
                "customer_id": "",
                "user_first_name": "",
                "user_last_name": "",
                "company_name": "",
                "max_devices": 0,
                "valid_license":  False
        }
