# -*- coding: utf-8 -*-

from __future__ import division, print_function

import pdb
import re
import sys
import titlecase


class Entry(object):
    def __init__(self, input, parse_type='ACM'):
        self.entry_type = ''
        self.required_fields, self.optional_fields = [], []
        self.data = {}
        self.first_author = ''
        self.indent = '  '
        lines = input.splitlines()[1:-1]
        for line in lines:
            field_type, field_value = line.split('=')
            if parse_type.lower() == 'acm':
                self.parse_acm(field_type.strip().strip('{}'),
                               field_value.strip().strip('{},'))
            else:
                print('parse type not implemented yet')

    def parse_acm(self, field_type, field_value):
        parsed = ''
        if field_type in ('booktitle', 'journal', 'title'):
            parsed = titlecase.titlecase(field_value)
        elif field_type in (
            'pages', 'number', 'organization', 'publisher', 'volume', 'year',
        ):
            parsed = field_value
        elif field_type == 'author':
            authors = field_value.split(' and ')
            parsed = []
            for aidx, author in enumerate(authors):
                author = author.split(',')
                parsed.append(author[1].strip() + ' ' + author[0].strip())
                if aidx == 0:
                    self.first_author = author[0].strip()
            parsed = ' and '.join(parsed)
        else:
            print('field type', field_type, 'not yet supported')
        if parsed:
            self.data[field_type] = parsed

    def print(self):
        output = '@' + self.entry_type + '{' + self.first_author.lower() +\
            self.data['year'] + \
            re.split(r'[ -]', self.data['title'])[0].lower() + ',\n'
        for f in self.required_fields:
            try:
                output += self.indent + f + ' = "' + self.data[f] + '",\n'
            except KeyError:
                print('ERROR: required field', f, 'for entry type',
                      self.entry_type, 'missing')
        for f in self.optional_fields:
            try:
                output += self.indent + f + ' = "' + self.data[f] + '",\n'
            except KeyError:
                pass
        output = output[:-2] + '\n}\n'
        print(output)


class Article(Entry):
    def __init__(self, input):
        Entry.__init__(self, input)
        self.entry_type = 'article'
        self.required_fields = ['author', 'title', 'journal', 'year']
        self.optional_fields = ['volume', 'number', 'pages',
                                'month', 'note', 'key']


class InProceedings(Entry):
    def __init__(self, input):
        Entry.__init__(self, input)
        self.entry_type = 'inproceedings'
        self.required_fields = ['author', 'title', 'booktitle', 'year']
        self.optional_fields = ['editor', 'pages', 'organization', 'publisher',
                                'address', 'month', 'note', 'key']


def parse(input='input.txt'):
    with open('input.txt') as infile:
        data = infile.read()
    entry_type = data.split('{')[0].lower()
    if entry_type == '@article':
        e = Article(data)
    elif entry_type == '@inproceedings':
        e = InProceedings(data)
    else:
        print('entry type', entry_type, 'not yet supported')
        sys.exit()
    e.print()

if __name__ == '__main__':
    parse()
