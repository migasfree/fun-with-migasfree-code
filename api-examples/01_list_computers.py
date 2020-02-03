#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Show computers' CID, name and UUID

from __future__ import print_function
from migasfree_sdk.api import ApiToken


def main():
    user = "reader"
    api = ApiToken(user=user)

    for element in api.filter(
        "computers",
        {"status": "intended", "ordering": "id"}
    ):
        print(element["id"], element["name"], element["uuid"])


if __name__ == "__main__":
    main()
