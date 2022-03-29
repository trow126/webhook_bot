import os
import configparser
from flask import Flask, request, abort
import random
import time
import pandas as pd
import datetime

app = Flask(__name__)

@app.route('/')
def root():
    return 'online'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        time.sleep(random.uniform(1,2))

        # Get the message from the POST body
        message = request.get_json(force=True)
        # 受信時間,アラート名,取引所,通貨ペア,ロット,ポジション

        df = pd.DataFrame(index=[0], columns=['timestamp', 'alert_name', 'exchange', 'pair', 'lot', 'position'])
        
        df['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['alert_name'] = message['alert_name']
        df['exchange'] = message['exchange']
        df['pair'] = message['pair']
        df['lot'] = message['lot']
        df['position'] = message['position']
        df.to_pickle('./alert_tmp.pkl')

        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, 'setting.ini')
    config = configparser.ConfigParser()
    config.read(file_path, 'utf_8_sig')
    webhook_host = config.get('webhook', 'HOST')
    webhook_port = config.getint('webhook', 'PORT')

    app.run(host=webhook_host, port=webhook_port)