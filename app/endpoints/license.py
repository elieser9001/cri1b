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

    if cri1_license:
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

@bp.route('/device/<email>/<ext_id>/<device_id>')
def device(email, ext_id, device_id):
    crud.rm_device(email=email, ext_id=ext_id, device_id=device_id)
    
    return jsonify({"result": "done"})
