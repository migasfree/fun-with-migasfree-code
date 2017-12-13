#!/usr/bin/env python
# -*- coding: utf-8 -*-

# List cid's name's and uuid's Computers

from migasfree_sdk import ApiToken


def main():
    user = "reader"
    api = ApiToken(user=user)

    for element in api.filter(
            "computers",
            {"status": "intended", "ordering": "id"}
        ):
        print element["id"], element["name"], element["uuid"]

if __name__ == "__main__":
    main()