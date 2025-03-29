from flask import jsonify, request
from supabase import create_client, Client
from config import Config
from flask import Blueprint

unlicensedminer_bp = Blueprint('unlicensedminer', __name__, url_prefix='/unlicensedminer')

@unlicensedminer_bp.route('/status', methods=['GET'])
def get_user_status():
    # Assuming you have a way to identify the logged-in user, e.g., through a session or token
    user_id = request.args.get('user_id')  # You might get this from a session or token in a real scenario

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Fetch the status from the application table
    response = supabase.table('application').select('status').eq('user_id', user_id).execute()

    if response.data:
        return jsonify({"status": response.data[0]['status']}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@unlicensedminer_bp.route('/announcements', methods=['GET'])
def get_announcements():
    user_id = request.args.get('user_id')  # from a session or token

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Fetch announcements from the comments table
    response = supabase.table('comments').select('announcement').eq('user_id', user_id).execute()

    if response.data:
        announcements = [item['announcement'] for item in response.data]
        return jsonify({"announcements": announcements}), 200
    else:
        return jsonify({"error": "No announcements found"}), 404

def init_routes(bp):
    bp.route('/status', methods=['GET'])(get_user_status)
    bp.route('/announcements', methods=['GET'])(get_announcements)
