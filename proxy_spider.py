import urllib
from grab.spider import Spider, Task, Data
from grab import Grab, GrabError

import locale
enc = locale.getpreferredencoding()

import re
#ip_re = re.compile('((\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5])\.(\d{1,2}|1\d{2}|2[0-4][0-9]|25[0-5]))')

BASE_PAGE = 'http://www.my-proxy.com/free-proxy-list'


import logging
logging.basicConfig(level=logging.DEBUG)

class ProxySpider(Spider):

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
        self.store_(ip_port_list)
        check(ip_port_list)


    def store_(self, ip_port_list):
        file_to_write = open("ip-port(http).txt", "w")

        for elem in ip_port_list:
            elem = str(elem)
            elem.replace(":", "\t")
            file_to_write.write(elem + "\n")

        file_to_write.close()


import socket

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


def check(ip_port):
    own_ip = get_local_ip_address('8.8.8.8')
    g = Grab()

    proxy_list = []
    for addr in ip_port:

        g.setup(proxy=addr, proxy_type='http', connect_timeout=10, timeout=15)

        try:
            g.go('http://www.icanhazip.com')
        except GrabError:
            pass
        if g.tree.text_content() and g.tree.text_content()==own_ip:
            print addr
            proxy_list.append(addr)
            print proxy_list




def main():
    threads = 1
    bot = ProxySpider(thread_number=threads,network_try_limit=10)

    try: bot.run()
    except KeyboardInterrupt: pass

    print bot.render_stats()

if __name__ == '__main__':
    main()


