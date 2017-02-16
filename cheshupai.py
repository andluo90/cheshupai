# -*-coding:utf-8-*-
import urllib2,json,thread,time
from datetime import datetime


def get_token(phone_num):
    auth_code = 'http://api.guazipai.com/customer/login/code/?phone=%d' % phone_num
    res = urllib2.urlopen(auth_code)
    print res.read()
    code = str(raw_input('请输入验证码： '))
    login_url = 'http://api.guazipai.com/customer/login/submit/?phone=%d&code=%s' % (phone_num, code)
    print urllib2.urlopen(login_url).read()
    json_result = json.loads(urllib2.urlopen(login_url).read())
    print json_result['message']
    print json_result['data']['user_id']
    print json_result['data']['pai_token']
    return json_result['data']['pai_token']


def auction(token, id, price):
    # http://api.guazipai.com/customer/order/bid/?id=691419&price=8200&lat=0&lng=0&bread=f43f216e4f16fa7894dd90bbc786bf56
    start = datetime.now()
    print 'Start:', start.strftime('%Y-%m-%d %H:%M:%S')
    auction_url = 'http://api.guazipai.com/customer/order/bid/?id=%d&price=%d&lat=0&lng=0&bread=f43f216e4f16fa7894dd90bbc786bf56' % (
    id, price)
    req = urllib2.Request(auction_url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    req.add_header('PAI-TOKEN', token)
    response = urllib2.urlopen(req)
    response = response.read()
    print response
    result = json.loads(response)
    print result['code']
    print result['message']
    try:
        for item in result['data']['state']:
            print '  ', item, result['data']['state'][item]
    except TypeError:
        pass
    end = datetime.now()
    print 'End:', end.strftime('%Y-%m-%d %H:%M:%S')
    print 'Elapsed time:', (end - start).seconds


# profile_url = 'http://api.guazipai.com/customer/user/profile/'
# response = opener.open(profile_url)

def get_result(token, id):
    # http://api.guazipai.com/customer/user/list/?page=1&status=0
    usre_list = 'http://api.guazipai.com/customer/user/list/?page=1&status=0'
    req = urllib2.Request(usre_list)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    req.add_header('PAI-TOKEN', token)
    response = urllib2.urlopen(req)
    response = response.read()
    result = json.loads(response)
    list = result['data']['list']
    for item in list:
        if item['id'] == str(id):
            for (k, v) in item.items():
                print k, ':', v
    else:
        print 'Can not find the id %d' % id

def testaa(cont):
    print cont

if __name__ == '__main__':
    phone_dict = {
        '13045866804': 'c9c84464d13ee91b434ad22e7c809d9a',
        '13650723808': '30e068dda8d6dd71678e96531b0e749f',
        '18122445507': 'c28711a5f19224b07cb0bc018767de02',
        '13760808820': 'addf68fe42539c74d0b9e5ae510c9737'}
    try:
        thread.start_new_thread(auction,(phone_dict['13650723808'],692374,125000))
        thread.start_new_thread(auction, (phone_dict['13650723808'], 692374, 125000))
        thread.start_new_thread(auction, (phone_dict['13650723808'], 692374, 125000))
    except Exception:
        print 'Thread start error...'

    time.sleep(15)


    # get_token(18122445507)
    # auction('c28711a5f19224b07cb0bc018767de03',692374,125000)

    # auction('c28711a5f19224b07cb0bc018767de03', 692449, 100000)
    #get_result(phone_dict['13760808820'], 694130)
