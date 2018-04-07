import sys
sys.path.append('../sockserv')
sys.path.append('../python')
from client import Client
import random
import threading
import rsa_soln
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

client = None
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/get_users')
def get_users():
  return render_template('get_users.html', user_list = client.user_list)

@app.route('/send_message')
def send_message():
  msg = request.args.get('msg')
  to_message = request.args.get('tomsg').split(',')
  print(to_message)
  for user in to_message:
    threading.Thread(
        target = client.send_message,
        args = (msg, user)
    ).start()
  return ''

@app.route('/get_messages')
def get_messages():
  return render_template('get_messages.html', messages = client.messages)

if __name__ == '__main__':
  mersenne_powers = [107, 127, 521, 607, 1279, 2203, 2281]
  (power1, power2) = random.sample(mersenne_powers, 2)
  p = 2 ** power1 - 1
  q = 2 ** power2 - 1

  e, d, n = rsa_soln.generate_keys(p, q)

  web_port = random.randint(2500, 4000) * 2
  print('Running on port {}'.format(web_port))

  username = input("Please enter a username: ").replace(',', '').strip()
  host_addr = input("Please enter the host address: ")

  client = Client(web_port + 1, e, d, n, host_addr, username)
  threading.Thread(
      target = client.start_listening,
      args = (None,)
  ).start()
  threading.Thread(
      target = client.send_initial_connect_message,
      args = (None,)
  ).start()

  app.run(debug=False, port = web_port)
