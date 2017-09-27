#!/usr/bin/env python
# encoding: utf-8

import csv
import json
import re

class CsvFilterRuleLoader(object):

    """Docstring for CsvFilterRuleLoader. """

    def __init__(self, jsonRules):
        """Load CsvFilterRule from json format

        :json: json format rules

        """
        _rules = json.loads(jsonRules)

        self._rules = list()
        for r in _rules:
            self._rules.append(CsvFilterRule(r))

    def getAll(self):
        """Get all csv filter rules
        :returns: Array of CsvFilterRule

        """
        return self._rules

class CsvFilterRule(object):

    def __init__(self, jsonRule):
        """ Rule of filter

        :jsonRule: json format rule

        """
        self._column = jsonRule['column']
        self._keyword = jsonRule['keyword']

    def column(self):
        """return column name of rule
        :returns: column name

        """
        return self._column

    def keyword(self):
        """return keyword of rule
        :returns: keyword

        """
        return self._keyword


class CsvFilter(object):

    def __init__(self, rules):
        """@todo: to be defined1.

        :rules: @todo

        """
        self._rules = rules

    def filter(self, data):
        """Filter data depends on rules

        :data: csv file data
        :returns: list

        """
        ans = list()
        for d in data:
            for r in self._rules:
                if r.column() in d.keys() and re.search(r.keyword(), d[r.column()]):
                    ans.append(d)
                    break
        return ans


def csvReader(filename):

    reader = csv.DictReader(open(filename))
    data = list()
    for record in reader:
        data.append(record)

    return data

if __name__ == '__main__':
    ruleFilename = 'rules.json'
    rules = None
    with open(ruleFilename, 'rb') as ruleFile:
        rules = CsvFilterRuleLoader(ruleFile.read()).getAll()

    result = list()
    if rules:
        dataFilename = 'product.csv'
        data = csvReader(dataFilename)
        if data:
            result = CsvFilter(rules).filter(data)
    if result:
        outFilename = 'filtered.csv'
        fields = result[0].keys()
        with open(outFilename, 'wb') as outFile:
            writer = csv.DictWriter(outFile, fieldnames=fields)
            writer.writeheader()
            for record in result:
                writer.writerow(record)
