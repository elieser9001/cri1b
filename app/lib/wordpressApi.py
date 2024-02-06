import requests
import os
from dotenv import load_dotenv
load_dotenv()

cri1_username = os.getenv('CRI1_USERNAME')
cri1_password = os.getenv('CRI1_PASSWORD')

def fetch_json(wc_endpoint):
    url = f"https://cri1.com/wp-json/wc/v3/{wc_endpoint}"
    response = requests.get(url, auth=(cri1_username, cri1_password))
    try:
        r_json = response.json()
    except:
        return None

    return r_json

def fetch_graphql(query, variables):
    url = "https://cri1.com/graphql"

    response = requests.post(
        url,
        auth=(cri1_username, cri1_password),
        json={
            "query": query,
            "variables": variables
        }
    )

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

        email_found = (len(list(filter(lambda item: str(item["value"]).upper() == str(email).upper(), user_profile_emails))) > 0)

        return email_found
    except:
        return False

def email_to_customer_id_and_devices(email):
    try:
        users_data = fetch_json(f"customers?role=all")

        for user_data in users_data:
            if str(user_data["email"]).upper() != str(email).upper():
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
                    "max_devices": int(max_devices_linked) if len(max_devices_linked) > 0 else 1
                }

        return None
    except Exception as e:
        print(e)
        return None

def get_userdata_by_email(email):
    try:
        query = """
            query Query($search: String!) {
            users(where: {search: $search, searchColumns: EMAIL}) {
                nodes {
                    databaseId
                    firstName
                    lastName
                }
            }
        }    
        """
        variables = {"search": email}
        data = fetch_graphql(query=query, variables=variables)        
        
        return {
            "id": data["data"]["users"]["nodes"][0]["databaseId"],
            "first_name": data["data"]["users"]["nodes"][0]["firstName"],
            "last_name": data["data"]["users"]["nodes"][0]["lastName"],
        }
    except Exception as e:
        print(e)
        return None
    
def get_membership(user_data):
    try:
        user_id = user_data["id"]
        membership_data = fetch_json(f"memberships/members?customer={user_id}")
        
        return {
                    "customer_id": user_id,
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "company_name": "",
                    "status": membership_data[0]["status"],
                    "max_devices": int(list(filter(lambda item: item["slug"] == "sesiones-activas", membership_data[0]["profile_fields"]))[0]["value"])
                }
    except Exception as e:
        print(e)
        return None

def main_email_to_customer_id_and_devices(email):
    try:
        user_data = get_userdata_by_email(email)
        
        if user_data:
            user_membership = get_membership(user_data)

            if user_membership:
                return user_membership
    except Exception as e:
        print(e)
    
    return None


def get_cri1_license(email: str):
    try:        
        main_user_membership = main_email_to_customer_id_and_devices(email)
        
        if main_user_membership is not None:
            if main_user_membership["status"] == "active":
                return {
                        "customer_id": main_user_membership["customer_id"],
                        "user_first_name": main_user_membership["first_name"],
                        "user_last_name": main_user_membership["last_name"],
                        "company_name": main_user_membership["company_name"],
                        "max_devices": main_user_membership["max_devices"],
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
