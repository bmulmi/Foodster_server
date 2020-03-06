from flask import Flask, request, jsonify
from database import *

app = Flask(__name__)

initialize()


@app.route("/")
def index():
    return "Server is up and running again!!"


'''
@app.route('/login', methods=['POST'])
def login_index():
    login_data = request.form.copy()
    user_id = find_user(login_data)
    if user_id:
        return user_id
    else:
        return ("failure")


def checkLoginValidation(data):
    if data["email"] == user["username"] and data["password"] == user["password"]:
        return True
    else:
        return False


@app.route('/vendorlogin', methods=['POST'])
def vendor_login():
    login_data = request.form.copy()
    vendor_id = find_vendor(login_data)
    if vendor_id:
        return vendor_id
    else:
        return ("failure")


@app.route('/signup', methods=['POST'])
def signup_index():
    user_data = request.form.copy()
    print("data recieved")
    for each in user_data:
        print(user_data[each])
    upsert_user(user_data)
    user_id = find_user(user_data)
    return str(user_id)


@app.route('/home/<id>', methods=['GET'])
def home_index(id):
    data = get_wall_feed(id)
    print(jsonify(data))
    return (jsonify(data))


@app.route('/vendorsignup', methods=['POST'])
def signup_vendor():
    vendor_data = request.form.copy()
    print("vendor data recieved")
    for each in vendor_data:
        print(vendor_data[each])
    upsert_vendor(vendor_data)
    vendor_id = find_vendor(vendor_data)
    return str(vendor_id)


@app.route('/vendorwall/<id>', methods=['GET'])
def vendorwall_index(id):
    dat = get_vendor_info(id)
    return (jsonify(dat))


@app.route('/vendorpost/<id>', methods=['GET', 'POST'])
def vedorpost_index(id):
    if request.method == 'GET':
        return "F"
    else:
        vendor_data = request.form.copy()
        print(vendor_data)
        print(id)
        add_new_post(id, vendor_data)
        return "success"


@app.route('/search', methods=['GET'])
def search_vendors():
    data = get_all_vendors()
    print(jsonify(data))
    return (jsonify(data))


@app.route('/vendorinfo/<id>', methods=['GET'])
def vendorpage_index(id):
    data = get_vendor_info(id)
    return(jsonify(data))


@app.route('/userinfo/<id>', methods=['GET'])
def userinfo_index(id):
    data = get_user_info(id)
    return(jsonify(data))


@app.route('/unfollow/<uid>/<vid>', methods=['POST'])
def unfollow(uid, vid):
    updated_user = unfollow_vendor(uid, vid)
    return (jsonify(updated_user))


@app.route('/follow/<uid>/<vid>', methods=['POST'])
def follow(uid, vid):
    updated_user = follow_vendor(uid, vid)
    return (jsonify(updated_user))
'''

if __name__ == "__main__":
    app.run()
