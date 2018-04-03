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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_users')
def get_users():
    return render_template('get_users.html', user_list=client.user_list)

if __name__ == '__main__':
    mersenne_powers = [2201, 2281, 3217, 4253, 4423, 9689, 11213]
    (power1, power2) = random.sample(mersenne_powers, 2)
    p = 2 ** power1 - 1
    q = 2 ** power2 - 1

    e, d, n = rsa_soln.generate_keys(p, q)


    client = Client(random.randint(5000, 8000), e, d, n)
    threading.Thread(
            target = client.start_listening,
            args = (None,)
    ).start()
    threading.Thread(
            target = client.send_initial_connect_message,
            args = (None,)
    ).start()

    app.run(debug=False, port = 5001)