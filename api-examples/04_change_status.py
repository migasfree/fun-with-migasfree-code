#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Change to status reserved the computers with label "ETQ-RED"

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
        print "ETQ-RED not exists"
        return

    computers = api.filter(
        "computers",
        {"sync_attributes__id": attribute_id, "ordering": "id"}
    )
    for c in computers:
        print c["name"], c["uuid"], c["status"]
        response = api.post(
            'computers/%i/status' % c["id"],
            {"status": "reserved"}
        )
        if api.is_ok(response.status_code):
            print "Status changed to: %s" % response.json()["status"]
        else:
            print "Error: %s %s changing status" % (response.status_code, response.json())

if __name__ == "__main__":
    main()
