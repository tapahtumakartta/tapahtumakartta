# Import modules
from flask import Flask
from flask import request
import json
import time
import hashlib


# function gen_hash
# params:
# for_admin - bool - tells function to generate either an admin or user hash
# brief:
# Generates an md5 hash based on the current epoch time
def gen_hash(for_admin):
    # Generate "randomness" using the current epoch time
    epoch = str(time.time())

    # Generate a hash from the time str
    hash_str = hashlib.md5(epoch.encode()).hexdigest()

    # If a hash for the admin was requested, make a longer one
    if for_admin:
        hash_str += hashlib.md5(epoch.encode()).hexdigest()
    return hash_str


# Initiate the api app
api = Flask(__name__)


# REST API paths:
# new_map handler
# params:
# markers - json string - marker data
# brief:
# Takes marker data and parses it into
# a Python map and processes and saves it
@api.route('/new_map', methods=['GET', 'POST'])
def new_map():
    try:
        # Marker data from the request
        markers = request.form('q')
        # Parse from a json string into a map
        markers = json.loads(markers)

        # Get hashes for the admin and the user views
        hash_admin = gen_hash(True)
        hash_user = gen_hash(False)

        # Build a dict from the response parts and
        # turn it into a json string and return
        response = {
            "status": 200,
            "admin_hash": hash_admin,
            "user_hash": hash_user
        }
        return json.dumps(response)
    except TypeError:
        # Print an error if the marker data is flawed
        response = {"status": 400}
        return json.dumps(response)


if __name__ == '__main__':
    api.run(debug=True)
