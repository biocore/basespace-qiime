#!/usr/bin/env python

import sys
import json
import logging

from glob import glob
from os.path import join

from qcli import qcli_system_call
from skbio.util import create_dir


def system_call(cmd, shell=True):
    """Simple wrapper around qcli_system_call"""
    info = qcli_system_call(cmd)

    if info[2] != 0:
        logging.error('STDOUT: '+info[0])
        logging.error('STDERR: '+info[1])
        return sys.exit(info[2])


def main():

    # load json file
    jsonfile = open('/data/input/AppSession.json')
    app_session = json.load(jsonfile)

    # determine the number of properties
    properties_num = len(app_session['Properties']['Items'])

    # get command attributes, etc
    for index in range(properties_num):
        # set project ID
        if app_session['Properties']['Items'][index]['Name'] == \
                'Input.Projects':
            project_id = \
                    app_session['Properties']['Items'][index]['Items'][0]['Id']


    # from BaseSpace's documentation
    input_dir = '/data/input/samples/'
    base = join('/data/output/appresults/', project_id)
    output_dir = join(base, 'sl-out')

    # for sanity
    create_dir(output_dir)

    # split libraries
    cmd = ("multiple_split_libraries_fastq.py "
           "-i '{input_dir}' -o '{output_dir}'")
    params = {'input_dir': input_dir, 'output_dir': output_dir}

    system_call(cmd.format(**params))
    for log_file in glob(join(output_dir, 'log_*')):
        with open(log_file, 'U') as fd_log:
            print fd_log.read()

    input_dir = join(output_dir, 'seqs.fna')
    output_dir = join(base, 'closed-ref')
    cmd = ("pick_closed_reference_otus.py "
           "-i '{input_seqs}' -o '{output_dir}'")
    params = {'input_seqs': input_dir, 'output_dir': output_dir}

    system_call(cmd.format(**params))
    for log_file in glob(join(output_dir, 'log_*')):
        with open(log_file, 'U') as fd_log:
            print fd_log.read()

if __name__ == '__main__':
    sys.exit(main())
