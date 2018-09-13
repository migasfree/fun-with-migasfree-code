#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Print computer's tags

from migasfree_client.utils import get_mfc_project
from migasfree_sdk.api import ApiToken


def main():
    user = "reader"
    api = ApiToken(user=user)

    cid=1

    # METHOD 1
    data = api.get("computers", {"id": cid})
    print data["tags"]

    # METHOD 2
    data = api.get("computers/" + str(cid), {})
    print data["tags"]


if __name__ == "__main__":
    main()
