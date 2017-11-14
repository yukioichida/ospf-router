#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve, json, datetime
 
# Classe de acesso a dados externos
class DataAccess:
 
    def __init__(self):
        self.host_file = "hosts.dat"
        self.request_file = "requests.json"
        self.dns_file = "dns.json"

    def get_host(self, ip):
        data = shelve.open(self.host_file)
        host = data.get(ip,None)
        data.close()
        return host

    def set_host(self, ip, host):
        data = shelve.open(self. host_file)
        data[ip] = host
        data.close()

    def save_request(self, ip, url):
        self.save_url(self.request_file, ip, url)

    def save_url(self, file, ip, url):
        # Recupera a collection
        data = self.create_data(ip, url)
        fd = open(file, 'r')
        collection = fd.readline()
        fd.close()
        collection = collection.replace("data = ","").replace("'","")
        # Adiciona a requisição
        collection = json.loads(collection)
        collection.append(data)
        #trata o dado
        collection = "data = '%s'" % (json.dumps(collection))
        # Atualiza a collection
        fd = open(file,'w')
        fd.write(collection)
        fd.close()


    def save_dns(self, ip, dns):
        self.save_url(self.dns_file, ip, dns)


    def create_data(self, ip, url):
        host = self.get_host(ip)
        now = datetime.datetime.now()
        data = dict()
        data["data"] = now.strftime("%d/%m/%Y %H:%M")
        data["ip"] = ip
        data["name"] = host
        data["url"] = url
        return data
