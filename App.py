from flask import Flask, request, jsonify
from openai import OpenAI
import json
from flask_cors import CORS

client = OpenAI(
	base_url="https://router.huggingface.co/hf-inference/v1",
	api_key="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"
)

app = Flask(__name__)
CORS(app)

# Load the JSON data (In real implementation, this could be from a database)
with open("rawdata.json", "r") as file:
    performance_data = json.load(file)

#openai.api_key = "your-openai-api-key"  # Replace with your API Key

def generate_performance_summary(data):
    prompt = f"""
    The student has taken a CAT exam. Below is their performance data:
    
    **Overall Performance:**
    - Score: {data['overall']['score']}
    - Accuracy: {data['overall']['accuracy']}
    - Attempts: {data['overall']['attempts']}/{data['overall']['questions']}
    - Time Spent: {data['overall']['timeSpent']} hours
    
    **Section-wise Analysis:**
    - **VARC**: {data['varc']['accuracy']} Accuracy
    - **DILR**: {data['dilr']['accuracy']} Accuracy
    - **QA**: {data['qa']['accuracy']} Accuracy
    
    **Question Selection Strategy:**
    - VARC: Easy ({data['varc']['selection']['easy']['correct']} Correct, {data['varc']['selection']['easy']['incorrect']} Incorrect, {data['varc']['selection']['easy']['skipped']} Skipped)
    - DILR: Medium ({data['dilr']['selection']['medium']['correct']} Correct, {data['dilr']['selection']['medium']['incorrect']} Incorrect, {data['dilr']['selection']['medium']['skipped']} Skipped)
    - QA: Hard ({data['qa']['selection']['hard']['correct']} Correct, {data['qa']['selection']['hard']['incorrect']} Incorrect, {data['qa']['selection']['hard']['skipped']} Skipped)
    
    **Improvement Areas:**
    - Identify sections with the lowest accuracy and provide actionable steps for improvement.
    
    Provide a detailed, bullet-pointed analysis focusing on Accuracy, Question Selection Strategy, and Improvement Areas.
    """
    
    try:
        response = client.ChatCompletion.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "system", "content": "You are an educational performance analyst."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

@app.route("/http://192.168.117.17:5500/api/summary", methods=["GET"])
def get_summary():
    summary = generate_performance_summary(performance_data)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
