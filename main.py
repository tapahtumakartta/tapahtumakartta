# Import modules
from flask import Flask, render_template, request
import string
import random
import json
import time
import hashlib
import os


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
# Define map data dir
MATH_PATH = "maps/"


# Server paths:
# -------------
# root handler
# brief:
# Show an error message by default as the root
# is not used for API use
@api.route('/')
def index():
    return render_template(FRONTEND,
                           site_title="Luo kartta",
                           map_dict={},
                           btn_type="Jaa tämä kartta",
                           btn_function="sendData(true)"
                           )


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

        # Write marker data into a file
        file_name = "maps/" + hash_admin + "_" + hash_user
        target_file = open(file_name, "w")
        target_file.write(json.dumps(markers))
        target_file.close()

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
# map handler for user
# brief:
# Displays a shared map associated with
# the given hash
@api.route('/u/<user_hash>')
def show_map(user_hash):
    map_files = os.listdir(MATH_PATH)
    map_str = "Error"

    for i in map_files:
        if i.split("_")[1] == user_hash:
            map_data = open("maps/" + i, "r")
            map_str = map_data.read()
            break

    return map_str


# map handler for admin
# brief:
# Displays a shared map associated with
# the given hash
@api.route('/a/<admin_hash>')
def show_admin_panel(admin_hash):
    map_files = os.listdir(MATH_PATH)
    map_str = "Error"

    for i in map_files:
        if i.split("_")[0] == admin_hash:
            map_data = open("maps/" + i, "r")
            map_str = map_data.read()
            break

    return render_template(FRONTEND,
                           site_title="Muokkaa karttaa",
                           map_dict=map_str,
                           btn_type="Tallenna kartta",
                           btn_function="sendData(false)"
                           )


if __name__ == '__main__':
    api.run(port=8001)
