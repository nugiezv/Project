import psycopg2
from flask import Flask
from flask import request as rq
from flask import jsonify
from loguru import logger

app = Flask(__name__)
def conn():
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="127.0.0.1",
                            port="5432",
                            database="JobPortal")
    return conn

def connuser_id(usernames):
    connection = conn()
    cursor = connection.cursor()
    query = "SELECT user_id from users WHERE username = %s"
    cursor.execute(query,(usernames, ))
    users_records = cursor.fetchone()[0]
    return users_records

def con_c_userid(jobs_id):
    connection = conn()
    cursor = connection.cursor()
    query = "SELECT c_user_id from jobs WHERE jobs_id = %s"
    cursor.execute(query,(jobs_id, ))
    users_records = cursor.fetchone()[0]
    return users_records

def is_company():
    username = rq.authorization['username']
    connection = conn()
    cursor = connection.cursor()
    comps = "SELECT type FROM users WHERE username = %s"
    cursor.execute(comps, (username,))
    companies = cursor.fetchone()[0] # [0]biar hilang kurung nya
    if companies == 'company':
        return True
    else:
        return False 

# LOGIN
def login():
    username = rq.authorization["username"]
    password = rq.authorization["password"]

    connection = conn()
    cursor = connection.cursor()
    username1 = "select username from users where username = %s"
    cursor.execute(username1, (username,))
    user = cursor.fetchone()[0]
    password1 = "select password from users where username = %s"
    cursor.execute(password1, (username,))
    passw = cursor.fetchone()[0]

    if username == user and password == passw:
        return "Login Berhasil"
    else:
        return "Login Gagal"

# SIGN UP
@app.route('/signup', methods=['POST'])
def signup():
    try:
        A = rq.json
        mail = A["email"]
        uname = A["username"]
        pasw = A["password"]
        tipe = A["type"]

        connection = conn()
        print("using python variable")
        cursor = connection.cursor()
        postgreSQL_select_Query = "INSERT INTO public.users(\
                                username, email, password, type)\
                                VALUES (%s, %s, %s, %s);"
        cursor.execute(postgreSQL_select_Query, (uname, mail, pasw, tipe))
        connection.commit()
        # logger.debug()

        return "Sign Up Success"
    except:
        return jsonify({
            "error" : "Bad Request",
            "message" : "username sudah terdaftar"
        })
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
# UPDATE USER DATA
@app.route('/user/<string:unames>/update_user', methods=['PUT'])
def update(unames):
    if login() != "Login Berhasil":
        return "Gagal Login"
    else:
        try:
            A = rq.json
            userExist = unames
            mail = A["newEmail"]
            uname = A["newUsername"]
            pasw = A["newPassword"]
            tipe = A["newType"]

            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            postgreSQL_select_Query = "UPDATE public.users SET username = %s, email = %s, password = %s, type = %s WHERE username = %s ;"
            cursor.execute(postgreSQL_select_Query,
                        (uname, mail, pasw, tipe, userExist))
            connection.commit()
            return "User Updated Successfully"

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

# INPUT PROFILE JOBSEEKER
@app.route('/user/jobseeker/input_profile', methods=['POST'])
def input_j_profile():
    if login() != "Login Berhasil":
        return "Gagal Login"
    else:
        try:
            A = rq.json
            usernames = rq.authorization['username']
            name = A["j_name"]
            address = A["j_address"]
            contact = A["j_contact"]
            edu = A["j_education"]
            exp = A["j_experience"]

            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            postgreSQL_select_Query = "INSERT INTO public.jobseeker_profile (j_user_id, j_name, j_address, j_contact, j_education, j_experience) VALUES ((SELECT user_id from users WHERE username = %s), %s, %s, %s, %s, %s)  ;"
            cursor.execute(postgreSQL_select_Query,
                        (usernames, name, address, contact, edu, exp))
            connection.commit() 
            return "User Input Successfully"

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


# UPDATE PROFILE JOBSEEKER
@app.route('/user/jobseeker/update_profile', methods=['PUT'])
def update_j_profile():
    if login() != "Login Berhasil":
        return "Gagal Login"
    else:
        try:
            A = rq.json
            usernames = rq.authorization['username']
            name = A["j_name"]
            address = A["j_address"]
            contact = A["j_contact"]
            edu = A["j_education"]
            exp = A["j_experience"]

            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            postgreSQL_select_Query = "UPDATE public.jobseeker_profile SET j_name = %s, j_address = %s, j_contact = %s, j_education = %s, j_experience = %s WHERE j_user_id = (SELECT user_id from users WHERE username = %s) ;"
            cursor.execute(postgreSQL_select_Query,
                        (name, address, contact, edu, exp, usernames))
            connection.commit() 
            return "User Updated Successfully"

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


# INPUT PROFILE COMPANY
@app.route('/user/company/input_profile', methods=['POST'])
def input_c_profile():
    if login() != "Login Berhasil" and is_company() == True:
        return "Gagal Login"
    else:
        try:
            A = rq.json
            usernames = rq.authorization['username']
            name = A["c_name"]
            address = A["c_address"]
            descr = A["c_description"]

            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            postgreSQL_select_Query = "INSERT INTO public.company_profile (c_user_id, c_name, c_address, c_description) VALUES ((SELECT user_id from users WHERE username = %s), %s, %s, %s)  ;"
            cursor.execute(postgreSQL_select_Query,
                        (usernames, name, address, descr))
            connection.commit() 
            return "User Input Successfully"

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


# UPDATE PROFILE COMPANY
@app.route('/user/company/update_profile', methods=['PUT'])
def update_c_profile():
    if login() != "Login Berhasil" and is_company() == True:
        return "Gagal Login"
    else:
        try:
            A = rq.json
            usernames = rq.authorization['username']
            name = A["c_name"]
            address = A["c_address"]
            descr = A["c_description"]
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            postgreSQL_select_Query = "UPDATE public.company_profile SET c_name = %s, c_address = %s, c_description = %s WHERE c_user_id = (SELECT user_id from users WHERE username = %s) ;"
            cursor.execute(postgreSQL_select_Query,
                        (name, address, descr, usernames))
            connection.commit() 
            return "User Updated Successfully"

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


# SEARCH USER
@ app.route('/search_user', methods=['POST'])
def search_user():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            arr = []
            usernames = rq.args.get('username')
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()

            postgreSQL_select_Query = f"SELECT user_id, username, email, type FROM public.users WHERE username LIKE '%{usernames}%'  "
            cursor.execute(postgreSQL_select_Query)
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append(
                    {"id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "type" : row[3]})
            return jsonify(arr)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# POST A JOB
@ app.route('/timeline/post_jobs', methods=['POST'])
def jobs():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            A = rq.json
            c_id = rq.authorization['username']
            job = A['job']
            descr = A['description']
            loc = A['location']
            tipe = A['type']
            gen = A['gender']
            stat = A['status']
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            postgreSQL_select_Query = "INSERT INTO public.jobs(jobs_name, c_user_id, jobs_description, jobs_location, jobs_type, jobs_gender, jobs_status) VALUES (%s, (SELECT user_id FROM users WHERE users.username = %s), %s, %s, %s, %s, %s);"
            cursor.execute(postgreSQL_select_Query, (job, c_id, descr, loc, tipe, gen, stat))
            connection.commit()
            logger.debug(postgreSQL_select_Query)
            return "Job Posted"
        # except (Exception, psycopg2.Error) as error:
        #     return "Error while fetching data from PostgreSQL", 401

        finally:
            if connection:
                cursor.close()
                connection.close()  
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# GET A JOB
@app.route('/timeline/get_jobs', methods=['GET'])
def get_jobs():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            arr = []
            usernames = rq.authorization['username']
            id_jobs = rq.args.get('jobs_id')
            connection = conn()
            cursor = connection.cursor()
            postgreSQL_select_Query = "SELECT jobs.* FROM jobs INNER JOIN users ON users.user_id = jobs.c_user_id where username = %s AND jobs_id = %s "

            cursor.execute(postgreSQL_select_Query, (usernames,id_jobs))
            print("Selecting rows from mobile table using cursor.fetchall")
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({"1. jobs_id": row[0], 
                            "2. jobs_name": row[1],
                            "3. c_user_id": row[2],
                            "4. jobs_description": row[3],
                            "5. jobs_location": row[4],
                            "6. jobs_type": row[5],
                            "7. jobs_gender": row[6],
                            "8. jobs_status": row[7]})
            return jsonify(arr)

        except (Exception, psycopg2.Error) as error:
            return "Error while fetching data from PostgreSQL"

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'


# GET ALL JOB
@ app.route('/timeline/get_all_jobs', methods=['GET'])
def get_all_job():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            arr = []
            usernames = rq.authorization['username']
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()

            postgreSQL_select_Query = "SELECT jobs_id, jobs_name, c_user_id, jobs_description, jobs_location, jobs_type, jobs_gender, jobs_status FROM jobs INNER JOIN users ON users.user_id = jobs.c_user_id WHERE users.username = %s "
            cursor.execute(postgreSQL_select_Query, (usernames,))
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({"1. jobs_id": row[0], 
                            "2. jobs_name": row[1],
                            "3. c_user_id": row[2],
                            "4. jobs_description": row[3],
                            "5. jobs_location": row[4],
                            "6. jobs_type": row[5],
                            "7. jobs_gender": row[6],
                            "8. jobs_status": row[7]
                            })
            return jsonify(arr)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# EDIT JOBS
@app.route('/jobs/edit_jobs', methods=['PUT'])
def edit_jobs():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            A = rq.json
            usernames = rq.authorization['username']
            jobs_id = rq.args.get('id_jobs')
            name = A["newJobName"]
            descr = A["newJobDescr"]
            loc = A["newJobLoc"]
            tipe = A["newJobType"]
            gen = A['newJobGender']
            stat = A['newJobStatus']

            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            if str(connuser_id(usernames)) != str(con_c_userid(jobs_id)):
                return "Username dan jobs_id tidak sama"
            else:
                postgreSQL_select_Query = "UPDATE jobs SET jobs_name = %s, jobs_description = %s, jobs_location = %s, jobs_type = %s, jobs_gender = %s, jobs_status = %s WHERE c_user_id = (SELECT user_id from users WHERE username = %s ) AND jobs_id = %s;"
                cursor.execute(postgreSQL_select_Query,
                            (name, descr, loc, tipe, gen, stat, usernames, jobs_id))
                connection.commit()
                return "Jobs Updated Successfully"

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# LIST ALL AVAILABLE JOB
@ app.route('/timeline/list_available_jobs', methods=['GET'])
def list_job():
    if login() == 'Login Berhasil' and is_company() != True:
        try:
            arr = []
            usernames = rq.authorization['username']
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()

            postgreSQL_select_Query = "SELECT jobs_id, jobs_name, c_user_id, jobs_description, jobs_location, jobs_type, jobs_gender, jobs_status FROM jobs INNER JOIN users ON users.user_id = jobs.c_user_id WHERE jobs_status = 'Available' "
            cursor.execute(postgreSQL_select_Query, (usernames,))
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({"1. jobs_id": row[0], 
                            "2. jobs_name": row[1],
                            "3. c_user_id": row[2],
                            "4. jobs_description": row[3],
                            "5. jobs_location": row[4],
                            "6. jobs_type": row[5],
                            "7. jobs_gender": row[6],
                            "8. jobs_status": row[7]
                            })
            return jsonify(arr)
        except (Exception, psycopg2.Error) as error:
            return f'Error while fetching data from PostgreSQL'

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# SEARCH JOBS BY CRITERIA
# LOCATION, TYPE, GENDER
@ app.route('/search_jobs', methods=['POST'])
def search_jobs():
    if login() == 'Login Berhasil' and is_company() != True:
        connection = conn() 
        try:

            where = []
            for key, value in rq.args.items():
                #key aktif tapi valuenya kosong/null
                if not value: 
                    continue

                if key == "gender":
                    if value == "Pria":
                        where.append("gender != Wanita")
                    if value == "Wanita":
                        where.append("gender != Pria")
                    continue #di skip where dibawah karena sudah selesai cek gendernya
                        
                where.append("{} LIKE '%{}%'".format(key,value))


            column = "jobs_id, jobs_name, c_user_id, jobs_description, jobs_location, jobs_type, jobs_gender, jobs_status"
            table = "jobs INNER JOIN users ON users.user_id = jobs.c_user_id"
            if len(where) > 0:
                sql = "SELECT %s FROM %s WHERE %s" % (column, table, " AND ".join(where))
            else:
                sql = "SELECT %s FROM %s " % (column, table)
            
            
            print("using python variable")
            cursor = connection.cursor()
            
            cursor.execute(sql)
            users_records = cursor.fetchall()

            arr = []
            print("Print each row and it's columns values")
            for row in users_records:
                arr.append(
                    {"1. jobs_id": row[0], 
                    "2. jobs_name": row[1],
                    "3. c_user_id": row[2],
                    "4. jobs_description": row[3],
                    "5. jobs_location": row[4],
                    "6. jobs_type": row[5],
                    "7. jobs_gender": row[6],
                    "8. jobs_status": row[7]})
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
            return jsonify(arr)
    else:
        return 'Permission Denied'

# GET A JOB DETAIL
@app.route('/timeline/get_jobs_detail', methods=['GET'])
def get_a_jobdetail():
    if login() == 'Login Berhasil' and is_company() != True:
        try:
            arr = []
            # usernames = rq.authorization['username']
            id_jobs = rq.args.get('jobs_id')
            connection = conn()
            cursor = connection.cursor()
            postgreSQL_select_Query = "SELECT jobs.* FROM jobs INNER JOIN users ON users.user_id = jobs.c_user_id where jobs_id = %s "

            cursor.execute(postgreSQL_select_Query, (id_jobs))
            print("Selecting rows from mobile table using cursor.fetchall")
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({
                            # "1. jobs_id": row[0], 
                            "1. jobs_name": row[1],
                            # "3. c_user_id": row[2],
                            "2. jobs_description": row[3],
                            "3. jobs_location": row[4],
                            "4. jobs_type": row[5],
                            "5. jobs_gender": row[6],
                            "6. jobs_status": row[7]})
            return jsonify(arr)

        except (Exception, psycopg2.Error) as error:
            return "Error while fetching data from PostgreSQL"

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# APPLY A JOB
@ app.route('/timeline/apply_job', methods=['POST'])
def apply_job():
    if login() == "Login Berhasil" and is_company() != True:
        try:
            A = rq.json
            user_id = rq.authorization['username']
            jobs_id = rq.args.get('jobs_id')
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()

            postgreSQL_select_Query = "INSERT INTO application (j_user_id, jobs_id) VALUES ((SELECT users.user_id FROM users WHERE username = %s), (SELECT jobs.jobs_id FROM jobs WHERE jobs_id = %s));"
            cursor.execute(postgreSQL_select_Query, (user_id, jobs_id))
            connection.commit()
            return "Job Applied"
        except (Exception, psycopg2.Error) as error:
            return "Error while fetching data from PostgreSQL"
        
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# LIST ALL APPLIED JOB AND STATUS
@ app.route('/timeline/<string:usernames>/applied_jobs', methods=['GET'])
def applied_job(usernames):
    if login() == 'Login Berhasil' and is_company() != True:
        try:
            arr = []
            usernames = rq.authorization['username']
            # id_jobseeker = rq.args.get('j_user_id')
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()

            postgreSQL_select_Query = "SELECT jobs.jobs_id, jobs.jobs_name, jobs.c_user_id, jobs.jobs_description, jobs.jobs_location, jobs.jobs_type, jobs.jobs_gender, jobs.jobs_status, application.j_user_id, application.is_accepted FROM jobs INNER JOIN application ON application.jobs_id = jobs.jobs_id WHERE application.j_user_id = (SELECT user_id from users WHERE username = %s ) "
            cursor.execute(postgreSQL_select_Query, (usernames,))
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({"jobs_id": row[0], 
                            "jobs_name": row[1],
                            "c_user_id": row[2],
                            "jobs_description": row[3],
                            "jobs_location": row[4],
                            "jobs_type": row[5],
                            "jobs_gender": row[6],
                            "jobs_status": row[7]
                            })
            return jsonify(arr)
        except (Exception, psycopg2.Error) as error:
            return f'Error while fetching data from PostgreSQL'

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# GET A JOBSEEKER PROFILE
@app.route('/user/j_profile', methods=['GET'])
def jobseeker_profile():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            arr = []
            # usernames = rq.authorization['username']
            id_jobseeker = rq.args.get('j_user_id')
            connection = conn()
            cursor = connection.cursor()
            postgreSQL_select_Query = "SELECT jobseeker_profile.* FROM jobseeker_profile INNER JOIN users ON users.user_id = jobseeker_profile.j_user_id WHERE j_user_id = %s "

            cursor.execute(postgreSQL_select_Query, (id_jobseeker,))
            print("Selecting rows from mobile table using cursor.fetchall")
            users_records = cursor.fetchall()

            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({"j_profile_id": row[0], 
                            "j_user_id": row[1],
                            "j_name": row[2],
                            "j_address": row[3],
                            "j_contact": row[4],
                            "j_education": row[5],
                            "j_experience": row[6],
                            })
            return jsonify(arr)

        except (Exception, psycopg2.Error) as error:
            return "Error while fetching data from PostgreSQL"

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

# LIST APPLICANT
@ app.route('/timeline/list_application', methods=['GET'])
def list_applicant():
    if login() == 'Login Berhasil' and is_company() == True:
        try:
            arr = []
            # usernames = rq.authorization['username']
            jobs = rq.args.get('jobs_id')
            connection = conn()
            print("using python variable")
            cursor = connection.cursor()
            
            postgreSQL_select_Query = "SELECT jp.j_user_id, jp.j_name, jp.j_address, jp.j_contact, jp.j_education, jp.j_experience FROM application INNER JOIN jobseeker_profile AS jp ON jp.j_user_id = application.j_user_id  WHERE jobs_id = %s "
            cursor.execute(postgreSQL_select_Query, (jobs,))
            users_records = cursor.fetchall()
            logger.debug(users_records)
            print("Print each row and it's columns values")
            for row in users_records:
                arr.append({
                            "j_user_id": row[0],
                            "j_name": row[1],
                            "j_address": row[2],
                            "j_contact": row[3],
                            "j_education" : row[4],
                            "j_experience" : row[5] 
                            })
            return jsonify(arr)
        except (Exception, psycopg2.Error) as error:
            return "Error while fetching data from PostgreSQL"
        
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    else:
        return 'Permission Denied'

if __name__ == '__main__':
    app.run(debug=True)