import mysql.connector as MySQLdb
import pandas as pd

from flask import Flask
from flask import request, jsonify
from flask_mail import Mail
from flask_mail import Message

application = Flask(__name__)

application.config.update(dict(
    DEBUG=True,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME="riteshsengar26@gmail.com",
    MAIL_PASSWORD="bemylife",
))


def db_conn():
    try:
        connection = MySQLdb.connect(host="54.165.254.26", port=3306, database="fish_app", user="ritesh", password="mindcrew01",autocommit=True)
    except:
        connection = MySQLdb.connect(host="54.165.254.26", port=3306, database="fish_app", user="ritesh", password="mindcrew01",autocommit=True)

    return connection


@application.route("/forgotpassword", methods=['GET','POST'])
def index():
    try:
        conn = db_conn()
        cur = conn.cursor()

        mail = Mail(app)

        params = request.json["forgotpassword"]
        email = params['email']
        print(params)

        try:
            cur.execute("select * from otp_verification where email = '{}'".format(email))
            data = cur.fetchall()
            print(data)
            if len(data) == 1:
                from random import randint
                otp = str(randint(100000, 999999))
                msg = Message("Verification Code",
                                sender="riteshsengar26@gmail.com",
                                recipients=[email])
                msg.body = otp
                mail.send(msg)

                query = """UPDATE otp_verification SET otp = %s WHERE email = %s"""
                cur.execute(query, (otp, email))
                conn.commit()
                cur.close()
                conn.close()
                return jsonify({"status": "success", "otp": otp})
            else:
                query = """INSERT INTO otp_verification(email,otp)
                            VALUES (%s, %s)"""
                cur.execute(query, [email, otp])
                conn.commit()

                cur.close()
                conn.close()
                return jsonify({"status": "success", "otp": otp})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({"status": "fail", "msg": str(e)})
    except Exception as e: 
        print(e)

@application.route('/adduser', methods=['GET','POST'])
def scoreboard():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["adduserdata"]
        email = params['email']
        fullname = params['full_name']
        mob_code = params['mob_code']
        mobile_number = params['mob_number']
        password = params['password1']
        platform = params['platform']
        try:
            query = """INSERT INTO tb_users(full_name,email,mobile_number,mobile_code,password,platform)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cur.execute(query, [fullname, email, mobile_number, mob_code, password, platform])
            conn.commit()
            id = cur.lastrowid
            cur.close()
            conn.close()
            return jsonify({'status': 'success', 'userdata': [{'id': id, 'full_name': fullname, 'email': email, "profilepic": "",
                                                                "mob_number": mobile_number, "mob_code": mob_code, "password": password}]})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)


@application.route('/login', methods=['GET','POST'])
def login():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["login"]
        email = params["email"]
        password = params["password1"]
        # platform = params["platform"]
        try:
            cur.execute("select * from tb_users where email = %s and password = %s", (email, password))
            data = cur.fetchall()
            print("-----------------------------")
            print(data)
            print("-----------------------------")
            if len(data) == 1:
                cur.close()
                conn.close()
                print("data[0][8] ---------------", data[0][8])
                pic = data[0][8] if data[0][8] != None else " "
                return jsonify({'status': 'success', "userdata": [{"id": data[0][0], "email":data[0][2], "password": data[0][5], "full_name":data[0][1],
                                        "profilepic":pic, "mob_number": data[0][3], "mob_code": data[0][4]}]})
            elif len(data) == 0:
                cur.execute("select * from tb_users where email ='{}'".format(email))
                data = cur.fetchall()
                if len(data) == 0:
                    cur.close()
                    conn.close()
                    return jsonify({'status': 'fail', "erroremail": "Email not found"})
                elif len(data) == 1:
                    cur.execute("select * from tb_users where password ='{}'".format(password))
                    data = cur.fetchall()
                    cur.close()
                    conn.close()
                    if len(data) == 0:
                        return jsonify({'status': 'fail', "errorpassword": "Incorrect Password"})
                    else:
                        pass
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)
        return jsonify({'status': 'fail', 'msg': str(e)})


@application.route('/verificationcode', methods=['GET', 'POST'])
def verificationcode():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["verificationcode"]
        email = params["email"]
        # userid = params["userid"]
        otp = params["code"]
        # platform = params["platform"]
        print(params)
        try:
            cur.execute("select * from otp_verification where email = %s and otp = %s", (email, otp))
            data = cur.fetchall()[0]
            print(data)
            cur.close()
            conn.close()
            return jsonify({'status': 'success'})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail'})
    except Exception as e: 
        print(e)


@application.route('/socialadduser', methods=['GET', 'POST'])
def socialadduser():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["socialadduser"]
        email = params["email"]
        full_name = params["full_name"]
        fbid = params["fbid"]
        platform = params["platform"]

        print(params)

        cur.execute("select * from tb_users where email = %s and facebook_id = %s", (email, fbid))
        data = cur.fetchall()
        if len(data) == 1:
            cur.close()
            conn.close()
            return jsonify({'status': 'success', "userdata": [
                {"id": data[0][0], "email": data[0][2], "full_name": data[0][1]}]})
        else:
            try:

                query = """INSERT INTO tb_users(full_name,email,platform,facebook_id)
                                        VALUES (%s, %s, %s, %s)"""
                cur.execute(query, [full_name, email, platform, fbid])
                conn.commit()
                id = cur.lastrowid
                cur.close()
                conn.close()
                return jsonify({'status': 'success', "userdata": [
                    {"id": id, "email": email, "full_name": full_name}]})
            except Exception as e:
                cur.close()
                conn.close()
                return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)


@application.route('/verifymobilenumber', methods=['GET', 'POST'])
def verifymobilenumber():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["verifymobilenumber"]

        userid = params["userid"]
        mobile_number = params["mobilenumber"]
        countrycode = params["countrycode"]
        platform = params["platform"]

        print(params)

        try:
            query = """UPDATE tb_users SET mobile_number = %s, mobile_code = %s WHERE id = %s"""
            cur.execute(query, (mobile_number, countrycode, userid))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'success'})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)


@application.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        userid = request.json["logout"]["userid"]

        try:
            cur.execute("select * from tb_users where id = '{}'".format(userid))
            data = cur.fetchall()[0]
            print(data)
            cur.close()
            conn.close()
            return jsonify({'status': 'success'})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)


def image_convert(pic, full_name):
    profile_pic = ""
    if pic != "":
        try:
            import base64, os
            profile_pic = base64.b64decode(pic)
            print(os.getcwd(),"-----------------Working Directory")
            filename = str(os.getcwd())+"/profilepics/"+str(full_name) + ".jpg"
            with open(filename, 'wb') as f:
                f.write(profile_pic)
            return filename
        except Exception as e:
            print(e, "--------------Error")
    else:
        pass
    return profile_pic


@application.route('/userprofile', methods=['GET', 'POST'])
def userprofile():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["userprofile"]

        userid = params["userid"]
        profilepic = params["profilepic"]
        full_name = params["name"]
        password = params["password"]
        # platform = params["platform"]
        # print(params)
        # pic = profilepic
        profilepic = image_convert(profilepic, full_name)
        try:
            cur.execute("select * from tb_users where id = %s and password = %s", (userid, password))
            data = cur.fetchall()
            print(data)
            if len(data) == 1:
                query = """UPDATE tb_users SET full_name = %s, profile_pic = %s WHERE id = %s and password = %s"""
                cur.execute(query, (full_name, profilepic, userid, password))
                conn.commit()
                cur.close()
                conn.close()
                return jsonify({'status': 'success', "profilepic": profilepic})
            else:
                cur.close()
                conn.close()
                return jsonify({'status': 'fail', 'msg': "User not found"})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)

@application.route('/forgetpasswordupdate', methods=['GET', 'POST'])
def forgetpasswordupdate():
    try:
        # if request.method == 'POST':
        conn = db_conn()
        cur = conn.cursor()
        params = request.json["forgetpasswordupdate"]
        email = params["email"]
        userid = params["userid"]
        password = params["password"]
        print(params)

        try:
            cur.execute("select * from tb_users where id = %s and email = %s", (userid, email))
            data = cur.fetchall()
            print(data)
            if len(data) == 1:
                query = """UPDATE tb_users SET password = %s WHERE id = %s and email = %s"""
                cur.execute(query, (password, userid, email))
                conn.commit()
                cur.close()
                conn.close()
                return jsonify({'status': 'success'})
            else:
                cur.close()
                conn.close()
                return jsonify({'status': 'fail', 'msg': "User not found"})
        except Exception as e:
            cur.close()
            conn.close()
            return jsonify({'status': 'fail', 'msg': str(e)})
    except Exception as e: 
        print(e)

@application.route('/fish', methods=['GET', 'POST'])
def fish():
    try:
        from classify import image_predict

        # if request.method == 'POST':
        image = request.json["image"]

        # profile_pic = image_convert(profilepic, full_name)
        
        label = image_predict(image_path=image)
        # label = image_predict(image_path='examples/blackmerlin6.jpg')

        print(label,"--------------------------------------")
        # os.system('python classify.py --model fish.model --labelbin lb.pickle --image 1.jpeg')
        fishname = label.split(":")[0]
        percent = label.split(":")[1]

        print("Fish------------",fish)
        print("Percent------------",percent)
        return jsonify({'fishname':fishname,"percent":percent})
    except Exception as e: 
        print(e)


if __name__ == "__main__":
    application.run(debug=True,port= '8000')
