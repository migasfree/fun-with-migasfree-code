#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Change to status reserved the computers with label "ETQ-RED"

from __future__ import print_function
from migasfree_sdk.api import ApiToken


def main():
    user = "admin"
    api = ApiToken(user=user)

    # Get Label "ETQ-RED"
    prefix = "ETQ"
    value = "RED"
    try:
        attribute_id = api.id("attributes", {"prefix": prefix, "value": value})
    except:
        print("{}-{} not exists".format(prefix, value))
        return

    computers = api.filter(
        "computers",
        {"sync_attributes__id": attribute_id, "ordering": "id"}
    )

    i = 0
    for c in computers:
        print(c["name"], c["uuid"], c["status"])
        response = api.post(
            'computers/%i/status' % c["id"],
            {"status": "reserved"}
        )
        if api.is_ok(response.status_code):
            print("Status changed to: %s" % response.json()["status"])
        else:
            print("Error: %s %s changing status" % (response.status_code, response.json()))
        i += 1

    if not i:
        print("There are not computers with attribute {}-{}".format(prefix, value))


if __name__ == "__main__":
    main()
