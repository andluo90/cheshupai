# -*-coding:utf-8-*-
import json,threading,time
from urllib import request
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def get_token(phone_num):
    auth_code = 'http://api.guazipai.com/customer/login/code/?phone=%d' % phone_num
    res = request.urlopen(auth_code)
    print (res.read().decode("utf-8"))
    code = str(input('请输入验证码： '))
    login_url = 'http://api.guazipai.com/customer/login/submit/?phone=%d&code=%s' % (phone_num, code)
    print (request.urlopen(login_url).read().decode('utf-8'))
    json_result = json.loads(request.urlopen(login_url).read().decode("utf-8"))
    print (json_result['message'])
    print (json_result['data']['user_id'])
    print (json_result['data']['pai_token'])
    return json_result['data']['pai_token']


def auction(token, id, price,ssid):
    # http://api.guazipai.com/customer/order/bid/?id=691419&price=8200&lat=0&lng=0&bread=f43f216e4f16fa7894dd90bbc786bf56
    start = datetime.now()
    print ('Start:', start.strftime('%Y-%m-%d %H:%M:%S'))
    auction_url = 'http://api.guazipai.com/customer/order/bid/?id=%d&price=%d&lat=22.543096&lng=114.05786499999999&bread=%s' % (
    id, price,ssid)
    req = request.Request(auction_url)
    # req.add_header('User-Agent',
    #                'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A346 Safari/602.1')
    req.add_header('User-Agent',
                   'Mozi1lla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    req.add_header('PAI-TOKEN', token)
    response = request.urlopen(req)
    response = response.read().decode("UTF-8")
    print (response)
    result = json.loads(response)
    print (result['code'])
    print (result['message'])
    try:
        for item in result['data']['state']:
            print ('  ', item, result['data']['state'][item])
    except TypeError:
        pass
    except KeyError:
        print("Key Error!")

    end = datetime.now()
    print ('End:', end.strftime('%Y-%m-%d %H:%M:%S'))
    print ('Elapsed time:', (end - start).seconds)


# profile_url = 'http://api.guazipai.com/customer/user/profile/'
# response = opener.open(profile_url)

def get_result(token, id):
    # http://api.guazipai.com/customer/user/list/?page=1&status=0
    usre_list = 'http://api.guazipai.com/customer/user/list/?page=1&status=0'
    req = request.Request(usre_list)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    req.add_header('PAI-TOKEN', token)
    response = request.urlopen(req)
    response = response.read().decode("UTF-8")
    result = json.loads(response)
    list = result['data']['list']
    for item in list:
        if item['id'] == str(id):
            for (k, v) in item.items():
                print (k, ':', v)
    else:
        print ('Can not find the id %d' % id)

def run():
    phone_dict = {
        '13045866804': 'c9c84464d13ee91b434ad22e7c809d9a',
        '13650723808': '30e068dda8d6dd71678e96531b0e749f',
        '18122445507': '740be926da66478ba0966cc78af6f106',
        '13760808820': 'addf68fe42539c74d0b9e5ae510c9737',
        '18126600062': '31152f8bf095f23167996ccb182e0733'}
    try:
        threading.Thread(target=auction,args=(phone_dict['13045866804'],707312,5000,'d77aaf4e2e2a0e7cb302cf48ef381c98')).start()


    except Exception:
        print ('Thread start error...')

    time.sleep(30)

def set_time_to_run(time=()):
    if not time:
        scheduler = BlockingScheduler()
        scheduler.add_job(run, 'cron', day_of_week='1-7', hour=time[0], minute=time[1], second=time[2])
        scheduler.start()
        scheduler.shutdown()
    else:
        run()


if __name__ == '__main__':
    time = (18,10,00)
    set_time_to_run(time)


