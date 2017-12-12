#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import subprocess
import os
import httplib
import json
import urllib
import platform
import csv

from distutils.sysconfig import get_python_lib


if not get_python_lib() in sys.path:
    sys.path.append(get_python_lib())

from migasfree_client.utils import get_config
from migasfree_client import settings as client_settings


def getUserPath():
    _platform = platform.system()
    if _platform == 'Linux':
        _env = "HOME"
    elif _platform == 'Windows':
        _env = "USERPROFILE"
    return os.getenv(_env)


class ApiConsumer():
    def __init__(self, user, token="", URLPathVersioning="/api/v1/token"):
        self.user = user
        self.URLPathVersioning = URLPathVersioning

        _token_file = self.token_file()

        config = get_config(client_settings.CONF_FILE, 'client')
        self.host = config.get('server', 'localhost')
        self.connection = httplib.HTTPConnection(self.host)

        if token:
            self.token = token
        else:
            if not os.path.exists(_token_file):
                password = self.get_password()
                if password:
                    data = json.dumps({"username": user, "password": password})
                    headers = {"Content-type": "application/json"}
                    self.connection.request(
                        'POST',
                        '/token-auth/',
                        data,
                        headers)

                    response = self.connection.getresponse()
                    status = response.status
                    body = response.read()
                    if status == httplib.OK:
                        with open(_token_file, 'w') as handle:
                            handle.write(json.loads(body)["token"])
                    else:
                        print("Error")
                        print(status)
                        print(body)
                        exit()

            with open(_token_file, "r") as handle:
                self.token = handle.read()

        self.headers = {
            "Content-type": "application/json",
            "Authorization": "Token %s" % self.token
        }

    def token_file(self):
        return os.path.join(
            getUserPath(),
            ".migasfree-token.%s" % self.user
        )

    def get_password(self):
        cmd = "zenity --title 'Password for %s in %s' --password 2>/dev/null" % (
            self.user,
            self.host
        )
        try:
            password = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=True
            )
        except:
            password = None
        return password

    def __request(self, method, endpoint, data={}, params={}):
        data = json.dumps(data)

        if params:
            params = '?' + urllib.urlencode(params)
        else:
            params = ''

        self.connection.request(
            method,
            '%s/%s/%s' % (self.URLPathVersioning, endpoint, params),
            data,
            self.headers
        )
        response = self.connection.getresponse()
        self.status = response.status
        self.reason = response.reason
        self.body = response.read()

        if self.is_forbidden() and \
                json.loads(self.body)["detail"] == "Invalid token.":
            os.remove(self.token_file())

    def get_id(self, endpoint, params):
        return self.get(endpoint, params)["id"]

    def get(self, endpoint, params):
        self.__request("GET", endpoint, params=params)
        if self.is_ok():
            data = json.loads(self.body)
            if data["count"] == 1:
                return data["results"][0]
            elif data["count"] == 0:
                raise Exception('Not found')
            else:
                raise Exception('Multiple records found')

    def filter(self, endpoint, params={}):
        page = 1
        while page:
            params["page"] = page
            self.__request("GET", endpoint, params=params)
            if self.is_ok():
                for element in json.loads(self.body)["results"]:
                    yield element
                page += 1
            else:
                page = None

    def post(self, endpoint, data):
        self.__request("POST", endpoint, data=data)
        if self.is_ok():
            return json.loads(self.body)

    def patch(self, endpoint, data):
        self.__request("PATCH", endpoint, data=data)
        if self.is_ok():
            return json.loads(self.body)

    def add(self, endpoint, data):
        self.__request("POST", endpoint, data=data)
        if self.is_created():
            return json.loads(self.body)["id"]

    def is_ok(self):
        return self.status == httplib.OK

    def is_created(self):
        return self.status == httplib.CREATED

    def is_forbidden(self):
        return self.status == httplib.FORBIDDEN

    def csv(self, endpoint, params={}, fieldnames=[], output="output.csv"):

        def render_line(element, fieldnames):
            line = {}
            for keys in fieldnames:
                x = element
                for key in keys.split('.'):
                    x = x[key]
                    line[keys] = x
            return line

        with open(output, 'wb') as csvfile:
            if fieldnames:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            for element in self.filter(endpoint, params):
                if not fieldnames:
                    fieldnames = element.keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                writer.writerow(render_line(element, fieldnames))