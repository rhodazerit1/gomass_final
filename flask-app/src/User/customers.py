########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response
import json
from src import db


customers = Blueprint('customers', __name__)

# Update User information for user
@customers.route('/customers', methods=['PUT'])
def update_customer():
    cus_info = request.json
    cus_id = cus_info['id']
    first = cus_info['first_name']
    last = cus_info['last_name']
    company = cus_info['company']

    query = 'UPDATE customers SET first_name = %s, last_name = %s, company = %s where id = %s'
    data = (first, last, company, cus_id)
    cursor = db.get_db().cursor()
    x = cursor.execute(query, data)
    db.get_db().commit()
    return 'Customer info updated.'

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('select id, company, last_name,\
        first_name, job_title, business_phone from customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from customers where id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Delete User from DB
@customers.route('/customers/<userID>', methods=['DELETE'])
def delete_user(userID):
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM customers WHERE id = %s', (userID,))
    db.get_db().commit()
    return 'Customer deleted.', 200

"""
@customers.route('/customers/<userID>', methods=['DELETE'])
def delete_customer(userID):
    cursor = db.get_db().cursor()

    # Construct the SQL query for deleting the customer by ID
    query = 'DELETE FROM customers WHERE id = %s'
    data = (userID,)

    # Execute the SQL command and commit to the database
    cursor.execute(query, data)
    db.get_db().commit()
    
    # Check if the customer was deleted
    if cursor.rowcount == 0:
        # No customer was deleted, possibly because the customer did not exist
        return jsonify(message="Customer not found"), 404
    else:
        # Respond with success message and status code
        return jsonify(message="Customer deleted successfully"), 200
"""

# Add a new customer to the DB
@customers.route('/customers', methods=['POST'])
def add_customer():
    cus_info = request.json
    first = cus_info['first_name']
    last = cus_info['last_name']
    company = cus_info['company']

    query = 'INSERT INTO customers (first_name, last_name, company) VALUES (%s, %s, %s)'
    data = (first, last, company)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    
    new_customer_id = cursor.lastrowid
    
    response_data = {
        'message': 'Customer added successfully.',
        'customer_id': new_customer_id
    }
    
    return jsonify(response_data), 201
