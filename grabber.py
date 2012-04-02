# /usr/bin/env/python
# -*-coding=utf-8-*-

import re
# Проcтое решение «в лоб», проверяющее не только цифры но и выход за пределы допустимых диапазонов
#?   ip4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
#???


from grab import Grab

g = Grab()

file_site_list = open('site_list.txt', 'r')



line_number = 1  # ))) Только для вывода в консоль

for site_address in file_site_list:
    
    g.go(site_address)

        # Этот кусок ставит на все <br> теги текст '\n'
    raw_br_list = g.xpath_list('//br')  
    for item in raw_br_list:
        item.text = "\n"
        
        # Получаем ВЕСЬ текст со страницы
    raw_text = g.xpath_text('//*')          # И неуклюже выбираем...  TODO Сделать правильно!!
    ip_port_list =  re.findall("[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+[:][0-9]+", raw_text)  
    
    
# ProxyList format
#       type  host  port [user pass]
#       (values separated by 'tab' or 'blank')
    file_to_write = open("ip-port.txt", "w")
    for elem in ip_port_list:
        elem.replace(":", " ") # !!!!!!
        file_to_write.write("socks5 " + elem + "\n")
    file_to_write.close()
    
    print "{} line done".format(line_number)
    line_number += 1





#pattern = "((?P<login>\w+):(?P<password>\w+)@)?(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:(?P<port>\d+))?"

#re.match(pattern, "12.34.56.789").groupdict()
#re.match(pattern, "12.34.56.789:80").groupdict()
#re.match(pattern, "john:pass@12.34.56.789:80").groupdict()













