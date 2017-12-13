#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create a repository named "bluefish_geany"

import datetime

from migasfree_client.utils import get_mfc_version, get_hardware_uuid
from migasfree_sdk import ApiToken


def main():
    user = "admin"
    api = ApiToken(user=user)

    project_name = get_mfc_version()
    project_id = api.id("projects", {"name": project_name})

    all_systems_id = api.id(
        "attributes",
        {"prefix": "SET", "value": "ALL SYSTEMS"}
    )

    uuid = get_hardware_uuid()

    cid = api.id("computers", {"uuid": uuid})

    attribute_cid = api.id("attributes", {"prefix": "CID", "value": cid})

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    data = {
        "name": "bluefish_geany",
        "packages_to_install": ["bluefish", "geany"],
        "start_date": today,
        "project": project_id,
        "included_attributes": [all_systems_id, attribute_cid]
    }

    deployment_id = api.add("deployments", data)

    if deployment_id:
        print "deployment_id", deployment_id


if __name__ == "__main__":
    main()
