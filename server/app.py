import json
from urllib.request import urlopen
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    with open('server/index.html', 'rt', encoding='utf-8') as f:
        content = f.read()
        f.close()
    return content


@app.route('/lunchmenu', methods=['POST'])
def lunchmenu():
    f = open('server/requesttemplate.json', 'rt', encoding='UTF8')
    data_str = f.read()
    data = json.loads(data_str)
    time = data['action']['detailParams']['date']['value']
    print(f'time : {time}')

    # 학교 급식 api 메뉴 사이트에서 급식메뉴 json 파일을 크롤링해온다. 해당 사이트 프로젝트 : https://github.com/5d-jh/school-menu-api
    school_type = 'high'
    school_code = 'B100000505'
    year, month, date = time.split('-')
    URL = f'https://schoolmenukr.ml/api/{school_type}/{school_code}?year={year}&month={month}&date={date}'

    result = json.loads(urlopen(URL).read().decode('utf-8'))
    menus = result["menu"][0]["lunch"]
    menu_today: str = ','.join(menus)

    response = {'version': '1.0', 'template': {'outputs': [{'simpleText': {'text': menu_today}}]}}
    print(f'{data["userRequest"]["block"]["name"]} : {data["userRequest"]["user"]["id"]} requested menu skill. return value : {response}')
    return response


if __name__ == '__main__':
    app.run(port='80')
