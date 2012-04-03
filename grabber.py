# /usr/bin/env/python
# -*-coding=utf-8-*-
import subprocess
import re
# Проcтое решение «в лоб», проверяющее не только цифры но и выход за пределы допустимых диапазонов
#?   ip4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
#???


#pattern = "((?P<login>\w+):(?P<password>\w+)@)?(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:(?P<port>\d+))?"

#re.match(pattern, "12.34.56.789").groupdict()
#re.match(pattern, "12.34.56.789:80").groupdict()
#re.match(pattern, "john:pass@12.34.56.789:80").groupdict()

from grab import Grab

g = Grab()

file_site_list = open('site_list.txt', 'r')



line_number = 1  # ))) Только для вывода в консоль

for site in file_site_list:
    # Разобрать строку на socks_type и site_address
    temp = site.split()
    socks_type = temp[0] + "\t"
    site_address = temp[1]
    
    g.go(site_address)

        # Этот кусок ставит на все <br> теги текст '\n'
    raw_br_list = g.xpath_list('//br')  
    for item in raw_br_list:
        item.text = "\n"
        
        # Получаем ВЕСЬ текст со страницы
    raw_text = g.xpath_text('//*')          # И неуклюже выбираем...  TODO Сделать правильно!!
    ip_port_list =  re.findall("[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+[:][0-9]+", raw_text)  
    
    
# ProxyList format
#    type  host  port [user pass]

    file_to_write = open("ip-port.txt", "a")

    for elem in ip_port_list:
        elem = elem.replace(":", "\t")
        file_to_write.write(socks_type + elem + "\n")
        
    file_to_write.close()
    
    print "{} line done".format(line_number)
    line_number += 1

file_site_list.close()
print "All sites done."
print "Now checking addresses for..."


# Проверка адресов на рабочесть)))
# Используется YAPH через proxychains

proc = subprocess.Popen("cat ip-port.txt | sort | uniq | proxychains yaph --use_hunter_stdin", shell=True, stdout=subprocess.PIPE)

#for output in proc.stdout.readline(): #читаем строку - вывод 
is_data = True
while is_data: 
    data = proc.stdout.readline()
    if data:
        print data
    else: is_data = False

print "It's over"

# удалить файл ip-port.txt
os.remove("ip-port.txt")

















