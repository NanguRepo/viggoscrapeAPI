"""Router for Viggoscrape.xyz"""
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import os
import json
from flask import render_template, request, jsonify, send_from_directory, Flask
from scraper import get_assignments
import scraper_v2

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/', methods=['GET'])
def home():
    """The homepage"""
    return render_template('landing.html')

@app.route('/old', methods=['GET'])
def homeold():
    """The old homepage, for nostalgia"""
    return render_template('landing-old.html')

@app.route('/favicon.ico')
def favicon():
    """Website icon"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                                'favicon.ico', mimetype='image/vnc.microsoft.icon')

@app.route('/placeholder')
def placeholder():
    """A placeholder"""
    return render_template('placeholder.html')

@app.route('/examples')
def examples():
    """Return the examples page"""
    # return render_template("examples.html")
    return "UNDER CONSTRUCTION!"

@app.route('/_nav.html')
def nav():
    """Return the nav page"""
    return render_template("nav.html")

@app.route('/_demo.html')
def demo():
    """Return the demo hero"""
    return render_template("demo.html")

@app.route('/api/v2/assassin', methods=['GET'])
def assassin():
    with open("values.json", "r") as file:
        values = json.load(file)
    input = ""
    try:
        input = request.args['name'].upper().replace('_', ' ')
        return values[input]
    except:
        return jsonify({
            'DEMAND': None,
            'VALUE': None,
            'OBTAIN': None,
            'ORIGIN': None
        })

@app.route('/api/v1/scrape', methods=['GET'])
def scrape():
    """Route to access scraper v1. Outdated!!"""
    args = format_args(dict(request.args))
    if "errors" in args:
        return jsonify(args)

    return jsonify(
        get_assignments(
            args
        )
    )

@app.route('/api/v2/scrape', methods=['GET'])
def scrape_v2():
    """
    Route to access scraper v2.
    Takes subdomain, username, password, date, and groupByAssignment
    """
    args = format_args(dict(request.args))
    if "errors" in args:
        return jsonify(args)

    viggo = scraper_v2.Viggoscrape()
    viggo.login_data = {
        "username": args['username'],
        "password": args['password']
    }
    viggo.subdomain = args['subdomain']
    viggo.date_selected = args['date']
    viggo.group_by_assignment = bool(int(args['groupByAssignment']))

    return jsonify(
        viggo.get_assignments()
    )

def format_args(args):  # sourcery skip: remove-redundant-if
    """Sanitizes input"""
    error_list = []
    if 'date' not in args:
        args['date'] = None
    if 'groupByAssignment' not in args:
        args['groupByAssignment'] = "1"
    if not args['groupByAssignment'].isdigit():
        error_list.append("Property groupByAssignment is not an integer")
    elif int(args['groupByAssignment']) not in [0, 1]:
        error_list.append(
            f"""
            Property groupByAssignment is not 0 or 1, recieved {args['groupByAssignment']} instead
            """
        )
    if 'subdomain' not in args:
        error_list.append("No subdomain provided")
    if 'username' not in args:
        error_list.append("No username provided")
    if 'password' not in args:
        error_list.append("No password provided")
    if error_list:
        return {
            "errors": error_list
        }
    if args['subdomain'] == '':
        return {"errors": ["Subdomain field is empty."]}

    return args

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
