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

def active_subscriptions(user_json_data):
    try:
        meta_data = user_json_data[0]["meta_data"]    
        subscriptions_ids = list(filter(lambda item: item["key"] == "_wcs_subscription_ids_cache", meta_data))

        subscriptions_info = []

        if subscriptions_ids and subscriptions_ids[0]["value"]:
            for id in subscriptions_ids[0]["value"]:
                result = fetch_json(f"subscriptions/{id}")
                
                # if result["next_payment_date_gmt"]:
                if result["status"] == "active":
                    # subscriptions_info.append(result["next_payment_date_gmt"])

                    subscriptions_info.append({
                        "product_name": result["line_items"][0]["name"],
                        "product_id": result["line_items"][0]["product_id"],
                        "expire": result["next_payment_date_gmt"]
                    })

        return subscriptions_info
    except:
        return None
    

def get_cri1_license(email: str):
    try:
        user_json_data = get_user_data(email=email)
        subscriptions = active_subscriptions(user_json_data=user_json_data)
        
        if user_json_data:
            user_json_data = user_json_data[0]

            for sub in subscriptions:
                if "expire" in sub:
                    exp_datetime = datetime.strptime(sub["expire"], "%Y-%m-%dT%H:%M:%S")
                    current_datetime = datetime.now()

                    if exp_datetime - current_datetime > timedelta(0):
                        return {"user_first_name": user_json_data["first_name"], "user_last_name": user_json_data["last_name"], "company_name": user_json_data["billing"]["company"], "valid_license":  True}
                    else:
                        return {"user_first_name": user_json_data["first_name"], "user_last_name": user_json_data["last_name"], "company_name": user_json_data["billing"]["company"], "valid_license":  False}
                else:
                    return {"user_first_name": user_json_data["first_name"], "user_last_name": user_json_data["last_name"], "company_name": user_json_data["billing"]["company"], "valid_license":  False}

            return {"user_first_name": user_json_data["first_name"], "user_last_name": user_json_data["last_name"], "company_name": user_json_data["billing"]["company"], "valid_license":  False}
        else:
            return None
    except Exception as e:
        print(e)
        return None
