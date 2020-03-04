from pymongo import MongoClient
import configparser
from bson.objectid import ObjectId
from datetime import datetime


def initialize():
    config = configparser.ConfigParser()
    config.read('config.ini')
    connection_str = config['database']['mongo_connection']
    client = MongoClient(connection_str)
    global users
    global vendors

    db = client["foodster-user"]
    users = db.users
    vendors = db.vendors
    print("foodster-user database initialized")


# insert or update user details
def upsert_user(user):
    if '_id' in user:
        doc = {'firstName': user['firstName'],
               'lastName': user['lastName'],
               'email': user['email'],
               'password': user['password'],
               'dob': user['dob'],
               'following': user['following']}
        print("udpating")
        users.update_one(
            {'_id': ObjectId(user['_id'])},
            {'$set': doc}
        )

    else:
        users.insert_one({'firstName': user['firstName'],
                          'lastName': user['lastName'],
                          'email': user['email'],
                          'password': user['password'],
                          'dob': user['dob'],
                          'following': []})


def find_user(user):
    temp = users.find_one({'email': user['email']})
    if temp:
        return str(temp['_id'])
    else:
        return "failure"

# insert or update vendor details


def upsert_vendor(vendor):
    if '_id' in vendor:
        print("updating")
        doc = {
            'name': vendor['name'],
            'location': vendor['location'],
            'latitude': vendor['latitude'],
            'longitude': vendor['longitude'],
            'email': vendor['email'],
            'password': vendor['password'],
            'description': vendor['description'],
            'posts': vendor['posts']
        }
        vendors.update_one(
            {'_id': ObjectId(vendor['_id'])},
            {'$set': doc}
        )
    else:
        vendors.insert_one({
            'name': vendor['name'],
            'location': vendor['location'],
            'latitude': vendor['latitude'],
            'longitude': vendor['longitude'],
            'email': vendor['email'],
            'password': vendor['password'],
            'description': vendor['description'],
            'posts': []
        })


def find_vendor(vendor):
    temp = vendors.find_one({'email': vendor['email']})
    if temp:
        return str(temp['_id'])
    else:
        return "failure"


def add_new_post(id, data):
    vendor = vendors.find_one({'_id': ObjectId(id)})
    posts = vendor['posts']
    doc = {
        'description': data['description'],
        'validFrom': data['validFrom'],
        'validUntil': data['validUntil'],
        'timeStamp': data['timeStamp']
    }
    posts.append(doc)
    vendor['posts'] = posts
    upsert_vendor(vendor)
    # print(vendor)


def follow_vendor(user_id, vendor_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    following = user['following']
    if vendor_id not in following:
        following.append(vendor_id)
        user['following'] = following
        upsert_user(user)
    user['_id'] = str(user['_id'])
    user['id'] = str(user['_id'])
    return user


def unfollow_vendor(user_id, vendor_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    following = user['following']
    if vendor_id in following:
        following.remove(vendor_id)
        user['following'] = following
        upsert_user(user)
    user['_id'] = str(user['_id'])
    user['id'] = str(user['_id'])
    return user


def get_all_vendors():
    data = vendors.find()
    all_vendors = list()
    for each in data:
        temp = str(each['_id'])
        each['_id'] = temp
        each['id'] = temp
        all_vendors.append(each)
    return all_vendors


def get_wall_feed(id):
    user = users.find_one({'_id': ObjectId(id)})
    following = user['following']
    post_list = list()
    for each in following:
        temp = vendors.find_one({'_id': ObjectId(each)})
        for post in temp['posts']:
            post_list.append({
                'id': str(temp['_id']),
                'name': temp['name'],
                'location': temp['location'],
                'email': temp['email'],
                'description': temp['description'],
                'post': post
            })
    sorted_posts = sorted(
        post_list, key=lambda x: datetime.strptime(x['post']['timeStamp'], "%Y-%m-%dT%H:%M:%S"))

    posts_sorted = sorted_posts[::-1]
    # for each in post_list:
    #     print(each['post'])

    # print("_---------------")
    # for each in sorted_posts:
    #     print(each['post'])
    # print("_---------------")

    # for each in posts_sorted:
    #     print(each['post'])
    return posts_sorted


def get_vendor_info(vendorId):
    vendor = vendors.find_one({'_id': ObjectId(vendorId)})
    vendor['_id'] = str(vendor['_id'])
    vendor['id'] = vendor['_id']
    return vendor


def get_user_info(userId):
    user = users.find_one({'_id': ObjectId(userId)})
    user['_id'] = str(user['_id'])
    user['id'] = user['_id']
    return user


def debuging():
    initialize()
    user = find_user({'email': 'bmulmi@ramapo.edu'})
    vendor = find_vendor({'email': 'sodexomyway@ramapo.edu'})
    dat = follow_vendor(user, vendor)
    # get_wall_feed(user)
    print(dat)


# debuging()
# t = find_user({'email': 'bulmi@ramapo.edu'})
# add_new_post(temp_id, [])
# print(t)
