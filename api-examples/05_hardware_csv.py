#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hardware to csv

from api_consumer import ApiConsumer
import os

if __name__ == "__main__":

    output = 'hardware.csv'
    user = "reader"
    endpoint = 'computers'
    fieldnames = ['id', 'name', 'product', 'cpu', 'ram', 'disks',
        'storage', 'project.name', 'mac_address', 'ip_address']
    params = {"status": "intended", "ordering": "id"}

    api = ApiConsumer(user=user)
    api.csv(endpoint, params, fieldnames, output)

    os.system("xdg-open %s" % output)


