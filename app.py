from flask import Flask,render_template,request

app=Flask(__name__)

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

if __name__=='__main__':
    app.run(debug=True)

