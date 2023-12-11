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

def get_user_data(email: str):
    json_data = fetch_json(f"customers?email={email}&role=all")
    
    return json_data

def get_user_membership(user_id):
    user_membership = fetch_json(f"memberships/members?customer={user_id}")

    return user_membership

def get_cri1_license(email: str):
    try:
        user_json_data = get_user_data(email=email)
        user_json_data = user_json_data[0]
        
        user_membership = get_user_membership(user_json_data["id"])
        user_membership = user_membership[0]
        
        if user_membership["status"] == "active":
            return {
                "user_first_name": user_json_data["first_name"],
                "user_last_name": user_json_data["last_name"],
                "company_name": user_json_data["billing"]["company"],
                "valid_license":  True
            }
        else:
            return {
                "user_first_name": "",
                "user_last_name": "",
                "company_name": "",
                "valid_license":  False
            }
    except Exception as e:
        print(e)
        return {"user_first_name": "", "user_last_name": "", "company_name": "", "valid_license":  False}
