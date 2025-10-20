from flask import Blueprint, jsonify

donation_bp = Blueprint('donation', __name__, url_prefix='/api/donations')

@donation_bp.route('/', methods=['GET'])
def list_donations():
    # placeholder: return empty list for now
    return jsonify(donations=[])
