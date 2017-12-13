#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hardware to csv

from migasfree_sdk import ApiToken
import os

if __name__ == "__main__":

    user = "reader"
    fields = [
        'id', 'name', 'product', 'cpu', 'ram', 'disks',
        'storage', 'project.name', 'mac_address', 'ip_address'
    ]
    output = "hardware.csv"

    api = ApiToken(user=user)
    api.csv(
        'computers',
        {"status": "intended", "ordering": "id"},
        fields,
        output
    )
    os.system("xdg-open %s" % output)