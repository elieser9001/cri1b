from flask import Blueprint, jsonify
from app.lib.LicenseManager import LicenseManager
from app.database import crud

bp = Blueprint('clients_checkin', __name__)

@bp.route('/license/<key>/<ext_id>/<device_id>/<phone_number>/')
def license(key, ext_id, device_id, phone_number):
    license = crud.get_license(key=key)
    
    if license:
        lm = LicenseManager(
            license=license,
            extension_id=ext_id,
            device_id=device_id,
            phone_number=phone_number
        )

        result = lm.extension_data()
    else:
        result = {}

    
    print(result)

    return jsonify(result)
