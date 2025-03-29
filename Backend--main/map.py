from flask import jsonify, current_app

def init_routes(bp):
    @bp.route('/get', methods=['GET'])
    def get_locations():
        try:
            # Fetch data from Supabase
            supabase = current_app.supabase
            response = supabase.table('locations').select('*').execute()
            locations = response.data

            # Convert to a list of dictionaries (if needed)
            locations_list = []
            for location in locations:
                locations_list.append({
                    'id': location['id'],
                    'name': location['name'],
                    'latitude': float(location['latitude',0]),
                    'longitude': float(location['longitude',0]),
                    'description': location['description',''],
                    'image': location['image',''],
                    'longDes': location['longDes',''],
                })

            print("Returning locations:", locations_list)  # Debugging output

            return jsonify(locations_list)
        except Exception as e:
            return jsonify({"error": str(e)}), 500