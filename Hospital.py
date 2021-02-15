from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
import pymysql

app = Flask(__name__)

@app.route('/doctors_info')
def doctors_info():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='hospital01')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute('select * from doctor')
            if res > 0:
                details = cursor.fetchall()
                return render_template('doc_dis.html', details=details)
    finally:
        connection.close()

@app.route('/patient_info')
def patient_info():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='hospital01')
    try:
        with connection.cursor() as cursor:
             res = cursor.execute('select * from patient')
             if res > 0:
                details = cursor.fetchall()
                return render_template('patient_dis.html', details=details)
    finally:
        connection.close()

@app.route('/add_patient', methods=['POST','GET'])
def add_patient():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01'
                                 )
    if request.method == 'POST':
        details = request.form
        firstname = details['firstname']
        lastname = details['lastname']
        docid = details['docid']
        age = details['age']
        gender = details['gender']
        dateofbirth = details['dateofbirth']
        occupation = details['occupation']
        ph_num = details['ph_num']
        city=details['city']
        bloodgroup=details['bloodgroup']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO patient(firstname,lastname,docid,age,gender,dateofbirth,occupation,ph_num,city,bloodgroup) VALUES (%s, %s,%s,%s, %s ,%s ,%s, %s, %s ,%s)"
                cursor.execute(sql, (firstname, lastname , docid, age, gender, dateofbirth, occupation,ph_num, city,bloodgroup))
            connection.commit()

        finally:
            connection.close()
    return redirect(url_for('patient_info'))

@app.route('/add_doctor', methods=['POST', 'GET'])
def add_doctor():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01'
                                 )
    if request.method == 'POST':
        details = request.form
        id =details['id']
        firstname = details['firstname']
        lastname = details['lastname']
        age = details['age']
        gender = details['gender']
        dateofbirth = details['dateofbirth']
        salary= details['salary']
        experience = details['experience']
        qualification=details['qualification']
        ph_num = details['ph_num']
        dateofjoin=details['dateofjoin']
        try:

            with connection.cursor() as cursor:
                sql = "INSERT INTO doctor(id,firstname,lastname,age,gender,dateofbirth,salary,experience,qualification,ph_num,dateofjoin) VALUES (%s,%s, %s,%s, %s ,%s ,%s, %s, %s ,%s, %s)"
                cursor.execute(sql, (id, firstname, lastname , age, gender, dateofbirth,salary,experience,qualification,ph_num,dateofjoin))
            connection.commit()

        finally:
            connection.close()
    return redirect(url_for('doctors_info'))


@app.route('/patient_status')
def patient_status():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute("select id,firstname,lastname,docid,healthstatus,discharge,bloodgroup,dateofjoin from healthstatus where healthstatus='Not Cured'")
            if res > 0:
                details = cursor.fetchall()
                return render_template('ongoing.html', details=details)
    finally:
        connection.close()

@app.route('/recovered_status')
def recovered_status():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute("select id,firstname,lastname,docid,treatment_days,healthstatus,discharge,bloodgroup,dateofjoin,dateofdischarge from healthstatus where healthstatus='Cured'")
            if res > 0:
                details = cursor.fetchall()
                return render_template('cured.html', details=details)
    finally:
        connection.close()

@app.route('/patient_full')
def patient_full():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='hospital01')
    try:
        with connection.cursor() as cursor:
             res = cursor.execute('select patient.id,patient.firstname,patient.lastname,patient.age,patient.docid,patient.gender,healthstatus.healthstatus,healthstatus.treatment_days,healthstatus.discharge,patient.bloodgroup,healthstatus.dateofjoin,healthstatus.dateofdischarge,patient.dateofbirth,patient.occupation,patient.ph_num,patient.city from patient left join healthstatus on healthstatus.id=patient.id union select patient.id,patient.firstname,patient.lastname,patient.age,patient.docid,patient.gender,healthstatus.healthstatus,healthstatus.treatment_days,healthstatus.discharge,patient.bloodgroup,healthstatus.dateofjoin,healthstatus.dateofdischarge,patient.dateofbirth,patient.occupation,patient.ph_num,patient.city from patient right join healthstatus on healthstatus.id=patient.id')
             if res > 0:
                details = cursor.fetchall()
                return render_template('patient_join.html', details=details)
    finally:
        connection.close()


@app.route('/update_status' , methods=['POST','GET'])
def update_status():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01'
                                 )
    if request.method == 'POST':
        details=request.form
        id=details['id']
        healthstatus =details['healthstatus']
        treatment_days=details['treatment_days']
        discharge = details['discharge']
        dateofdischarge=details['dateofdischarge']

        try:
            with connection.cursor() as cursor:
                cursor.execute("update healthstatus set healthstatus=%s,treatment_days=%s,discharge=%s,dateofdischarge=%s  where id=%s", (healthstatus,treatment_days ,discharge, dateofdischarge,id))
                connection.commit()
                return redirect(url_for('recovered_status'))
        finally:
            connection.close()

@app.route('/search_patient', methods=['POST','GET'])
def search_patient():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res = cursor.execute("select * from patient where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('patient_result.html', details=details)

    finally:
            connection.close()



@app.route('/search_doctor', methods=['POST','GET'])
def search_doctor():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from doctor where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('doctor_result.html', details=details)

    finally:
            connection.close()

@app.route('/search_status', methods=['POST','GET'])
def search_status():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='hospital01')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from healthstatus where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('status_result.html', details=details)

    finally:
            connection.close()


@app.route('/branch2_doctors')
def branch2_doctors():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch2')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute('select * from doctor')
            if res > 0:
                details = cursor.fetchall()
                return render_template('doc_dis2.html', details=details)
    finally:
        connection.close()

@app.route('/branch2_patient')
def branch2_patient():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch2')
    try:
        with connection.cursor() as cursor:
             res = cursor.execute('select * from patient')
             if res > 0:
                details = cursor.fetchall()
                return render_template('patient_dis2.html', details=details)
    finally:
        connection.close()

@app.route('/add_patientb2', methods=['POST','GET'])
def add_patientb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2'
                                 )
    if request.method == 'POST':
        details = request.form
        firstname = details['firstname']
        lastname = details['lastname']
        docid = details['docid']
        age = details['age']
        gender = details['gender']
        dateofbirth = details['dateofbirth']
        occupation = details['occupation']
        ph_num = details['ph_num']
        city=details['city']
        bloodgroup=details['bloodgroup']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO patient(firstname,lastname,docid,age,gender,dateofbirth,occupation,ph_num,city,bloodgroup) VALUES (%s, %s,%s,%s, %s ,%s ,%s, %s, %s ,%s)"
                cursor.execute(sql, (firstname, lastname , docid, age, gender, dateofbirth, occupation,ph_num, city,bloodgroup))
            connection.commit()

        finally:
            connection.close()
    return redirect(url_for('branch2_patient'))

@app.route('/add_doctorb2', methods=['POST', 'GET'])
def add_doctorb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2'
                                 )
    if request.method == 'POST':
        details = request.form
        id =details['id']
        firstname = details['firstname']
        lastname = details['lastname']
        age = details['age']
        gender = details['gender']
        dateofbirth = details['dateofbirth']
        salary= details['salary']
        experience = details['experience']
        qualification=details['qualification']
        ph_num = details['ph_num']
        dateofjoin=details['dateofjoin']
        try:

            with connection.cursor() as cursor:
                sql = "INSERT INTO doctor(id,firstname,lastname,age,gender,dateofbirth,salary,experience,qualification,ph_num,dateofjoin) VALUES (%s,%s, %s,%s, %s ,%s ,%s, %s, %s ,%s, %s)"
                cursor.execute(sql, (id, firstname, lastname , age, gender, dateofbirth,salary,experience,qualification,ph_num,dateofjoin))
            connection.commit()

        finally:
            connection.close()
    return redirect(url_for('branch2_doctors'))

@app.route('/patient_statusb2')
def patient_statusb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute("select id,firstname,lastname,docid,healthstatus,discharge,bloodgroup,dateofjoin from healthstatus where healthstatus='Not Cured'")
            if res > 0:
                details = cursor.fetchall()
                return render_template('ongoing2.html', details=details)
    finally:
        connection.close()

@app.route('/recovered_statusb2')
def recovered_statusb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute("select id,firstname,lastname,docid,treatment_days,healthstatus,discharge,bloodgroup,dateofjoin,dateofdischarge from healthstatus where healthstatus='Cured'")
            if res > 0:
                details = cursor.fetchall()
                return render_template('cured2.html', details=details)
    finally:
        connection.close()

@app.route('/update_statusb2' , methods=['POST','GET'])
def update_statusb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2'
                                 )
    if request.method == 'POST':
        details=request.form
        id=details['id']
        healthstatus =details['healthstatus']
        treatment_days=details['treatment_days']
        discharge = details['discharge']
        dateofdischarge=details['dateofdischarge']

        try:
            with connection.cursor() as cursor:
                cursor.execute("update healthstatus set healthstatus=%s,treatment_days=%s,discharge=%s,dateofdischarge=%s  where id=%s", (healthstatus,treatment_days ,discharge, dateofdischarge,id))
                connection.commit()
                return redirect(url_for('recovered_statusb2'))
        finally:
            connection.close()

@app.route('/search_patientb2', methods=['POST','GET'])
def search_patientb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from patient where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('patient_result2.html', details=details)

    finally:
            connection.close()

@app.route('/search_doctorb2', methods=['POST','GET'])
def search_doctorb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from doctor where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('doctor_result2.html', details=details)

    finally:
            connection.close()

@app.route('/search_statusb2', methods=['POST','GET'])
def search_statusb2():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch2')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from healthstatus where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('status_result2.html', details=details)

    finally:
            connection.close()

@app.route('/patient_full2')
def patient_full2():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch2')
    try:
        with connection.cursor() as cursor:
             res = cursor.execute('select patient.id,patient.firstname,patient.lastname,patient.age,patient.docid,patient.gender,healthstatus.healthstatus,healthstatus.treatment_days,healthstatus.discharge,patient.bloodgroup,healthstatus.dateofjoin,healthstatus.dateofdischarge,patient.dateofbirth,patient.occupation,patient.ph_num,patient.city from patient left join healthstatus on healthstatus.id=patient.id union select patient.id,patient.firstname,patient.lastname,patient.age,patient.docid,patient.gender,healthstatus.healthstatus,healthstatus.treatment_days,healthstatus.discharge,patient.bloodgroup,healthstatus.dateofjoin,healthstatus.dateofdischarge,patient.dateofbirth,patient.occupation,patient.ph_num,patient.city from patient right join healthstatus on healthstatus.id=patient.id')
             if res > 0:
                details = cursor.fetchall()
                return render_template('patient_join2.html', details=details)
    finally:
        connection.close()



@app.route('/branch3_doctors')
def branch3_doctors():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch3')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute('select * from doctor')
            if res > 0:
                details = cursor.fetchall()
                return render_template('doc_dis3.html', details=details)
    finally:
        connection.close()

@app.route('/branch3_patient')
def branch3_patient():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch3')
    try:
        with connection.cursor() as cursor:
             res = cursor.execute('select * from patient')
             if res > 0:
                details = cursor.fetchall()
                return render_template('patient_dis3.html', details=details)
    finally:
        connection.close()

@app.route('/add_patientb3', methods=['POST','GET'])
def add_patientb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3'
                                 )
    if request.method == 'POST':
        details = request.form
        firstname = details['firstname']
        lastname = details['lastname']
        docid = details['docid']
        age = details['age']
        gender = details['gender']
        dateofbirth = details['dateofbirth']
        occupation = details['occupation']
        ph_num = details['ph_num']
        city=details['city']
        bloodgroup=details['bloodgroup']
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO patient(firstname,lastname,docid,age,gender,dateofbirth,occupation,ph_num,city,bloodgroup) VALUES (%s, %s,%s,%s, %s ,%s ,%s, %s, %s ,%s)"
                cursor.execute(sql, (firstname, lastname , docid, age, gender, dateofbirth, occupation,ph_num, city,bloodgroup))
            connection.commit()

        finally:
            connection.close()
    return redirect(url_for('branch3_patient'))

@app.route('/add_doctorb3', methods=['POST', 'GET'])
def add_doctorb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3'
                                 )
    if request.method == 'POST':
        details = request.form
        id =details['id']
        firstname = details['firstname']
        lastname = details['lastname']
        age = details['age']
        gender = details['gender']
        dateofbirth = details['dateofbirth']
        salary= details['salary']
        experience = details['experience']
        qualification=details['qualification']
        ph_num = details['ph_num']
        dateofjoin=details['dateofjoin']
        try:

            with connection.cursor() as cursor:
                sql = "INSERT INTO doctor(id,firstname,lastname,age,gender,dateofbirth,salary,experience,qualification,ph_num,dateofjoin) VALUES (%s,%s, %s,%s, %s ,%s ,%s, %s, %s ,%s, %s)"
                cursor.execute(sql, (id, firstname, lastname , age, gender, dateofbirth,salary,experience,qualification,ph_num,dateofjoin))
            connection.commit()

        finally:
            connection.close()
    return redirect(url_for('branch3_doctors'))

@app.route('/patient_statusb3')
def patient_statusb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute("select id,firstname,lastname,docid,healthstatus,discharge,bloodgroup,dateofjoin from healthstatus where healthstatus='Not Cured'")
            if res > 0:
                details = cursor.fetchall()
                return render_template('ongoing3.html', details=details)
    finally:
        connection.close()

@app.route('/recovered_statusb3')
def recovered_statusb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute("select id,firstname,lastname,docid,treatment_days,healthstatus,discharge,bloodgroup,dateofjoin,dateofdischarge from healthstatus where healthstatus='Cured'")
            if res > 0:
                details = cursor.fetchall()
                return render_template('cured3.html', details=details)
    finally:
        connection.close()

@app.route('/update_statusb3' , methods=['POST','GET'])
def update_statusb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3'
                                 )
    if request.method == 'POST':
        details=request.form
        id=details['id']
        healthstatus =details['healthstatus']
        treatment_days=details['treatment_days']
        discharge = details['discharge']
        dateofdischarge=details['dateofdischarge']

        try:
            with connection.cursor() as cursor:
                cursor.execute("update healthstatus set healthstatus=%s,treatment_days=%s,discharge=%s,dateofdischarge=%s  where id=%s", (healthstatus,treatment_days ,discharge, dateofdischarge,id))
                connection.commit()
                return redirect(url_for('recovered_statusb3'))
        finally:
            connection.close()

@app.route('/search_patientb3', methods=['POST','GET'])
def search_patientb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from patient where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('patient_result3.html', details=details)

    finally:
            connection.close()

@app.route('/search_doctorb3', methods=['POST','GET'])
def search_doctorb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from doctor where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('doctor_result3.html', details=details)

    finally:
            connection.close()

@app.route('/search_statusb3', methods=['POST','GET'])
def search_statusb3():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='mythili13',
                                 db='branch3')
    if request.method == 'POST':
        details = request.form
        id = details['id']
    try:
        with connection.cursor() as cursor:
             res=cursor.execute("select * from healthstatus where id=%s", (id))
             if res > 0:
                    details = cursor.fetchall()
                    return render_template('status_result3.html', details=details)

    finally:
            connection.close()

@app.route('/patient_full3')
def patient_full3():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch3')
    try:
        with connection.cursor() as cursor:
             res = cursor.execute('select patient.id,patient.firstname,patient.lastname,patient.age,patient.docid,patient.gender,healthstatus.healthstatus,healthstatus.treatment_days,healthstatus.discharge,patient.bloodgroup,healthstatus.dateofjoin,healthstatus.dateofdischarge,patient.dateofbirth,patient.occupation,patient.ph_num,patient.city from patient left join healthstatus on healthstatus.id=patient.id union select patient.id,patient.firstname,patient.lastname,patient.age,patient.docid,patient.gender,healthstatus.healthstatus,healthstatus.treatment_days,healthstatus.discharge,patient.bloodgroup,healthstatus.dateofjoin,healthstatus.dateofdischarge,patient.dateofbirth,patient.occupation,patient.ph_num,patient.city from patient right join healthstatus on healthstatus.id=patient.id')
             if res > 0:
                details = cursor.fetchall()
                return render_template('patient_join3.html', details=details)
    finally:
        connection.close()

@app.route('/login1', methods=['POST','GET'])
def login1():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='hospital01')

    if request.method == 'POST':
        id = request.form.get('id', False)
        password=request.form['password']
        try:
            with connection.cursor() as cursor:
                 cursor.execute('select password from credentials where id=%s and password=%s',(id,password))
                 pw= cursor.fetchone()
                 if pw:
                     return render_template('dashboard1.html')
                 else:
                     return 'Incorrect credentials'
        finally:
            connection.close()

@app.route('/login2',methods=['GET','POST'])
def login2():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch2')
    if request.method == 'POST':
        id = request.form.get('id', False)
        password=request.form['password']
        try:
            with connection.cursor() as cursor:
                 cursor.execute('select password from credentials where id=%s and password=%s',(id,password))
                 pw= cursor.fetchone()
                 if pw:
                     return render_template('dashboard2.html')
                 else:
                     return 'Incorrect credentials'
        finally:
             connection.close()

@app.route('/login3',methods=['GET','POST'])
def login3():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch3')
    if request.method == 'POST':
        id = request.form.get('id', False)
        password=request.form['password']
        try:
            with connection.cursor() as cursor:
                 cursor.execute('select password from credentials where id=%s and password=%s',(id,password))
                 pw= cursor.fetchone()
                 if pw:
                     return render_template('dashboard3.html')
                 else:
                     return 'Incorrect credentials'
        finally:
            connection.close()

@app.route('/home1')
def home1():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='hospital01')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute('select total_doctors,total_patients,total_recovered from stats order by row_num desc limit 1')
            if res > 0:
                details = cursor.fetchall()
                return render_template('homepage.html', details=details)
            else:
                return "NO"
    finally:
        connection.close()

@app.route('/home2')
def home2():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch2')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute('select total_doctors,total_patients,total_recovered from stats order by row_num desc limit 1')
            if res > 0:
                details = cursor.fetchall()
                return render_template('homepage2.html', details=details)
    finally:
        connection.close()

@app.route('/home3')
def home3():
    connection = pymysql.connect(host='localhost',
                          user='root',
                          password='mythili13',
                          db='branch3')
    try:
        with connection.cursor() as cursor:
            res = cursor.execute('select total_doctors,total_patients,total_recovered from stats order by row_num desc limit 1')
            if res > 0:
                details = cursor.fetchall()
                return render_template('homepage3.html', details=details)
    finally:
        connection.close()
if __name__=="__main__":
    app.run(debug=True)