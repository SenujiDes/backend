from flask import jsonify, request, current_app
import logging
import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def init_routes(bp):

    @bp.route('/get', methods=['GET'])
    def get_royalties():
        try:
            supabase = current_app.supabase
            # Fetch data from Supabase
            response = supabase.table('royalty').select('*').execute()
            return jsonify(response.data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    @bp.route('/calculate', methods=['POST'])
    def calculate_royalty():
        try:
            # Log the start of the function
            logging.debug("Starting calculate_royalty function")

            # Get JSON data from the request
            data = request.json
            logging.debug(f"Received data: {data}")

            # Extract and validate input values
            if 'water_gel' not in data or 'nh4no3' not in data or 'powder_factor' not in data:
                logging.error("Missing required input fields")
                return jsonify({"error": "Missing required fields: water_gel, nh4no3, powder_factor"}), 400

            water_gel = float(data['water_gel'])
            nh4no3 = float(data['nh4no3'])
            powder_factor = float(data['powder_factor'])

            # Validate positive values
            if water_gel < 0 or nh4no3 < 0 or powder_factor <= 0:
                logging.error("Values must be positive")
                return jsonify({"error": "Values must be greater than zero"}), 400

            # Calculate royalty values
            # 1. Calculate total explosive quantity
            total_explosive_quantity = water_gel + nh4no3
            
            # 2. Calculate blasted rock volume
            # Assuming powder_factor = total_explosive_quantity / rock_volume
            # So rock_volume = total_explosive_quantity / powder_factor
            blasted_rock_volume = total_explosive_quantity / powder_factor if powder_factor > 0 else 0
            
            # 3. Calculate base royalty (assuming a rate of 50 LKR per cubic meter)
            royalty_rate_per_cubic_meter = 50.0
            base_royalty = blasted_rock_volume * royalty_rate_per_cubic_meter
            
            # 4. Apply SSCL (Social Security Contribution Levy) - assuming 2.5%
            sscl_rate = "2.5%"
            sscl_value = base_royalty * 0.025
            royalty_with_sscl = base_royalty + sscl_value
            
            # 5. Apply VAT - assuming 15%
            vat_rate = "15%"
            vat_value = royalty_with_sscl * 0.15
            total_amount_with_vat = royalty_with_sscl + vat_value

            # Create response in the format expected by the frontend
            result = {
                "calculation_date": datetime.datetime.now().isoformat(),
                "inputs": {
                    "water_gel_kg": water_gel,
                    "nh4no3_kg": nh4no3,
                    "powder_factor": powder_factor
                },
                "calculations": {
                    "total_explosive_quantity": total_explosive_quantity,
                    "basic_volume": blasted_rock_volume,  # Basic volume is the same as blasted rock volume
                    "blasted_rock_volume": blasted_rock_volume,
                    "base_royalty": base_royalty,
                    "royalty_with_sscl": royalty_with_sscl,
                    "total_amount_with_vat": total_amount_with_vat
                },
                "rates_applied": {
                    "royalty_rate_per_cubic_meter": royalty_rate_per_cubic_meter,
                    "sscl_rate": sscl_rate,
                    "vat_rate": vat_rate
                }
            }

            # Store the calculation in the database
            try:
                supabase = current_app.supabase
                supabase.table('royalty').insert({
                    'water_gel': water_gel,
                    'nh4no3': nh4no3,
                    'powder_factor': powder_factor,
                    'total_explosive_quantity': total_explosive_quantity,
                    'blasted_rock_volume': blasted_rock_volume,
                    'base_royalty': base_royalty,
                    'royalty_with_sscl': royalty_with_sscl,
                    'total_amount': total_amount_with_vat,
                    'calculation_date': datetime.datetime.now().isoformat()
                }).execute()
                logging.debug("Calculation stored in database")
            except Exception as db_error:
                # Just log the error but continue the function
                logging.error(f"Error storing calculation in database: {db_error}")

            # Return the calculation result to the frontend
            return jsonify(result), 200

        except Exception as e:
            # Log the full error with traceback
            logging.error(f"Error in calculate_royalty: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500