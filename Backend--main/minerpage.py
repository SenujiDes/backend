from flask import Blueprint, jsonify, request
from supabase import create_client, Client
from config import Config
from datetime import datetime, timedelta

# Create a Blueprint for miner-related routes
minerpage_bp = Blueprint('minerpage', __name__, url_prefix='/miner')

# Initialize Supabase client
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

# Function to calculate expiration date based on period_of_validation
def calculate_expiration_date(start_date, period_of_validation):
    years = int(period_of_validation.split()[0])  # Extract the number of years
    expiration_date = start_date + timedelta(days=365 * years)  # Add years to the start date
    return expiration_date

# Endpoint to fetch license status, license number, and expiry date
@minerpage_bp.route('/license', methods=['GET'])
def get_license():
    try:
        # Get the user_id from the Supabase session
        session = supabase.auth.session()
        if not session:
            return jsonify({"error": "User not authenticated"}), 401

        user_id = session.user.id

        # Fetch license status from the 'users' table
        user_response = supabase.table('users').select("license_status, active_date").eq('userId', user_id).execute()
        if not user_response.data:
            return jsonify({"error": "User not found"}), 404

        user_data = user_response.data[0]
        license_status = user_data['license_status']
        active_date_str = user_data.get('active_date')

        # Fetch exploration_license_no and period_of_validation from the 'application' table
        application_response = supabase.table('application').select("exploration_license_no, period_of_validation").eq('userId', user_id).execute()
        if not application_response.data:
            return jsonify({"error": "No application found for the user"}), 404

        application_data = application_response.data[0]
        exploration_license_no = application_data['exploration_license_no']
        period_of_validation = application_data.get('period_of_validation', '1 yr')  # Default to 1 year if not provided

        # Calculate expiry date
        if active_date_str:
            active_date = datetime.strptime(active_date_str, '%Y-%m-%d')
            expiry_date = calculate_expiration_date(active_date, period_of_validation)
        else:
            return jsonify({"error": "Active date is not available"}), 400

        return jsonify({
            "license_status": license_status,
            "license_number": exploration_license_no,
            "active_date": active_date_str,
            "period_of_validation": period_of_validation,
            "expires": expiry_date.strftime('%Y-%m-%d')  # Format expiry date
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch royalty amount due
@minerpage_bp.route('/royalty', methods=['GET'])
def get_royalty():
    try:
        # Get the user_id from the Supabase session
        session = supabase.auth.session()
        if not session:
            return jsonify({"error": "User not authenticated"}), 401

        user_id = session.user.id

        # Fetch total_royalty from the 'royalty' table
        royalty_response = supabase.table('royalty').select("total_royalty").eq('userId', user_id).execute()
        if not royalty_response.data:
            return jsonify({"error": "No royalty data found for the user"}), 404

        royalty_data = royalty_response.data[0]
        royalty_amount_due = royalty_data['total_royalty']

        return jsonify({
            "royalty_amount_due": royalty_amount_due
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch recent announcements
@minerpage_bp.route('/announcements', methods=['GET'])
def get_announcements():
    try:
        # Fetch data from the 'comments' table, ordered by creation date in descending order
        response = supabase.table('comments').select("text").order('created_at', desc=True).execute()
        announcements = [item['text'] for item in response.data]
        return jsonify({"announcements": announcements})
        # announcements = response.data
        # return jsonify(announcements)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# # Debugging announcements
# @minerpage_bp.route('/announcements', methods=['GET'])
# def get_announcements():
#     try:
#         print("Attempting to fetch announcements...")  # Debug point 1
        
#         # Fetch only the 'text' column from the 'comments' table
#         response = supabase.table('comments').select("text").order('created_at', desc=True).execute()
        
#         print("Raw database response:", response)  # Debug point 2
#         print("Response data:", response.data)    # Debug point 3
        
#         # Extract just the text values from the response
#         announcements = [item['text'] for item in response.data if item.get('text')]
        
#         print("Processed announcements:", announcements)  # Debug point 4
        
#         return jsonify({
#             "success": True,
#             "announcements": announcements,
#             "count": len(announcements)
#         })
#     except Exception as e:
#         print("Error fetching announcements:", str(e))  # Debug point 5
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500

# Function to initialize routes
def init_routes(bp):
    bp.add_url_rule('/license', view_func=get_license)
    bp.add_url_rule('/royalty', view_func=get_royalty)
    bp.add_url_rule('/announcements', view_func=get_announcements)
