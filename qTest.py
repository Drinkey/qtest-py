#!/usr/bin/env python

"""
This lib is created for interact with qTest
"""
import os
import sys
import json
import requests
from requests.auth import AuthBase

CACHE_PATH='.'
QTEST_API_VERSION='v3'

class qTestAuth(AuthBase):
    """
    This class implemented qTest authentication process
    """
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.url = url

    def login(self):
        url = self.url + '/oauth/token'
        headers = {
            'Authorization':'Basic bGluaC1sb2dpbjo=',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        request_body = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

        response = requests.post(url=url, data=request_body, headers=headers)
        return response.json()

    def __call__(self, r):
        token = self.login()
        r.headers['Authorization'] = '%s %s' % (token['token_type'], token['access_token'])
        return r

class qTest(object):
    """
    qTest interface class
    """
    def __init__(self, instance_url, username, password, project, use_cache=False):
        self.url = '%s/api/%s' % (instance_url, QTEST_API_VERSION)
        print "API Gateway: %s" % self.url

        self.project_name = project
        self.use_cache = use_cache
        
        self.session = requests.Session()
        self.session.auth = qTestAuth(instance_url, username, password)

        self.project_id = self.get_projectid_by_name(self.project_name)
        if not self.project_id:
            print "Unable to find Project ID, exiting.."
            return None

        self.fields = None
    
    def projects(self):
        url = '%s/projects' % self.url
        print "GET %s" % url
        proj = self.session.get(url=url)
        return proj.json()
    
    def get_projectid_by_name(self, name):
        print "Trying to find out project_id for %s" % name
        try:
            return [p['id'] for p in self.projects() if p['name'] == name][0]
        except:
            print "cannot found name %s" % name
            return None

if __name__ == "__main__":
    q = qTest(
        instance_url='https://xxxxxxxxxxxxxxx.qtestnet.com',
        username='cccccccccccccc',
        password='ffffffffffffff',
        project='Wtest',
        use_cache=True
        )
    # q.test_case_fields()
    print q.convert_test_case('6463948')
    print "============================="
    print q.convert_test_case('6463870')
