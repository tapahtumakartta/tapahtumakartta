# Import modules
from flask import Flask, render_template
from flask import request
import string
import random
import json
import time
import hashlib


# function gen_hash
# params:
# for_admin - bool - tells function to generate either an admin or user hash
# brief:
# Generates an md5 hash based on the current epoch time
def gen_hash(for_admin):
    if for_admin:
        # Generate "randomness" using the current epoch time
        epoch = str(time.time())

        # Generate a hash from the time str for admins
        # Probability of collision 2.9387359e-39
        hash_str = hashlib.md5(epoch.encode()).hexdigest()
    else:
        # For user hash, generate a short random string
        # Probability of collision 4.5800105e-15
        hash_str = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))

    return hash_str


# Initiate the api app
api = Flask(__name__)


# Define the path to the frontend interface
FRONTEND = "index.html"
# Define an REST API path
REST = "/rest/"


# Server paths:
# -------------
# root handler
# brief:
# Show an error message by default as the root
# is not used for API use
@api.route('/')
def index():
    return render_template(FRONTEND)


# REST API paths:
# ---------------
# new_map handler
# params:
# markers - json string - marker data
# brief:
# Takes marker data and parses it into
# a Python map and processes and saves it
@api.route(REST + 'new_map', methods=['GET', 'POST'])
def new_map():
    try:
        # Marker data from the request
        # Parse from a json string into a map
        markers = json.loads(request.data)

        # Get hashes for the admin and the user views
        hash_admin = gen_hash(True)
        hash_user = gen_hash(False)

        # Build a dict from the response parts and
        # turn it into a json string and return
        response = {
            "success": True,
            "markers": len(markers),
            "admin_hash": hash_admin,
            "user_hash": hash_user
        }
        json_response = json.dumps(response)
        return json_response
    except:
        # Print an error if the marker data is flawed
        response = {"success": False}
        return json.dumps(response)


# Map paths:
# ----------
# map handler
# brief:
# Displays a shared map associated with
# the given hash
@api.route('/map')
def show_map():
    return "Showing a map"


if __name__ == '__main__':
    api.run(port=8001)
