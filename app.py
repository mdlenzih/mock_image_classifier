from flask import Flask, request, jsonify
from mock_model import MockModel
import base64
from io import BytesIO

# Initialize Flask application
app = Flask(__name__)

# Initialize the mock model that will handle image processing and prediction
model = MockModel()

@app.route("/predict", methods=["POST"])
def predict():
    """
    Handle image upload and return prediction results.
    
    This endpoint accepts:
    1. Multipart form data with a file in the 'file' field
    2. JSON with a base64-encoded image in the 'file' field
    
    Returns:
        JSON response with prediction or error message
    """
    try:
        # Check if it's a file upload
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"error": "No file selected"}), 400
            processed_img = model.preprocess(file)
            
        # Check if it's a base64-encoded image
        elif request.is_json and "file" in request.json:
            try:
                # Decode base64 image
                image_data = base64.b64decode(request.json["file"])
                file = BytesIO(image_data)
                processed_img = model.preprocess(file)
            except Exception as e:
                return jsonify({"error": "Invalid base64 image data"}), 400
                
        else:
            return jsonify({"error": "No image data provided"}), 400
            
        # Get prediction
        prediction = model.predict(processed_img)
        return jsonify({"prediction": prediction})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
