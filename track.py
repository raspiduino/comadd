# Got from https://medium.com/@tarunkhare54321/track-website-browsing-time-using-python-838552fc0ede
# Edited by raspiduino for ComAdd

from flask import Flask, jsonify, request
import time
import os
from datetime import date

app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
prev_url = ""

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime
    global prev_url

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent
    
    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url

    if os.name == "nt":
    	log = open("weblog\\weblog"+date.today().strftime("%d%m%y")+".txt", "a+")
    else:
        log = open("weblog/weblog"+date.today().strftime("%d%m%y")+".txt", "a+")
    log.write("\n" + str(url_viewtime))
    log.close()

    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=['POST'])
def quit_url():
    return jsonify({'message': 'quit success!'}), 200

app.run(host='0.0.0.0', port=5000)
