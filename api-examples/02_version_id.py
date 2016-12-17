#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Print version_id

from migasfree_client.utils import get_mfc_version
from api_consumer import ApiConsumer


def main():
    user = "reader"
    api = ApiConsumer(user=user)

    version_name = get_mfc_version()

    version_id = api.get_id("versions", {"name": version_name})
    print "version_id:", version_id

if __name__ == "__main__":
    main()
