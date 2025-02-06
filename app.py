import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import PIL.Image
import io

# Initialize the Flask app
app = Flask(__name__)

# Configure the AI model
api_key = "AIzaSyBxg2Vzurrs7giquvhPlghaxZO0ya2MdK8"  # Replace with actual key
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Load sample images
sample_file_2 = PIL.Image.open('circuit.png')
sample_file_3 = PIL.Image.open('firefighter.jpg')

# Function to encode images in binary format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()

@app.route("/")
def home():
    return render_template("index.html")  # Serve a basic HTML form for interaction

@app.route("/ask", methods=["POST"])
def ask_image():
    image_choice = request.form.get("image_choice")
    query = request.form.get("query")

    # Select the correct image based on user choice
    if image_choice == "circuit":
        selected_image = sample_file_2
    elif image_choice == "firefighter":
        selected_image = sample_file_3
    else:
        return jsonify({"error": "Invalid image choice! Please choose 'circuit' or 'firefighter'."})

    # Convert the image to binary format
    selected_image_binary = encode_image(selected_image)

    # Generate the AI response
    response = model.generate_content([
        {"mime_type": "image/jpeg", "data": selected_image_binary},
        query
    ])

    # Return the AI response as JSON
    return jsonify({"ai_response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
