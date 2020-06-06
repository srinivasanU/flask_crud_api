from flask import Flask, jsonify ,request,Response,send_from_directory
import psycopg2
import json
from psycopg2.extras import RealDictCursor
from psycopg2.extras import Json, DictCursor
from db import dbconnection
from json import dumps
from conversion import get_dict_resultset
import pandas as pd
from werkzeug.utils import secure_filename

conn = dbconnection()
cur = conn.cursor(cursor_factory=DictCursor)
app = Flask(__name__)

@app.route('/contacts', methods=['GET','POST'])
def createcontact():
    if (request.method == 'POST'):
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone_no = request.form.get('phone_no')
        cur.execute("insert into contacts (firstname,lastname,phone_no) values(%s,%s,%s)",(firstname,lastname,phone_no));
        conn.commit()
        return  jsonify({'Message': 'Contact Added Successfully'}),200
    elif (request.method == 'GET'):
        sql = "select * from contacts";
        contacts = get_dict_resultset(sql)
        return  jsonify({'Message': 'Contacts Retreived Successfully', 'Contact_list': contacts}),200
    else:
        return jsonify({'Message':'Method Not Allowed'}),405

 
@app.route('/contacts/<contact_id>', methods=['GET','PUT','DELETE'])
def altercontact(contact_id):
    if (request.method == 'PUT'):
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone_no = request.form.get('phone_no')
        contact_id = contact_id
        cur.execute("update contacts SET firstname = %s , lastname = %s , phone_no = %s  WHERE contact_id = %s" , (firstname,lastname,phone_no,contact_id));
        conn.commit();
        return  jsonify({'Message': 'Contact Updated Successfully'}),200
    elif (request.method == 'DELETE'):
        contact_id = contact_id
        cur.execute("DELETE FROM contacts WHERE contact_id = " + (contact_id));
        conn.commit();
        return  jsonify({'Message': 'Contact Deleted Successfully'}),200
    elif (request.method == 'GET'):
        contact_id = contact_id
        sql = "select * from contacts where contact_id = " + contact_id;
        contacts = get_dict_resultset(sql)
        return  jsonify({'Message': 'Contact Retreived Successfully', 'Contact_list': contacts}),200
    else:
        return jsonify({'Message':'Method Not Allowed'}),405





@app.route('/import_contacts', methods=['POST'])
def import_contacts():
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file:
            filename = secure_filename(file.filename)
            re = pd.read_excel(str(filename), sheet_name='Sheet1')
            final_res = re.to_dict('records')
            for row in final_res:
                cur.execute("insert into contacts (lastname,phone_no,firstname) values(%s,%s,%s)",(str(row['lastname']),str(row['phone_no']),str(row['firstname'])));
            conn.commit()
            resp = jsonify({'message' :'File successfully uploaded'})
            resp.status_code = 201
            return resp
    else:
        return jsonify({'Message':'Method Not Allowed'}),405
        
if __name__ == '__main__':
    app.run(debug=True)