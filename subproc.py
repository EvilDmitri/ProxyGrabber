# -*-coding=utf-8-*-


import subprocess

if __name__ == '__main__':
    
    proc = subprocess.Popen("ping 8.8.8.8 -c 6", shell=True, stdout=subprocess.PIPE)

    for output in proc.stdout.readline(): #читаем строку - вывод 
        print output



