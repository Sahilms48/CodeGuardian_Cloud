from flask import Flask, jsonify, request
from google.cloud import storage
from llama_cpp import Llama
import os

app = Flask(__name__)

# Set Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/service_account.json"

# GCP bucket details
BUCKET_NAME = "custommodel_github"  # Replace with your bucket name
MODEL_FILE_NAME = "model007.gguf"

def download_model():
    """
    Downloads the .gguf file from the GCP bucket into the container.
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_FILE_NAME)

        local_path = f"/app/{MODEL_FILE_NAME}"
        blob.download_to_filename(local_path)
        return local_path
    except Exception as e:
        print(f"Error downloading model: {e}")
        return None

# Download the model at container startup
MODEL_PATH = download_model()
if not MODEL_PATH or not os.path.exists(MODEL_PATH):
    raise RuntimeError("Failed to download the model file during container initialization.")

def load_model(model_path):
    """
    Loads the .gguf model using llama-cpp-python.
    """
    try:
        # Load LLaMA model with given .gguf file
        model = Llama(model_path=model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

MODEL = load_model(MODEL_PATH)

@app.route("/check-model", methods=["GET"])
def check_model():
    """
    API to check if the model file exists in the container.
    """
    if os.path.exists(MODEL_PATH):
        return jsonify({"message": f"Model file {MODEL_FILE_NAME} is available at {MODEL_PATH}!"})
    else:
        return jsonify({"error": "Model file not found in container."}), 404

@app.route("/predict", methods=["POST"])
def predict():
    """
    API endpoint to make predictions using the model.
    """
    try:
        prompt = request.get_data(as_text=True).strip()
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Generate text with the model
        # Adjust parameters as needed (max_tokens, temperature, top_k, etc.)
        response = MODEL(
            prompt=prompt,
            max_tokens=100000000000000000000
        )

        # 'response' is a dictionary returned by llama_cpp
        # The generated text is usually in response["choices"][0]["text"]
        output_text = response["choices"][0]["text"]

        return output_text
    except Exception as e:
        return jsonify({"error": f"Failed to make prediction: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
