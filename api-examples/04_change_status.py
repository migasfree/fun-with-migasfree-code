#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Change to status reserved the computers with label "ETQ-RED"

from api_consumer import ApiConsumer


def main():
    user = "admin"
    api = ApiConsumer(user=user)

    # Get Label "ETQ-RED"
    prefix = "ETQ"
    value = "RED"
    attribute_id = api.get_id("attributes", {"prefix": prefix, "value": value})

    computers = api.filter(
        "computers",
        {"login__attributes__id": attribute_id, "ordering": "id"}
    )

    for c in computers:
        print c["name"], c["uuid"], c["status"]
        response = api.post(
            'computers/%i/status' % c["id"],
            {"status": "reserved"}
        )
        if api.is_ok():
            print"Status changed to: %s" % response["status"]
        else:
            print "Error: %s %s changing status" % (api.status, api.reason)

if __name__ == "__main__":
    main()