
from grab.spider import Spider, Task, Data
from grab import Grab, GrabError


import locale
enc = locale.getpreferredencoding()

BASE_PAGE = 'http://www.freeproxylists.net/ru/?page=1'
PAGE = 'http://www.freeproxylists.net/ru/?page='
ICAN = 'http://icanhazip.com/'

THREADS = 1

import logging
logging.basicConfig(level=logging.DEBUG)

class ProxySpider(Spider):

    def prepare(self):
        self.own_ip = get_local_ip_address()
        self.good_proxies = []

    def task_generator(self):
        yield (Task('cookie', url=BASE_PAGE))


    def task_cookie(self, grab, task):
        for x in range(1, 2):
            page = PAGE + str(x)
            grab.setup(url=page)
            yield Task('initial', grab=grab)



    def task_initial(self, grab, task):
        table = grab.xpath('//table[@class="DataGrid"]')
        del table[0]    # Remove table header

        ip_port_list = []
        for tr in table:
            ip = ''
            port = ''
            type = ''
            if u'IPDecode' in tr[0].text_content():
                ip = decode_hex(tr[0].text_content().split('"')[1])
                port = tr[1].text
                type = tr[2].text
                anonymity = tr[3].text
                country = tr[4].text_content()
                ip_port = ip + ':' + port
                ip_port_list.append(ip_port)

        print ip_port_list

        for ip in ip_port_list:
            grab = Grab()
            grab.setup(url='http://www.icanhazip.com')
            grab.setup(proxy=ip, proxy_type='http', connect_timeout=10, timeout=15)
            info = {'server': ip, 'type': 'http'}
            yield Task('proxy_check', grab=grab, info=info)




    def task_proxy_check(self, grab, task):
        ip = grab.tree.text_content()
        if ip == self.own_ip:
            pass
        else:
            #self.good_proxies.append()
            self.store_(task.info['server'])



    def store_(self, server):
        with open("ip-port(http).txt", "a") as f:
            f.write(server+'\n')


def decode_hex(str):
    real_str =  ''.join([ch.decode('hex') for ch in str[1:].split('%')])
    return real_str.split('>')[1].split('<')[0]


def get_local_ip_address():
    g = Grab()
    g.go(ICAN)
    ipaddr = g.tree.text
    return ipaddr



def main():

    bot = ProxySpider(thread_number=THREADS,network_try_limit=10)

    try:
        bot.run()
    except KeyboardInterrupt:
        pass


    print bot.render_stats()

if __name__ == '__main__':
    main()


