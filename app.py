from flask import Flask,render_template,request,session,jsonify
import os
from dotenv import load_dotenv
import uuid
import google.generativeai as genai

app=Flask(__name__)
app.secret_key='mu_secret_key'#change this to some strong key in production phase

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
model=genai.GenerativeModel("gemini-1.5-flash")

chat_session={}

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/interview',methods=['GET', 'POST'])
def environment():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
    
    return render_template('envr.html')

@app.route('/interview/environment',methods=['POST'])
def question_generation():
    data=request.get_json()
    user_message=data['message']

    try:
        if 'chat_id' not in session:
            session['chat_id']=str(uuid.uuid4())
        
        chat_id=session['chat_id']
        if chat_id not in chat_session:
            chat=model.start_chat(history=[])
            chat.send_message(
                "You are a technical interviewer. Conduct a realistic mock interview. "
                "Ask one question at a time and wait for the candidate to respond before continuing. "
                "Ask two DSA questions: one easy, one medium."
                "give small responses"
                )

            chat_session[chat_id]=chat

        chat=chat_session[chat_id]
        response=chat.send_message(user_message)
        reply=response.text.strip()
        return  jsonify({"reply":reply})
    
    except Exception as e:
        return jsonify({"reply":f"error{str(e)}"})
    
@app.route('/interview/evaluate', methods=['POST'])
def evaluate_code():
    data = request.get_json()
    code = data['code']

    try:
        if 'chat_id' not in session:
            session['chat_id'] = str(uuid.uuid4())

        chat_id = session['chat_id']
        if chat_id not in chat_session:
            chat = model.start_chat(history=[])
            chat_session[chat_id] = chat

        chat = chat_session[chat_id]

        # Prepare a prompt for evaluation
        eval_prompt = (
            "Evaluate the following code as a technical interviewer. "
            "Check for correctness, edge case handling, if logic correct then ask the candidate to discuss time and space complexity. "
            "Suggest improvements if any.\n\n"
            "give short responses"
            f"```\n{code}\n```"
        )

        response = chat.send_message(eval_prompt)
        reply = response.text.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__=='__main__':
    app.run(debug=True)

