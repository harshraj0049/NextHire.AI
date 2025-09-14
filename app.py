from flask import Flask,render_template,request,session,jsonify,flash,redirect,url_for
import os
from dotenv import load_dotenv
import uuid
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
model=genai.GenerativeModel("gemini-2.5-flash")

app.secret_key='mu_secret_key'#change this to some strong key in production phase


#database connection 
def init_db():
    conn=psycopg2.connect(
                        host="localhost",
                        database="demo_learn",
                        user="postgres",
                        password=os.getenv("POSTGRES_PASS"),
                        port="5432"
                    
    )
    #creating a cursor
    cur=conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS signin_users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15) UNIQUE NOT NULL,
            password_hash VARCHAR(200) NOT NULL   
        );''')

    conn.commit()

    cur.close()
    conn.close()


@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone=request.form.get('phone')
        password=request.form.get('password')

        password_hash=generate_password_hash(password)

        insert_query=''' INSERT INTO signin_users (username,email,password_hash,phone) VALUES(%s,%s,%s,%s)'''

        try:
            conn=psycopg2.connect(
                    host="localhost",
                    database="demo_learn",
                    user="postgres",
                    password=os.getenv("POSTGRES_PASS"),
                    port="5432")
            cur=conn.cursor()  
            cur.execute(insert_query,(name,email,password_hash,phone))

            conn.commit()

            cur.close()
            conn.close()
            return render_template('envr.html')
        except Exception as e:
            return f"An error occurred: {e}"
        
    return render_template('envr.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password=request.form.get('password')

        conn=psycopg2.connect(
                    host="localhost",
                    database="demo_learn",
                    user="postgres",
                    password=os.getenv("POSTGRES_PASS"),
                    port="5432")
        cur=conn.cursor()
        cur.execute("SELECT id, username, password_hash FROM signin_users WHERE email = %s",
                    (email,))
        user = cur.fetchone()#returns a tuple with one row that is selected

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]       # store id in session
            session['username'] = user[1]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('envr.html'))  # or any page you want
        else:
            flash('Invalid email or password', 'error')

    return render_template('envr.html')



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
    init_db()
    app.run(debug=True)

