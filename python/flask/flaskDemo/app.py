from flask import Flask, render_template, request, session
import requests
import re

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for session support

# 🔧 Bot reply cleaner
def extract_first_answer(text):
    text = text.strip()

    # Remove "Bot:" or "Assistant:" anywhere
    text = re.sub(r'\b(Bot|Assistant)\s*:\s*', '', text, flags=re.IGNORECASE)

    # Remove leading tags like "OUTPUT:", "Answer:", etc.
    text = re.sub(r'^(OUTPUT|Answer)\s*:\s*', '', text, flags=re.IGNORECASE)

    # Extract structured tag content
    for tag in ['RESULT', 'INST', 'ANS']:
        match = re.search(rf'\[{tag}\](.*?)\[/\s*{tag}\]', text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Clean up junky tag artifacts
    text = re.sub(r'#?\*\[.*?\]', '', text)

    # Fallback: first sentence or line
    sentence = re.split(r'[.!?]', text)[0]
    return sentence.strip()

# 🔹 Home route
@app.route('/')
def home():
    return render_template('home.html')

# 🔹 About route
@app.route('/about')
def about():
    return "This is a simple Flask app."

# 🔹 Debug route
@app.route('/debug')
def debug():
    return "This is the debug route. Everything's (hopefully) fine."

# 🔹 Chat route
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        user_message = request.form['message']

        # Call the bot backend
        try:
            api_response = requests.post(
                'http://34.135.90.197/chat',
                json={'message': user_message}
            )
            if api_response.status_code == 200:
                data = api_response.json()
                raw_reply = data.get('reply', "The bot didn't say anything.")
                bot_reply = extract_first_answer(raw_reply)
            else:
                bot_reply = f"Bot server error: {api_response.status_code}"
        except Exception as e:
            bot_reply = f"Error: {e}"

        # Append to chat history
        session['history'].append({'user': user_message, 'bot': bot_reply})
        session.modified = True

    return render_template('chat.html', history=session.get('history', []))

# 🔹 Clear chat history
@app.route('/clear')
def clear():
    session.pop('history', None)
    return render_template('chat.html', history=[])

# 🔹 Run app
if __name__ == '__main__':
    app.run(debug=True)
