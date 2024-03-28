from flask import Flask,render_template,url_for,request,redirect,flash,session
import mysql.connector
from cmail import sendmail
from otp import genotp
app=Flask(__name__)
#secret key
app.config['SECRET_KEY']="my super secret key that no one is supposed to Know"
mydb=mysql.connector.connect(host="localhost",user="root",password="system",db="blog")
with mysql.connector.connect(host="localhost",user="root",password="system",db="blog"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists reg(username varchar(50) primary key,mobile  varchar(10) unique,email varchar(50) unique,address varchar(250),password varchar(20))")
    
mycursor=mydb.cursor()
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/home")
def home():
    return "login successfully"
@app.route("/error")
def error():
    return "invalide username and password"

@app.route("/reg",methods=["GET","POST"])
def reg():
    if request.method=="POST":
        username=request.form.get("username")
        mobile =request.form.get("mobile")
        email =request.form.get("email")
        address=request.form.get("address")
        password =request.form.get("password")
        print(username,mobile,email,address,password)
        otp=genotp()
        sendmail(to=email,subject="Thanks for registration",body=f'otp is : {otp}')
        return render_template("verification.html",username=username,mobile=mobile,email=email,address=address,password=password,otp=otp)
        
        
        
    return render_template("reg.html")
@app.route('/otp/<username>/<mobile>/<email>/<address>/<password>/<otp>',methods=["GET","POST"])
def otp(username,mobile,email,address,password,otp):
    if request.method=="POST":
        uotp=request.form["uotp"]
        if otp==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("insert into reg values(%s,%s,%s,%s,%s)",[username,mobile,email,address,password])
            mydb.commit()
            cursor.close()
            return redirect(url_for("login"))
    return render_template("verification.html",username=username,mobile=mobile,email=email,address=address,password=password,otp=otp)
        

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":                                                                  
        username=request.form.get("username")
        password =request.form.get("password")                                                   
        cursor=mydb.cursor(buffered=True)
        cursor.execute("select count(*) from reg where username=%s && password=%s",[username,password])
        data=cursor.fetchone()[0]
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session["username"]]={}
            return redirect(url_for("homepage"))
            
        else:
            return "Invalid Username and password"
                
  
        
    return render_template("login.html")
@app.route("/logout")
def logout():
    if session.get("username"):
        session.pop("username")
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    return render_template("admin.html")
@app.route("/addpost" ,methods=["POST","GET"])
def add_post():
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute("insert into posts(title,content,slug) values(%s,%s,%s)",[title,content,slug])
        mydb.commit()
        cursor.close()
    return render_template("add_post.html")
@app.route("/view_posts")
def view_posts():
    cursor=mydb.cursor(buffered=True)
    cursor.execute("select * from posts")
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template("view_posts.html",posts=posts)
#delect post
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered="True")
    cursor.execute("select * from posts where id=%s",(id,))

    post=cursor.fetchall()
    print(post)
    cursor.execute("DELETE from posts where id=%s",(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('view_posts'))
@app.route("/update",methods=["POST","GET"])  
def update():
    if request.method=="POST":
        password=request.form.get("password")
        username=request.form.get("username")
        cursor=mydb.cursor(buffered="True")
        cursor.execute("update reg set password=%s where username=%s",[password,username])
        mydb.commit()
        cursor.close()
        return redirect(url_for("login"))
    return render_template("password.html")
@app.route("/update_post/<int:id>" ,methods=["POST","GET"])
def update_post(id):
    if request.method=="POST":
        title=request.form["title"]
        content=request.form["content"]
        slug=request.form["slug"]
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute("update  posts SET title=%s,content=%s,slug=%s WHERE id=%s",[title,content,slug,id])
        mydb.commit()
        cursor.close()
        return redirect(url_for("view_posts"))
    else:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',[id])
        post=cursor.fetchone()
        cursor.close()
        return render_template('update.html',post=post)

@app.route("/about")
def about():
    return render_template("about.html")






app.run(debug=True,use_reloader=True)