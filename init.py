# -*- coding: utf-8 -*-
# @Time    : 18-1-3 下午3:27
# @Author  : Juicpt
# @Site    :
# @File    : init.py
# @Software: PyCharm

import subprocess
version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)

def java_install(n):
    # java_ppa = ['sudo','add-apt-repository','ppa:webupd8team/java']
    # update = ['sudo','apt-get','update']
    # jdk7 = ['sudo','apt-get','install','oracle-java7-installer']
    # jdk8 = ['sudo','apt-get','install','oracle-java8-installer']
    # jdk7_acc = ['echo','oracle-java7-installer','shared/accepted-oracle-license-v1-1','select true','|','sudo','/usr/bin/debconf-set-selections']
    # jdk8_acc = ['echo','oracle-java8-installer','shared/accepted-oracle-license-v1-1','select true','|','sudo','/usr/bin/debconf-set-selections']

    openjdk_ppa = 'sudo add-apt-repository ppa:openjdk-r/ppa'
    java_ppa = 'sudo add-apt-repository ppa:webupd8team/java -y'
    update = 'sudo apt-get update'
    openjdk7 = 'sudo apt-get install -y openjdk-7-jdk'
    jdk7 = 'sudo apt-get install -y oracle-java7-installer'
    jdk8 = 'sudo apt-get install -y oracle-java8-installer'
    jdk7_acc = 'echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections'
    jdk8_acc = 'echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections'

    if n == 7:
        subprocess.check_call(openjdk_ppa, shell=True)
        print('添加成功')
        subprocess.check_call(update, shell=True)
        print('更新成功')
        # subprocess.check_call(jdk7_acc, shell=True)
        # print('协议同意')
        subprocess.check_call(openjdk7, shell=True)
        print('安装成功')
    elif n == 8:
        subprocess.check_call(java_ppa, shell=True)
        subprocess.check_call(update, shell=True)
        subprocess.check_call(jdk8_acc, shell=True)
        subprocess.check_call(jdk8, shell=True)
    else:
        print('参数错误')


if __name__ == '__main__':
    java_install(7)