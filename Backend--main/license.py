from flask import jsonify, request, current_app
import os
from werkzeug.utils import secure_filename
import logging
import re

# Define the allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, folder):
    """Save an uploaded file to the specified folder."""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder, filename)
        try:
            file.save(file_path)
            return file_path
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return None
    return None

def clean_numeric_value(value):
    """Clean numeric values by removing special characters and units."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Remove common units and special characters
        value = value.lower().strip()
        value = value.replace(',', '')  # Remove commas
        value = value.replace('usd', '')  # Remove currency
        value = value.replace('$', '')
        value = value.replace('tons/day', '')
        value = value.replace('m', '')  # Remove meters
        value = value.replace('%', '')
        value = value.replace('years', '')
        value = value.replace('year', '')
        value = value.strip()
        # Extract the first number found
        number_match = re.search(r'[\d.]+', value)
        if number_match:
            try:
                return float(number_match.group())
            except (ValueError, TypeError):
                return None
    return None

def init_routes(bp):
    @bp.route('/submit', methods=['POST'])
    def submit_license():
        try:
            # Create a folder to store uploaded files
            upload_folder = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)

            # Get form data or JSON data
            if request.is_json:
                data = request.get_json()
                form_data = {
                    "exploration_license_no": data.get('exploration_license_no'),
                    "applicant_name": data.get('applicant_name'),
                    "national_id": data.get('national_id'),
                    "address": data.get('address'),
                    "nationality": data.get('nationality'),
                    "employment": data.get('employment'),
                    "place_of_business": data.get('place_of_business'),
                    "residence": data.get('residence'),
                    "company_name": data.get('company_name'),
                    "country_of_incorporation": data.get('country_of_incorporation'),
                    "head_office_address": data.get('head_office_address'),
                    "registered_address_in_sri_lanka": data.get('registered_address_in_sri_lanka'),
                    "capitalization": clean_numeric_value(data.get('capitalization')),
                    "blasting_method": data.get('blasting_method'),
                    "depth_of_borehole": clean_numeric_value(data.get('depth_of_borehole')),
                    "production_volume": clean_numeric_value(data.get('production_volume')),
                    "machinery_used": data.get('machinery_used'),
                    "underground_mining_depth": clean_numeric_value(data.get('underground_mining_depth')),
                    "explosives_type": data.get('explosives_type'),
                    "land_name": data.get('land_name'),
                    "land_owner_name": data.get('land_owner_name'),
                    "village_name": data.get('village_name'),
                    "grama_niladhari_division": data.get('grama_niladhari_division'),
                    "divisional_secretary_division": data.get('divisional_secretary_division'),
                    "administrative_district": data.get('administrative_district'),
                    "nature_of_bound": data.get('nature_of_bound'),
                    "minerals_to_be_mined": data.get('minerals_to_be_mined'),
                    "industrial_mining_license_no": data.get('industrial_mining_license_no'),
                    "period_of_validity": clean_numeric_value(data.get('period_of_validity')),
                    "royalty_payable": clean_numeric_value(data.get('royalty_payable')),
                    "articles_of_association": data.get('articles_of_association'),
                    "annual_reports": data.get('annual_reports'),
                    "licensed_boundary_survey": data.get('licensed_boundary_survey'),
                    "project_team_credentials": data.get('project_team_credentials'),
                    "economic_viability_report": data.get('economic_viability_report'),
                    "mine_restoration_plan": data.get('mine_restoration_plan'),
                    "license_fee_receipt": data.get('license_fee_receipt'),
                    "applicant_signature": data.get('applicant_signature'),
                    "mine_manager_signature": data.get('mine_manager_signature'),
                    "director_general_signature": data.get('director_general_signature')
                }
            else:
                form_data = {
                    "exploration_license_no": request.form.get('exploration_license_no'),
                    "applicant_name": request.form.get('applicant_name'),
                    "national_id": request.form.get('national_id'),
                    "address": request.form.get('address'),
                    "nationality": request.form.get('nationality'),
                    "employment": request.form.get('employment'),
                    "place_of_business": request.form.get('place_of_business'),
                    "residence": request.form.get('residence'),
                    "company_name": request.form.get('company_name'),
                    "country_of_incorporation": request.form.get('country_of_incorporation'),
                    "head_office_address": request.form.get('head_office_address'),
                    "registered_address_in_sri_lanka": request.form.get('registered_address_in_sri_lanka'),
                    "capitalization": clean_numeric_value(request.form.get('capitalization')),
                    "blasting_method": request.form.get('blasting_method'),
                    "depth_of_borehole": clean_numeric_value(request.form.get('depth_of_borehole')),
                    "production_volume": clean_numeric_value(request.form.get('production_volume')),
                    "machinery_used": request.form.get('machinery_used'),
                    "underground_mining_depth": clean_numeric_value(request.form.get('underground_mining_depth')),
                    "explosives_type": request.form.get('explosives_type'),
                    "land_name": request.form.get('land_name'),
                    "land_owner_name": request.form.get('land_owner_name'),
                    "village_name": request.form.get('village_name'),
                    "grama_niladhari_division": request.form.get('grama_niladhari_division'),
                    "divisional_secretary_division": request.form.get('divisional_secretary_division'),
                    "administrative_district": request.form.get('administrative_district'),
                    "nature_of_bound": request.form.get('nature_of_bound'),
                    "minerals_to_be_mined": request.form.get('minerals_to_be_mined'),
                    "industrial_mining_license_no": request.form.get('industrial_mining_license_no'),
                    "period_of_validity": request.form.get('period_of_validity'),
                    "royalty_payable": clean_numeric_value(request.form.get('royalty_payable'))
                }

                # Handle file uploads
                file_fields = [
                    'articles_of_association', 'annual_reports', 'licensed_boundary_survey',
                    'project_team_credentials', 'economic_viability_report', 'mine_restoration_plan',
                    'license_fee_receipt', 'applicant_signature', 'mine_manager_signature',
                    'director_general_signature'
                ]

                for field in file_fields:
                    file = request.files.get(field)
                    if file:
                        file_path = save_file(file, upload_folder)
                        form_data[field] = file_path
                    else:
                        form_data[field] = None

            # Validate required fields
            required_fields = [
                'exploration_license_no', 'applicant_name', 'national_id', 'address', 'nationality',
                'employment', 'place_of_business', 'residence', 'company_name', 'country_of_incorporation',
                'head_office_address', 'registered_address_in_sri_lanka', 'capitalization',
                'blasting_method', 'depth_of_borehole', 'production_volume', 'machinery_used',
                'underground_mining_depth', 'explosives_type', 'land_name', 'land_owner_name',
                'village_name', 'grama_niladhari_division', 'divisional_secretary_division',
                'administrative_district', 'nature_of_bound', 'minerals_to_be_mined',
                'industrial_mining_license_no', 'period_of_validity', 'royalty_payable'
            ]

            for field in required_fields:
                if field not in form_data or form_data[field] is None:
                    return jsonify({"error": f"Missing or invalid field: {field}"}), 400

            # Insert data into Supabase
            supabase = current_app.supabase
            response = supabase.table('application').insert(form_data).execute()

            return jsonify({"message": "License submitted successfully!", "data": response.data}), 201
        except Exception as e:
            logging.error(f"Error in submit_license: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @bp.route('/get', methods=['GET'])
    def get_licenses():
        try:
            supabase = current_app.supabase
            # Fetch data from Supabase
            response = supabase.table('application').select('*').execute()
            return jsonify(response.data), 200
        except Exception as e:
            logging.error(f"Error in get_licenses: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500