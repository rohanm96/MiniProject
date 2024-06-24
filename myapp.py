from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

connection = pymysql.connect(
    host = 'devopsdemodb.cdgcwgoq6pwq.ap-south-1.rds.amazonaws.com',
    user = 'admin',
    password = 'root1234',
    db ='miniprojectdb',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)

@app.route('/')
def welcome():
    return '<center><h1>Welcome to Hospital Management System</h1></center>'

@app.route('/hospital', methods=['POST'])
def add_hospital():
    hospital_data = request.get_json()
    print(hospital_data)

    if not all(key in hospital_data for key in ('name', 'mobile', 'email', 'address', 'location', 'pincode')):
        return jsonify({"Error":"Missing Hospital Data"}), 400
    
    with connection.cursor() as cursor:
        sql = 'INSERT INTO hospital(name, mobile, email, address, location, pincode) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (hospital_data['name'], int(hospital_data['mobile']), hospital_data['email'], hospital_data['address'], hospital_data['location'], int(hospital_data['pincode'])))
    connection.commit()

    return jsonify({"Message":"Hospital addded successfully!!"}), 201

@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM hospital'
        cursor.execute(sql)
        result = cursor.fetchall()
    
    return jsonify({"Hospitals":result}), 200

@app.route('/hospital/<int:code>', methods=['PUT'])
def update_hospital(code):
    hospital_data = request.get_json()
    print(hospital_data)

    if not all(key in hospital_data for key in ('code', 'name', 'mobile', 'email', 'address', 'location', 'pincode')):
        return jsonify({"Error":"Missing Hospital Data"}), 400
    
    with connection.cursor() as cursor:
        sql = "UPDATE hospital SET code = %s, name = %s, mobile = %s, email = %s, address = %s, location = %s, pincode = %s WHERE code = %s"
        cursor.execute(sql, (int(hospital_data['code']), hospital_data['name'],  int(hospital_data['mobile']), hospital_data['email'], hospital_data['address'], hospital_data['location'], int(hospital_data['pincode']), int(code)))
    connection.commit()

    return jsonify({"Message":"Hospital updated successfully"}), 200

@app.route('/hospital/<int:code>', methods=['DELETE'])
def delete_hospital(code):
    with connection.cursor() as cursor:
        sql = "DELETE FROM hospital WHERE code = %s"
        cursor.execute(sql, int(code))
    connection.commit()
    
    return jsonify({"Message":"Hospital Deleted Successfully"}), 200               

if __name__ == "__main__":
    app.run(host = '0.0.0.0')