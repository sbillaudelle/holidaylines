import os
import json
import re
import sys
import imp

def _scan(path):

    path = os.path.abspath(path)
    files = os.listdir(path)
    res = []

    for file in files:
        if os.path.isdir(os.path.join(path, file)):
            res.extend(_scan(os.path.join(path, file)))
        else:
            if file == 'plugin.json':
                res.append(os.path.join(path, file))

    return res


def scan(path):

    res = _scan(path)
    return res


def find_plugin(id):
    
    plugins = scan('/home/stein/Labs/Web/CMS/umbrella/cms/plugins')
    for i in plugins:
        p = json.load(open(i))
        if p['id'] == id:
            return os.path.dirname(i)


def install_model(model):
    from django.core.management import color
    from django.db import connection, transaction

    cursor = connection.cursor()

    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)

    sql, references = connection.creation.sql_create_model(model, color.no_style(), seen_models)

    for statement in sql:
        cursor.execute(statement)

    index_sql = connection.creation.sql_indexes_for_model(model, color.no_style())

    for statement in index_sql:
        cursor.execute(statement)


class Plugin:

    def __init__(self, id):

        self.id = id
        self.path = find_plugin(self.id)
        self.templates = json.load(open(os.path.join(self.path, 'templates.json')))

        self.plugin = self.import_plugin()


    def import_plugin(self):

        plugin_file = os.path.join(self.path, '__init__.py')
        if os.path.isfile(plugin_file):
            sys.path.insert(0, os.path.join(self.path, '..'))
            return imp.load_module(
                'cms.plugins.{0}'.format(self.id),
                open(plugin_file),
                plugin_file,
                ('.py', 'r', imp.PY_SOURCE)
            )


    def handle_request(self, path, request):

        self.plugin.HANDLERS[path](request)


    def process(self, data):

        def replace(m):
            t = m.group('template')
            return self.plugin.process(self.templates[t])

        return re.sub('\%\s*{id}.(?P<template>\w*)\s*\%'.format(id=self.id), replace, data)
