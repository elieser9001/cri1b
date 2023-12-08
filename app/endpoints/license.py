from flask import Blueprint, jsonify
from app.lib.LicenseManager import LicenseManager
from app.database import crud
from app.lib.wordpressApi import get_cri1_license

bp = Blueprint('clients_checkin', __name__)

@bp.route('/license/<email>/<ext_id>/<device_id>/<phone_number>/')
def license(email, ext_id, device_id, phone_number):
    crud.link_device(device_id=device_id, email=email, ext_id=ext_id)
    devices_count = crud.devices_count(email=email, ext_id=ext_id)

    if devices_count > 3:
        return jsonify({"error": "max_devices_linked"})
    
    cri1_license = get_cri1_license(email=email)
    
    print("_______________________________________________")
    print(cri1_license)
    print("_______________________________________________")

    if "valid_license" in cri1_license and cri1_license["valid_license"] == True:
        ext_license = LicenseManager(
            email=email,
            first_name=cri1_license["user_first_name"],
            last_name=cri1_license["user_last_name"],
            extension_id=ext_id,
            device_id=ext_id,
            phone_number=phone_number
        )
        
        extension_data = ext_license.extension_data()
    
        return jsonify({
            "devices_count": devices_count,
            "cri1_license": cri1_license,
            "ext_license": extension_data
        })
    else:
        return jsonify({
            "devices_count": 0,
            "cri1_license": {"user_first_name": "", "user_last_name": "", "company_name": "", "valid_license":  False},
            "ext_license": None
        })
        

@bp.route('/device/<email>/<ext_id>/<device_id>')
def device(email, ext_id, device_id):
    crud.rm_device(email=email, ext_id=ext_id, device_id=device_id)
    
    return jsonify({"result": "done"})
