from flask import Flask,render_template, request, redirect,url_for
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="Project")


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html', warning = "")

@app.route('/showLogin')
def showLogin():
    return render_template('login.html', warning = "")


@app.route('/signUp',methods=["POST"])
def signUp():
    username = str(request.form["user"])
    password = str(request.form["password"])
    email = str(request.form["email"])

    cursor1 = conn.cursor()
    cursor1.execute("SELECT * FROM tbl_user WHERE user_username ='"+email+"'")
    x = cursor1.fetchone()

    if x is None:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_user(user_name,user_username,user_password)VALUES(%s,%s,%s)",(username,email,password))
        conn.commit()
        return render_template('login.html',warning = "")
    else:
        return render_template('signup.html', warning = "That username seems to be taken! Try another one!")


@app.route("/login",methods=["POST"])
def login():
    password = str(request.form["password"])
    email = str(request.form["email"])

    cursor1 = conn.cursor()
    cursor1.execute("SELECT * FROM tbl_user WHERE user_username ='"+email+"'"+"AND user_password = '"+password+"'")
    x = cursor1.fetchone()

    if x is None:
        return render_template('login.html', warning = "Invalid credentials!")
    else:
        return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')
    
        

if __name__=="__main__":
    app.run(debug=True)


