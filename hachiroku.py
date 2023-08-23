from flask import Flask,render_template,request,session,redirect,flash,url_for
from functools import wraps
import random 
import time 
from HROJ import *


hroj = Flask(__name__)
hroj.secret_key = 'ThLEkhFJhHZMOdVcO7wjIK691gyJUM3jBmot7HqudEzPhT10EihtazEOjO3hsAr00fwVZPmLPzGO2FO3t'

class auth:  
    def login_required(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            if 'username' in session or request.endpoint=="register":
                return route_function(*args, **kwargs)
            else:
                return redirect('/login')
        return wrapper
    
    @hroj.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST" and 'username' in request.form and 'password' in request.form:
            username = request.form['username']         
            password = request.form['password']         
            logthis(text = f"{color.bold}{username}{color.reset} [{color.blackbg}{password}{color.reset}] => {color.yellow}Trying to log in.{color.reset}",mode="warning")
            
            token,info = correct(username,password)
            
            if(token!="!" and info!="!"):
                logthis(text = f"{color.bold}{username}{color.reset} [{color.blackbg}{password}{color.reset}] => {color.green}Login approved!{color.reset}",mode="success")
                session['username'] = username
                session['password'] = password
                session['token'] = token
                session['mail'] = info['mail']
                session['role'] = info['role']
                session['name'] = info['name']
                session['surname'] = info['surname']
                return redirect('/')
            else:
                logthis(text = f"{color.bold}{username}{color.reset} [{color.blackbg}{password}{color.reset}] => {color.red}Login failed!{color.reset}",mode="danger")
                return render_template("login.html",error=False)
            
        return render_template("login.html",error=False)  
    
    @hroj.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == "POST" and 'username' in request.form and 'mail' in request.form and 'password' in request.form:
            name = request.form['name']         
            surname = request.form['surname']         
            username = request.form['username']         
            mail = request.form['mail']         
            password = request.form['password']         
            
            info = {}
            info['name']=name
            info['surname']=surname
            info['username']=username
            info['password']=password
            info['mail']=mail
            info['role']="01"
            info['accepted']=[] 
            info['submissions']=[]
            logthis(text = f"{color.bold}{username}{color.reset} - {color.blue}{password}{color.reset} [{color.blackbg}{mail}{color.reset}] => {color.yellow}Trying to register.{color.reset}",mode="warning")
            
            res = new_user(info)
            if(res!="!"):
                logthis(text = f"{color.bold}{username}{color.reset} - {color.blue}{password}{color.reset} [{color.blackbg}{mail}{color.reset}] => {color.green}Register approved!{color.reset}",mode="success")
                return redirect("/")
            else:
                logthis(text = f"{color.bold}{username}{color.reset} - {color.blue}{password}{color.reset} [{color.blackbg}{mail}{color.reset}] => {color.red}Register Failed!{color.reset}",mode="danger")
                flash('Registration failed. User already exists.', 'error')
                return render_template('register.html')
            
        return render_template("register.html")
    
    @hroj.route('/logout')
    def logout():
        session.pop('username', None)
        session.pop('role', None)
        try:
            session.pop('code', None)
        except:
            pass
        return redirect('/login')

    def refresh_session(info):
        # print(info)
        if( info=='!'):
            return
        session['username'] = info['username']
        session['password'] = info['password']
        session['mail'] = info['mail']
        session['role'] = info['role']
        session['name'] = info['name']
        session['surname'] = info['surname']
        
class page86:
    @hroj.route("/=>86",methods=['GET', 'POST'])
    @auth.login_required
    def mod86():
        if request.method == "POST":
            
            if 'create_user' in request.form :
                name = request.form['name']
                surname = request.form['surname']
                username = request.form['username']         
                mail = request.form['mail']         
                password = request.form['password']         
                role = request.form['role']
                
                info = {}
                info['name']=name
                info['surname']=surname
                info['username']=username
                info['password']=password
                info['mail']=mail
                info['role']=role 
                info['accepted']=[] 
                info['submissions']=[]
            
                new_user(info)
                logthis(text = f"{color.bold}{username}{color.reset} - {color.blue}{password}{color.reset} /{color.redbg}{role}{color.reset} [{color.blackbg}{mail}{color.reset}] => {color.bold}{color.green}New user created{color.reset}.",mode="success")
            elif 'ban_this' in request.form :
                tok = request.form['token']
                db = getdb()
                if tok in db:
                    logthis(text = f"{color.bold}{getdb()[tok]['username']}{color.reset} => Banned by {color.bold}{session['username']}{color.reset}!",mode="danger")
                    ban_user(tok)
                    
                
        return render_template("/hroj_mod/mod86.html",db=getdb())
  
class settings:
    
    @hroj.route('/settings',methods=['GET','POST'])
    @auth.login_required
    def settings():
        if request.method == 'POST':
            info = {}
            for key in ['name','surname','username','password','mail','role']:
                if(key in request.form):
                    info[key]=request.form[key]
                    # print(key)
            db = getdb()
            if not session['token'] in db:
                auth.logout()
                return redirect("/")
            
            update_user(session['token'],info)
            auth.refresh_session(db[session['token']])
            
        return render_template('settings.html')
        
      
@hroj.route("/")
@auth.login_required
def home():
    problems = get_problems()
    # print(problems)
    return render_template("home.html",problems=problems)

@hroj.route("/submission/<id>")
@auth.login_required
def submission(id):
    sbdb = get_submissions()
    db = getdb()
    
    tok = sbdb[id]['token']
    result = sbdb[id]['result']
    problem_id = sbdb[id]['problem_id']
    code = sbdb[id]['code']
    
    if not tok in db or problem_info(problem_id)=="!":
        # print(tok,problem_id)
        return redirect("/")
    
    info = db[tok]
    pinfo = problem_info(problem_id)
    return render_template("submission.html",id=id,result=result,problem_id=problem_id,info=info,pinfo=pinfo,code=code)


@hroj.route("/problem/<problem_id>",methods=['GET','POST'])
@auth.login_required
def problem(problem_id):
    pinfo = problem_info(problem_id)
    
    if request.method == 'POST':
        if 'code' in request.form and ( (not 'lastcode' in session) or session['lastcode']!=request.form['code']): 
            code = request.form['code']
            language = language_compiler_version(request.form['language'])
            _tok = session['token']
            session['lastcode']=code;
            id = submit_problem(problem_id,code,language,_tok)
            
            return redirect(url_for("submission", id=id))
        else:
            return render_template("problem.html",problem_id=problem_id,pinfo=pinfo)
    
    return render_template("problem.html",problem_id=problem_id,pinfo=pinfo)


@hroj.route("/user/<username>")
@auth.login_required
def user(username):
    token,info = user_info(username)
    if(token=="!"):
        return redirect("/")
    return render_template("user.html",info=info,username=username,submissions=info['submissions'],accepted=info['accepted'])



if __name__ == "__main__":
    Flask.run(hroj,host="0.0.0.0",port=5000,debug=True)

"""
* HACHIROKU (86) Online Judge by hachiroku.cpp
"""