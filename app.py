from flask import Flask, send_file, redirect
from flask_restful import Resource, Api, reqparse

import smtplib, ssl

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from hashlib import md5
#
# from os import mkdir
# from os.path import exists

from flask_cors import CORS

from email.mime.text import MIMEText

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

smtp_server = "smtp.gmail.com"
port = 465
sender_email = "turnsiy123@gmail.com"
receiver_email = "mcgradytansy@gmail.com"


with open('credential.csv') as file:
    password = file.read()

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('email')
parser.add_argument('subject')
parser.add_argument('message')

context = ssl.create_default_context()

body_template = \
"""
Subject: {}

{} from {}

{}
"""

class Listener(Resource):
    lib = []

    def post(self):
        args = parser.parse_args()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)

            content = body_template.format(args['subject'], args['name'], args['email'], args['message'])

            msg = MIMEText(content)

            msg['Subject'] = 'New portfolio contact'
            msg['From'] = sender_email
            msg['To'] = receiver_email

            server.sendmail(sender_email, receiver_email, msg.as_string())

        return None, 201

api.add_resource(Listener, '/contact')


''' Possible future function '''
# parser.add_argument('url')

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--hide-scrollbars')
# options.add_argument('window-size=1920,1080')

# class Capturer(Resource):
#     m = md5()
#     driver = webdriver.Chrome(options=options)
#
#     def get(self):
#         args = parser.parse_args()
#         url = args['url']
#
#         # Execute hash
#         self.m.update(url.encode())
#
#         file = 'images/{}.png'.format(self.m.hexdigest())
#
#         if not exists(file):
#             self.driver.get(url)
#             self.driver.save_screenshot(file)
#
#         return send_file(file, mimetype='image/png')

# api.add_resource(Capturer, '/capture')



if __name__ == '__main__':
    app.run(debug=False)

