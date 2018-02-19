#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Print project_id

from migasfree_client.utils import get_mfc_project
from migasfree_sdk.api import ApiToken


def main():
    user = "reader"
    api = ApiToken(user=user)

    project_name = get_mfc_project()

    project_id = api.id("projects", {"name": project_name})
    print "project_id:", project_id

if __name__ == "__main__":
    main()
