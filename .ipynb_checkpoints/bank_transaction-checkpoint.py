import os
from bottle import route, run, template, request, response
import json
import urllib.request
import ssl
from datetime import datetime
from bottle import get, post
from re import sub
# from bottle_postgresql import Database
import psycopg2

url = "https://s3-ap-southeast-1.amazonaws.com/he-public-data/bankAccountdde24ad.json"

ssl._create_default_https_context = ssl._create_unverified_context

index_html = '''Hello {{author}}'''

# with Database() as connection:
#     (
#         connection
#         .select('test')
#         .paging(0, 10)
#     )

# db = Database()

@route('/')
def index():
    return template(index_html, author="Callify")

@get('/transactions/<date>')
def date_transactions(date):
    try:
        date_transactions = list()
        with urllib.request.urlopen("https://s3-ap-southeast-1.amazonaws.com/he-public-data/bankAccountdde24ad.json") as url:
            resp = url.read()
            output = resp.decode('utf-8')
            try:
                data = json.loads(output)
                changed_date = datetime.strptime(date, '%d-%m-%y')
                changed_date_dt = changed_date.strftime('%d %b %y')
                for req in data:
                    if req['Date'].strip() == changed_date_dt.strip():
                        date_transactions.append(req)
            except:
                raise ValueError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'date_transactions': date_transactions})

@get('/balance/<date>')
def date_balance(date):
    try:
        balance_sum = 0
        with urllib.request.urlopen("https://s3-ap-southeast-1.amazonaws.com/he-public-data/bankAccountdde24ad.json") as url:
            resp = url.read()
            output = resp.decode('utf-8')
            try:
                data = json.loads(output)
                changed_date = datetime.strptime(date, '%d-%m-%y')
                changed_date_dt = changed_date.strftime('%d %b %y')
                for req in data:
                    if req['Date'].strip() == changed_date_dt.strip():
                        balance_sum += float(sub(r'[^\d.]', '', req['Balance AMT']))
                print(balance_sum)
            except:
                raise ValueError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'balance_sum': balance_sum})


@get('/details/<ID>')
def date_balance(ID):
    try:
        ID_transactions = list()
        balance_sum = 0
        with urllib.request.urlopen("https://s3-ap-southeast-1.amazonaws.com/he-public-data/bankAccountdde24ad.json") as url:
            resp = url.read()
            output = resp.decode('utf-8')
            try:
                data = json.loads(output)
                for req in data:
                    if str(req['Account No']) == ID:
                        ID_transactions.append(req['Transaction Details'])
                print(ID_transactions)
            except:
                raise ValueError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'ID_transactions': ID_transactions})

@route('/add', method='GET')
def show_form():
    return '''<form method="POST" action="/add">
                <input name="account_num" type="text" placeholder="Account Number"/>
                <br>
                <input name="transaction_details" type="text" placeholder="Transaction Details"/>
                <br>
                <input name="withdraw_amt" type="text" placeholder="Withdrawal AMT"/>
                <br>
                <input name="deposit_amt" type="text" placeholder="Deposit AMT"/>
                <br>
                <input type="submit" />
              </form>'''


@route('/add', method='POST')
def add_transactions():
    try:
        account_num = request.forms.get('account_num')
        transaction_details = request.forms.get('transaction_details')
        withdraw_amt = request.forms.get('withdraw_amt')
        deposit_amt = request.forms.get('deposit_amt')
        # postdata = request.body.read()
        print(account_num, transaction_details, withdraw_amt, deposit_amt)
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    # return json.dumps({'ID_transactions': ID_transactions})
    return 


if __name__ == '__main__':
    port = int(os.environ.get('PORT',8080))
    run(host='127.0.0.1',port=port, debug=True)

