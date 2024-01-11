from app.database.database import db_session
from app.database.models import  License, Device
from datetime import datetime
import uuid
    
def get_license(key: str):
    try:
        result = License.query.filter(License.key == key).one()
    except:
        result = None
        
    return result

def link_device(device_id: str, customer_id: str,  email: str, ext_id: str):
    try:
        device = Device(
            key=device_id,
            customer_id=customer_id,
            email=email,
            ext_id=ext_id
        )
        
        db_session.add(device)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        # print("Error en link_device", e)

def devices_count(customer_id: str, ext_id: str):
    result = 0

    try:
        result = db_session.query(
            Device
        ).filter(Device.customer_id == customer_id).filter(Device.ext_id == ext_id).count()
            
        print("---------------------------------")
        print(result)
        print("---------------------------------")
    except Exception as e:
        print("Error en devices_count", e)
        result = 0
        
    return result

def rm_device(email: str, ext_id: str, device_id: str):
    try:
        device = db_session.query(Device).filter(Device.email == email).filter(Device.ext_id == ext_id).filter(Device.key == device_id).one()
        
        db_session.delete(device)
        db_session.commit()  
    except Exception as e:
        db_session.rollback()
        print(e)

def create_license(
    # extension_id: str,
    # device_id: str,
    # key: str,
    name: str,
    lastname: str,
    email: str,
    phone_number: str,
    expired_time: str
):
    #  "%Y-%m-%d %I:%M:%S %p"
    expired_time = datetime.strptime(expired_time, "%d-%m-%Y %I:%M:%S %p")
    key = str(uuid.uuid4()).replace('-', '')
    
    license = License(
        # extension_id,
        # device_id,
        key=key,
        name=name,
        lastname=lastname,
        email=email,
        phone_number=phone_number,
        expired_time=expired_time
     )
    
    db_session.add(license)
    db_session.commit()
