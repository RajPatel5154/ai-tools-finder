from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__, template_folder="templates")

# ✅ Set OpenAI API key directly inside the client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "OPEN AI API KEY")  # Replace with your key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')

    try:
        # ✅ Pass the API key when creating the client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)  

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an AI tool finder. Based on the user's query, return a helpful and structured list of relevant AI tools in clean HTML format. For each tool, include a clickable name linking to the official site, a short description, and a list of 3-5 key features using HTML tags only (h3, a, p, ul, li)."},
                {"role": "user", "content": query}
            ]
        )

        # Extract response
        tools = response.choices[0].message.content

    except Exception as e:
        tools = f"Error: {str(e)}"

    return jsonify({"tools": tools})

if __name__ == '__main__':
    app.run(debug=True)
