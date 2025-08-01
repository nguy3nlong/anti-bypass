from flask import Flask, request, send_from_directory, jsonify
import os
import requests
import random
import string
import re
import time
app = Flask(__name__)

def yeumoney(cookies, id, t='False'):
    if t == 'True':
        time.sleep(10)
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.7',
    'priority': 'u=0, i',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Cookie': cookies
    }
    params = {
    'thongke_link': str(id),
    }

    response = requests.get('https://yeumoney.com/quangly/', params=params, headers=headers)
    if response.status_code == 200:
        html = response.text
        match = re.search(r'(\d+)\s*đ', html)
        if match:
            number = int(match.group(1))
            if number > 500 or number == 500:
                return('success-completed')
            elif number < 500 or number != 500:
                return('fail-completed')
        else:
            return('fail-data')
    else:
        return('fail-auth')

@app.route('/yeumoney/check', methods=['POST'])
def yeumoney_check():
    json = request.get_json()
    if not json:
        return jsonify({'e': 'Vui lòng thêm json vào request'}), 400
    cookies = json['cookies']
    if not cookies:
        return jsonify({'e': 'Vui lòng thêm cookies tài khoản hợp lệ'}), 400
    id = json['id']
    if not id:
        return jsonify({'e': 'Vui lòng cung cấp id Yeumoney'}), 400
    to = json['t']
    if not to:
        return jsonify({'e': 'Vui lòng cung cấp lựa chọn time'}), 400
    check = yeumoney(cookies, id)
    if check == 'success-completed':
        return jsonify({'s': 'Xác thực thành công'}), 200
    elif check == 'fail-auth':
        return jsonify({'f': 'Vui lòng kiểm tra lại Cookies'}), 400
    elif check == 'fail-completed':
        return jsonify({'f': 'Người dùng chưa vượt link'}), 400
    elif check == 'fail-data':
        return jsonify({'f': 'id bạn cung cấp không hợp lệ hoặc Server lỗi'}), 400
