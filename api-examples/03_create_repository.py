#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create a repository named "bluefish_geany"

import datetime

from migasfree_client.utils import get_mfc_version, get_hardware_uuid
from api_consumer import ApiConsumer


def main():
    user = "admin"
    api = ApiConsumer(user=user)

    version_name = get_mfc_version()
    version_id = api.get_id("versions", {"name": version_name})

    all_systems_id = api.get_id(
        "attributes",
        {"prefix": "SET", "value": "ALL SYSTEMS"}
    )

    uuid = get_hardware_uuid()

    cid = api.get_id("computers", {"uuid": uuid})

    attribute_cid = api.get_id("attributes", {"prefix": "CID", "value": cid})

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    repository_id = api.add(
            "repositories",
            {
                "name": "bluefish_geany",
                "toinstall": "bluefish geany",
                "date": today,
                "version": str(version_id),
                "attributes": [all_systems_id, attribute_cid]
            }
        )

    if repository_id:
        print "repository_id", repository_id
    else:
        print "ERROR: %s %s creating repository" % (api.status, api.reason)

if __name__ == "__main__":
    main()