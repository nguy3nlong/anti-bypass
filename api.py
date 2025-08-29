from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import re
import json
import time
from urllib.parse import unquote, quote

app = FastAPI()

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
    params = {'thongke_link': str(id)}

    response = requests.get('https://yeumoney.com/quangly/', params=params, headers=headers)
    if response.status_code == 200:
        html = response.text
        match = re.search(r'(\d+)\s*đ', html)
        if match:
            number = int(match.group(1))
            if number >= 500:
                return 'success-completed'
            elif number < 500:
                return 'fail-completed'
        else:
            return 'fail-data'
    else:
        return 'fail-auth'


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


@app.post("/yeumoney/check")
async def yeumoney_check(request: Request):
    body = await request.json()
    cookies = body.get("cookies")
    id = body.get("id")
    to = body.get("t")

    if not body:
        return JSONResponse({"e": "Vui lòng thêm json vào request"}, status_code=400)
    if not cookies:
        return JSONResponse({"e": "Vui lòng thêm cookies tài khoản hợp lệ"}, status_code=400)
    if not id:
        return JSONResponse({"e": "Vui lòng cung cấp id Yeumoney"}, status_code=400)
    if not to:
        return JSONResponse({"e": "Vui lòng cung cấp lựa chọn time"}, status_code=400)

    check = yeumoney(cookies, id, to)
    if check == 'success-completed':
        return JSONResponse({"s": "Xác thực thành công"}, status_code=200)
    elif check == 'fail-auth':
        return JSONResponse({"f": "Vui lòng kiểm tra lại Cookies"}, status_code=400)
    elif check == 'fail-completed':
        return JSONResponse({"f": "Người dùng chưa vượt link"}, status_code=400)
    elif check == 'fail-data':
        return JSONResponse({"f": "id bạn cung cấp không hợp lệ hoặc Server lỗi"}, status_code=400)
    else:
        return JSONResponse({"f": "Lỗi không xác định"}, status_code=400)


@app.post("/bbmkts/check")
async def bbmkts_check(request: Request):
    body = await request.json()
    cookies = body.get("cookies")
    id = body.get("id")
    to = body.get("t")

    if not body:
        return JSONResponse({"e": "Vui lòng thêm json vào request"}, status_code=400)
    if not cookies:
        return JSONResponse({"e": "Vui lòng thêm cookies tài khoản hợp lệ"}, status_code=400)
    if not id:
        return JSONResponse({"e": "Vui lòng cung cấp id Link BBMKTS"}, status_code=400)
    if not to:
        return JSONResponse({"e": "Vui lòng cung cấp lựa chọn time"}, status_code=400)

    check = bbmkts(cookies, id, to)
    if check == 'success-completed':
        return JSONResponse({"s": "Xác thực thành công"}, status_code=200)
    elif check == 'fail-auth':
        return JSONResponse({"f": "Vui lòng kiểm tra lại Cookies"}, status_code=400)
    elif check == 'fail-completed':
        return JSONResponse({"f": "Người dùng chưa vượt link"}, status_code=400)
    elif check == 'fail-data':
        return JSONResponse({"f": "id bạn cung cấp không hợp lệ hoặc Server lỗi"}, status_code=400)
    elif check == 'invalid-json':
        return JSONResponse({"f": "Lỗi server, json không hợp lệ"}, status_code=400)
    elif check == 'empty-data':
        return JSONResponse({"f": "Không có dữ liệu trong link, vui lòng kiểm tra lại ID"}, status_code=400)
    elif check == 'fail-html':
        return JSONResponse({"f": "Lỗi server, không tìm được ID của link"}, status_code=400)
    else:
        return JSONResponse({"f": "Lỗi không xác định"}, status_code=400)
