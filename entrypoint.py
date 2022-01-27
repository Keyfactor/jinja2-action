#!/usr/bin/env python3

import os
from jinja2 import Template, StrictUndefined, Environment, FileSystemLoader
from j2cli.context import read_context_data

def guess_format(file_name):
    _, extension = os.path.splitext(file_name)
    print(extension)
    formats = {
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.ini': 'ini',
        '.env': 'env',
    }
    return formats.get(extension, 'env')

variables = {'env': os.environ}
for variable in os.environ.get('INPUT_VARIABLES', '').split('\n'):
    clean_variable = bytes(variable.strip(), 'utf-8').decode('unicode_escape')
    if clean_variable != '':
        name, value = clean_variable.split('=', 1)
        variables.update({name: value})

data_files = os.environ.get('INPUT_DATA_FILE')
for data_file in data_files.split('\n'):
    clean_filename = bytes(data_file.strip(), 'utf-8').decode('unicode_escape')
    if clean_filename != '':
        format = os.environ.get('INPUT_DATA_FORMAT', guess_format(clean_filename))
        with open(clean_filename, 'r') as file:
            variables.update(read_context_data(format, file, None))

with open(os.environ['INPUT_TEMPLATE'], 'r') as file:
    template_kwargs = {}
    if os.environ.get('INPUT_STRICT') == 'true':
        template_kwargs.update({'undefined': StrictUndefined})
    template = Environment(loader=FileSystemLoader('.')).from_string(str(file.read()), **template_kwargs)

with open(os.environ['INPUT_OUTPUT_FILE'], 'w') as file:
    file.write(template.render(**variables) + '\n')
