# # from flask import jsonify, request, current_app
# # import logging

# # # Configure logging
# # logging.basicConfig(level=logging.DEBUG)
# # logger = logging.getLogger(__name__)

# # def init_routes(bp):
# #     @bp.route('/submit', methods=['POST'])
# #     def submit_contact():
# #         try:
# #             data = request.json
# #             supabase = current_app.supabase

# #             # Log the received data for debugging
# #             logger.debug(f"Received data: {data}")

# #             # Prepare the data for insertion
# #             contact_data = {
# #                 'name': data.get('name'),
# #                 'email': data.get('email'),
# #                 'phone': data.get('phone', None),  # Optional field
# #                 'subject': data.get('subject', None),  # Optional field
# #                 'message': data.get('message')
# #             }

# #             # Insert data into Supabase
# #             response = supabase.table('contact_data').insert(contact_data).execute()

# #             # Log the response from Supabase
# #             logger.debug(f"Supabase response: {response}")

# #             # Check if the response contains data (indicates success)
# #             if response.data:
# #                 return jsonify({
# #                     "message": "Contact message submitted successfully!",
# #                     "data": response.data
# #                 }), 201
# #             else:
# #                 logger.error(f"Supabase error: No data returned")
# #                 return jsonify({
# #                     "error": "Failed to submit contact message",
# #                     "details": "No data returned from Supabase"
# #                 }), 500

# #         except Exception as e:
# #             # Log the error
# #             logger.error(f"Error submitting contact message: {e}")
# #             return jsonify({"error": str(e)}), 500

# #     @bp.route('/get', methods=['GET'])
# #     def get_contacts():
# #         try:
# #             supabase = current_app.supabase
# #             # Fetch data from Supabase
# #             response = supabase.table('contact_data').select('*').execute()

# #             # Log the fetched data for debugging
# #             logger.debug(f"Fetched contacts: {response.data}")

# #             # Check if the response contains data (indicates success)
# #             if response.data:
# #                 return jsonify(response.data), 200
# #             else:
# #                 logger.error(f"Supabase error: No data returned")
# #                 return jsonify({
# #                     "error": "Failed to fetch contacts",
# #                     "details": "No data returned from Supabase"
# #                 }), 500

# #         except Exception as e:
# #             # Log the error
# #             logger.error(f"Error fetching contacts: {e}")
# #             return jsonify({"error": str(e)}), 500


# from flask import jsonify, request, current_app
# import logging
# from datetime import datetime

# # Set up logging
# logging.basicConfig(
#     level=logging.DEBUG,  # Set the logging level to DEBUG
#     format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
#     handlers=[
#         logging.FileHandler('app.log'),  # Log to a file
#         logging.StreamHandler()  # Log to the console
#     ]
# )

# def init_routes(bp):
#     @bp.route('/submit', methods=['POST'])
#     def submit_complaint():
#         try:
#             # Log the start of the function
#             logging.info("Starting submit_complaint function")

#             # Log the incoming request data
#             data = request.json
#             logging.debug(f"Received data: {data}")

#             # Validate required fields
#             required_fields = ['email', 'project', 'complaint_text']
#             if not all(field in data for field in required_fields):
#                 logging.error("Missing required fields in request")
#                 return jsonify({"error": "Missing required fields"}), 400

#             # Insert data into Supabase
#             supabase = current_app.supabase
#             response = supabase.table('complaints').insert({
#                 'email': data['email'],
#                 'project': data['project'],
#                 'complaint_text': data['complaint_text']
#             }).execute()

#             # Log the successful submission
#             logging.info("Complaint submitted successfully")
#             return jsonify({"message": "Complaint submitted successfully!", "data": response.data}), 201

#         except Exception as e:
#             # Log the error with traceback
#             logging.error(f"Error in submit_complaint: {e}", exc_info=True)
#             return jsonify({"error": str(e)}), 500

#     @bp.route('/get', methods=['GET'])
#     def get_complaints():
#         try:
#             # Log the start of the function
#             logging.info("Starting get_complaints function")

#             # Fetch data from Supabase
#             supabase = current_app.supabase
#             response = supabase.table('complaints').select('*').execute()

#             # Log the successful fetch
#             logging.info("Complaints fetched successfully")
#             return jsonify(response.data), 200

#         except Exception as e:
#             # Log the error with traceback
#             logging.error(f"Error in get_complaints: {e}", exc_info=True)
#             return jsonify({"error": str(e)}), 500


from flask import jsonify, request, current_app
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def init_routes(bp):
    @bp.route('/submit', methods=['POST'])
    def submit_complaint():
        try:
            # Log the start of the function
            logging.info("Starting submit_complaint function")

            # Log the incoming request data
            data = request.json
            logging.debug(f"Received data: {data}")

            # Validate required fields
            required_fields = ['email', 'project', 'complaint_text']
            if not all(field in data for field in required_fields):
                logging.error("Missing required fields in request")
                return jsonify({
                    "status_code": 400,
                    "error": "Missing required fields"
                }), 400

            # Insert data into Supabase
            supabase = current_app.supabase
            response = supabase.table('complaints').insert({
                'email': data['email'],
                'project': data['project'],
                'complaint_text': data['complaint_text']
            }).execute()

            # Log the successful submission
            logging.info("Complaint submitted successfully")
            return jsonify({
                "status_code": 201,
                "message": "Complaint submitted successfully!",
                "data": response.data
            }), 201

        except Exception as e:
            # Log the error with traceback
            logging.error(f"Error in submit_complaint: {e}", exc_info=True)
            return jsonify({
                "status_code": 500,
                "error": str(e)
            }), 500

    @bp.route('/get', methods=['GET'])
    def get_complaints():
        try:
            # Log the start of the function
            logging.info("Starting get_complaints function")

            # Fetch data from Supabase
            supabase = current_app.supabase
            response = supabase.table('complaints').select('*').execute()

            # Log the successful fetch
            logging.info("Complaints fetched successfully")
            return jsonify({
                "status_code": 200,
                "data": response.data
            }), 200

        except Exception as e:
            # Log the error with traceback
            logging.error(f"Error in get_complaints: {e}", exc_info=True)
            return jsonify({
                "status_code": 500,
                "error": str(e)
            }), 500