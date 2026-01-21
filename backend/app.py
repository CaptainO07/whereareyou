from flask import Flask,render_template,redirect,url_for,request
app=Flask(__name__)
@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        return redirect(url_for('welcome'))
    return render_template('home.html')
@app.route("/welcome")
def welcome():
    return render_template('welcome.html')
if __name__=='__main__':
    app.run(debug=True,threaded=True)

 
