from flask import Flask, request, send_from_directory, jsonify
import os
from urllib.parse import unquote, quote
import requests
import random
import string
import re
import json
import time
app = Flask(__name__)

def bbmkts_id(html, target):
    target_encoded = quote(unquote(target), safe='')
    target_variants = {
        target.strip(),
        unquote(target.strip()),
        f"https://bbmkts.com/go/{target_encoded.strip()}"
    }

    blocks = re.findall(r'<div class="link__user-list">(.*?)</div>\s*</div>', html, re.DOTALL)

    for block in blocks:
        chart_match = re.search(r'<a href="https://bbmkts\.com/site/link/chart/(\d+)"', block)
        go_match = re.search(r'value="(https://bbmkts\.com/go/[^"]+)"', block)

        if chart_match and go_match:
            chart_id = chart_match.group(1)
            go_link_raw = go_match.group(1)
            go_link_decoded = unquote(go_link_raw)

            if go_link_raw.strip() in target_variants or go_link_decoded.strip() in target_variants:
                return chart_id

    return None


def yeumoney(cookies, id, t='False'):
    if t == 'True':
        time.sleep(10)
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.7',
    'priority': 'u=0, i',
    'upgrade-insecure-requests': '1',
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

def bbmkts(cookies, bid, t='False'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://bbmkts.com/site/all-link',
        'Cookie': cookies
    }

    r1 = requests.get('https://bbmkts.com/site/all-link', headers=headers)
    html1 = r1.text
    target = f"https://bbmkts.com/go/{bid}"
    result = str(bbmkts_id(html1, target))
    if result == 'None':
        return 'fail-html'
    if t == 'True':
        time.sleep(10)
    response = requests.get(f'https://bbmkts.com/site/link/chart/{result}', headers=headers)

    if response.status_code == 200:
        html = response.text
        match = re.search(r"const\s+actuals\s*=\s*JSON\.parse\('(\[.*?\])'\)", html)

        if match:
            try:
                data = json.loads(match.group(1))

                if any(x > 0 for x in data):
                    return 'success-completed'
                elif any(x == 0 for x in data):
                    return 'fail-completed'
                else:
                    return 'empty-data'
            except json.JSONDecodeError:
                return 'invalid-json'
        else:
            return 'fail-data'
    else:
        return 'fail-auth'
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
    check = yeumoney(cookies, id, to)
    if check == 'success-completed':
        return jsonify({'s': 'Xác thực thành công'}), 200
    elif check == 'fail-auth':
        return jsonify({'f': 'Vui lòng kiểm tra lại Cookies'}), 400
    elif check == 'fail-completed':
        return jsonify({'f': 'Người dùng chưa vượt link'}), 400
    elif check == 'fail-data':
        return jsonify({'f': 'id bạn cung cấp không hợp lệ hoặc Server lỗi'}), 400
    else:
        return jsonify({'f': 'Lỗi không xác định'}), 400
@app.route('/bbmkts/check', methods=['POST'])
def bbmkts_check():
    json = request.get_json()
    if not json:
        return jsonify({'e': 'Vui lòng thêm json vào request'}), 400
    cookies = json['cookies']
    if not cookies:
        return jsonify({'e': 'Vui lòng thêm cookies tài khoản hợp lệ'}), 400
    id = json['id']
    if not id:
        return jsonify({'e': 'Vui lòng cung cấp id Link BBMKTS'}), 400
    to = json['t']
    if not to:
        return jsonify({'e': 'Vui lòng cung cấp lựa chọn time'}), 400
    check = bbmkts(cookies, id, to)
    if check == 'success-completed':
        return jsonify({'s': 'Xác thực thành công'}), 200
    elif check == 'fail-auth':
        return jsonify({'f': 'Vui lòng kiểm tra lại Cookies'}), 400
    elif check == 'fail-completed':
        return jsonify({'f': 'Người dùng chưa vượt link'}), 400
    elif check == 'fail-data':
        return jsonify({'f': 'id bạn cung cấp không hợp lệ hoặc Server lỗi'}), 400
    elif check == 'invalid-json':
        return jsonify({'f': 'Lỗi server, json không hợp lệ'}), 400
    elif check == 'empty-data':
        return jsonify({'f': 'Không có dữ liệu trong link, vui lòng kiểm tra lại ID'}), 400
    elif check == 'fail-html':
        return jsonify({'f': 'Lỗi server, không tìm được ID của link'}), 400
    else:
        return jsonify({'f': 'Lỗi không xác định'}), 400
