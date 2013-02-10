# /usr/bin/env/python
# -*-coding=utf-8-*-

import os, re

from grab import Grab




def spiderman(file_site_list):
    line_number = 1  # For console output
    
    for site in file_site_list:
        temp = site.split()
        socks_type = temp[0]
        site_address = temp[1]
        
        g.go(site_address)
    
        ip_port_list = find_()

        store_(ip_port_list, socks_type)        
        
        print "{} line done".format(line_number)
        line_number += 1
    
    file_site_list.close()
    print "All sites done."
    

def find_():
                # Add to all <br> - '\n'
    raw_br_list = g.xpath_list('//br')  
    for item in raw_br_list:
        item.text = "\n"

        # Receive all text from page
    raw_text = g.xpath_text('//*')
    return(re.findall('[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+[:][0-9]+', raw_text))


def find_proxies():
    pass


    
    
def store_(ip_port_list, socks_type):
    '''
    Store received "type ip port" list
    '''
    file_to_write = open("ip-port.txt", "a")
    
    for elem in ip_port_list:                  #  ProxyList format
        elem = elem.replace(":", "\t")       #    type  host  port [user pass]
        file_to_write.write(socks_type + "\t" + elem + "\n")
            
    file_to_write.close()



if __name__ == '__main__':
    g = Grab()

    file_site_list = open('site_list.txt', 'r')
    spiderman(file_site_list)
















