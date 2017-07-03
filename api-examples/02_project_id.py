#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Print version_id

from migasfree_client.utils import get_mfc_version
from api_consumer import ApiConsumer


def main():
    user = "reader"
    api = ApiConsumer(user=user)

    project_name = get_mfc_version()

    project_id = api.get_id("projects", {"name": project_name})
    print "project_id:", project_id

if __name__ == "__main__":
    main()
