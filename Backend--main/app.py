import os
from flask import Flask, jsonify
from flask_cors import CORS
from __init__ import create_app

app = create_app()

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "https://your-frontend-domain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Ceylonmine Backend!'
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    # Add SSL context if you have certificates
    ssl_context = None
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        ssl_context = ('cert.pem', 'key.pem')
    
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=True,
        ssl_context=ssl_context
    )




