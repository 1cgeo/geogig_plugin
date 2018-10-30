# -*- coding: utf-8 -*-

import sys,os
#10.2.1.54 nepomuceno
#10.2.1.53 alegranzi
#10.2.1.61 lunardi
#10.2.1.59 mendonca
#10.2.1.57 carvalho
#10.2.1.55 tolfo
#10.2.1.58 castro
#10.2.1.56 henrique
lista = ['10.2.1.53','10.2.1.55','10.2.1.57','10.2.1.54','10.2.1.56','10.2.1.58','10.2.1.59','10.2.1.61']
for item in lista:
    print 'iniciando: {0}'.format(item)
    #os.system("net rpc service status gg_backup  -I {0} -U administrador{1}senha | grep gg_backup".format(item,'%'))
    os.system("net rpc service status gg_commit_push  -I {0} -U administrador{1}senha".format(item,'%'))
    #os.system("net rpc service status gg_commit_push  -I {0} -U administrador{1}senha | grep gg_commit_push".format(item,'%'))