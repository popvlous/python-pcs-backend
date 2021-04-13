# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
 
import hashlib, binascii, os
import json
from flask import request
import requests

user_name = "pyrarc.app"
user_passwd = "dOidZQSGR09BnHROt4ss#NT3"
end_point_url_posts = "https://store.pyrarc.com/wp-json/jwt-auth/v1/token"

payload = {
    "username": user_name,
    "password": user_passwd
}

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_pass( password ):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash) # return bytes

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def getCustomerNameById(customer_id):
    r = requests.post(end_point_url_posts, data=payload)
    jwt_info = r.content.decode("utf-8").replace("'", '"')
    data = json.loads(jwt_info)
    s = json.dumps(data, indent=4, sort_keys=True)
    print(s)
    token = data['token']
    Auth_token = "Bearer " + token
    my_headers = {'Authorization': Auth_token}
    response_customers = requests.get('https://store.pyrarc.com/wp-json/wc/v3/customers/'+ str(customer_id), data=payload,
                                      headers=my_headers)
    customerlist = json.loads(response_customers.content.decode("utf-8").replace("'", '"'))
    return customerlist
