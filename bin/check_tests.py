#!/usr/bin/python2

"""
A script that collects information about tests and outputs to
results.csv file.
"""

import os
import re
import csv
import urllib2
import json

ROOT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
CHALICE2SILVER_TEST_DIR = os.path.join(
        ROOT_DIR, 'chalice2silver/src/test/resources')
SILVER_TEST_DIR = os.path.join(
        ROOT_DIR, 'silver/src/test/resources')
TEAM = 'viperproject'

class TestChecker(object):

    def __init__(self, test_suite, writer):
        self._cache = {}
        self.test_suite = test_suite
        self._writer = writer
        self.ignore_file = re.compile('^(IgnoreFile)\(/(.*)/issue/([0-9]+)/\)$')
        self.missing_output =  re.compile('^(MissingOutput)\(.*, /(.*)/issue/([0-9]+)/\)$')
        self.expected_output = re.compile('^(UnexpectedOutput)\(.*, /(.*)/issue/([0-9]+)/\)$')

    def construct_url(self, project, local_id):
        url = 'https://api.bitbucket.org/1.0/repositories/{0}/{1}/issues/{2}'.format(
            TEAM,
            project.lower(),
            local_id)
        return url

    def get_status(self, project, local_id):
        key = (project, local_id)
        if key in self._cache:
            return self._cache[key]
        url = self.construct_url(project, local_id)
        try:
            data = urllib2.urlopen(url).read()
        except:
            print url
            raise
        issue = json.loads(data)
        self._cache[key] = issue[u'status']
        return issue[u'status']

    def check_annotation(self, match):
        if match:
            annotation, project, local_id = match.groups()
            if local_id == '000':
                status = 'n/a'
            else:
                try:
                    status = self.get_status(project, local_id)
                except:
                    print self.test_suite, self._path, annotation, project, local_id
                    raise
            self._writer.writerow(
                    [
                        self.test_suite,
                        self._path,
                        annotation,
                        project,
                        local_id,
                        status
                        ])

    def check_file(self, path):
        with open(path) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith('//:: '):
                    line = line[5:]
                    self.check_annotation(self.ignore_file.match(line))
                    self.check_annotation(self.missing_output.match(line))
                    self.check_annotation(self.expected_output.match(line))

    def check_directory(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".chalice") or file.endswith('.sil'):
                    path = os.path.abspath(os.path.join(root, file))
                    self._path = path
                    self.check_file(path)

with open('result.csv', 'w') as fp:
    writer = csv.writer(fp)
    TestChecker('chalice2silver', writer).check_directory(
            CHALICE2SILVER_TEST_DIR)
    TestChecker('silver', writer).check_directory(
            SILVER_TEST_DIR)
