from flask import *
import mariadb

app = Flask(__name__)
app.config["DEBUG"] = True


conn = mariadb.connect(
    user='root',
    password='',
    host='127.0.0.1',
    port=3307,
    database='kampus_db'
    )

dbMysql = conn.cursor()

@app.route('/alumni', methods=['GET'])
def index():
    dbMysql.execute("select * from alumni")

    row_headers = [x[0] for x in dbMysql.description]
    listData = dbMysql.fetchall()
    json_data = []
    for result in listData:
        json_data.append(dict(zip(row_headers, result)))


    return {
        "message":"success get data",
        "data":json_data}

@app.route('/add/alumni', methods=['POST'])
def addAlumni():
    nama = request.form['nama']
    nim = request.form['nim']
    jenisKelamin = request.form['jenis_kelamin']
    no_hp = request.form['no_hp']
    alamat = request.form['alamat']

    try:
        dbMysql.execute("INSERT INTO alumni (nama, nim, jenis_kelamin, no_hp, alamat) VALUES (?, ?, ?, ?, ?)",
                    (nama, nim, jenisKelamin, no_hp, alamat))
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.commit()
    return "success"

@app.route('/update/alumni/<id>', methods=['PUT'])
def updateAlumni(id):

    nama = request.form['nama']
    alamat = request.form['alamat']

    try:
        dbMysql.execute(f"UPDATE alumni set alamat=?, nama=? where id=?",
                    (alamat,nama, id))
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.commit()
    return "success"




@app.route('/delete/alumni/<id>', methods=['DELETE'])
def delateAlumni(id):

    try:
        dbMysql.execute(f"DELETE FROM alumni where id='{id}'")
    except mariadb.Error as e:
        print(f"Error: {e}")

    conn.commit()
    return "success"