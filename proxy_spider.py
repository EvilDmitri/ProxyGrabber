import urllib
from grab.spider import Spider, Task, Data
from grab import Grab, GrabError
import socket

import locale
enc = locale.getpreferredencoding()

import re
#ip_re = re.compile('((\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5]))')

BASE_PAGE = 'http://www.my-proxy.com/free-proxy-list'
THREADS = 1

import logging
logging.basicConfig(level=logging.DEBUG)

class ProxySpider(Spider):

    def prepare(self):
        self.own_ip = get_local_ip_address('8.8.8.8')
        self.good_proxies = []

    def task_generator(self):
        for x in range(1, 11):
            PAGE = BASE_PAGE + '-' + str(x) + '.html'
            yield Task('initial', url=PAGE)

    def task_initial(self, grab, task):
                    # Add to all <br> - '\n'
        raw_br_list = grab.xpath_list('//br')
        for item in raw_br_list:
            item.text = "\n"
        raw_text = grab.xpath_text('//*')

        ip_port_list = re.findall('[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+[:][0-9]+', raw_text)

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
            f.write(server)






def get_local_ip_address(target):
  ipaddr = ''
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target, 8000))
    ipaddr = s.getsockname()[0]
    s.close()
  except:
    pass
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


