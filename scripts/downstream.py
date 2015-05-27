#!/usr/bin/env python

import sys
import json
import logging

from glob import glob
from os.path import join

from qcli import qcli_system_call
from biom import load_table
from skbio.util import create_dir


def system_call(cmd, shell=True):
    """Simple wrapper around qcli_system_call"""
    info = qcli_system_call(cmd)

    if info[2] != 0:
        logging.error('STDOUT: '+info[0])
        logging.error('STDERR: '+info[1])
        return sys.exit(info[2])


def main():

    spreadsheet_key = None

    with open('/data/input/AppSession.json', 'U') as fd_json:
        app = json.load(fd_json)

    # get command attributes, etc
    for item in app['Properties']['Items']:
        if item['Name'] == 'Input.Projects':
            project_id = item['Items'][0]['Id']
        if item['Name'] == 'Input.spreadsheet-key':
            spreadsheet_key = item['Content']
        if item['Name'] == 'Input.app-result-id':
            results_id = item['Content']['Id']
        if item['Name'] == 'Input.rarefaction-depth':
            depth = item['Content']


    # from BaseSpace's documentation
    input_dir = '/data/input/appresults/'
    base = join('/data/output/appresults/', project_id)

    create_dir(base)

    # OTU picking
    input_dir = join(input_dir, results_id)

    mapping_fp = join(base, 'mapping-file.txt')
    cmd = ("load_remote_mapping_file.py "
           "-k {spreadsheet_key} -o {mapping_fp}")
    params = {'spreadsheet_key': spreadsheet_key, 'mapping_fp': mapping_fp}

    system_call(cmd.format(**params))

    biom_fp = join(input_dir, 'otu_table.biom')
    tree_fp = glob(join(input_dir, '*.tree'))[0]
    output_dir = join(base, 'corediv-out')

    bt = load_table(biom_fp)

    if bt.is_empty():
        logging.error('BIOM table is empty, cannot perform diversity '
                      'analyses.')
        return 11

    params_fp = join(base, 'alpha-params.txt')
    with open(params_fp, 'w') as alpha_fp:
        alpha_fp.write('alpha_diversity:metrics shannon,PD_whole_tree,'
                       'chao1,observed_species')

    cmd = ("core_diversity_analyses.py "
           "-i {biom_fp} -o {output_dir} -m {mapping_fp} -e {depth} "
           "-t {tree_fp} -a -O {jobs} -p {params_fp}")
    params = {'biom_fp': biom_fp, 'output_dir': output_dir,
              'mapping_fp': mapping_fp, 'depth': depth, 'jobs': '4',
              'tree_fp': tree_fp, 'params_fp': params_fp}
    system_call(cmd.format(**params))

    for log_file in glob(join(output_dir, 'log_*')):
        with open(log_file, 'U') as fd_log:
            print fd_log.read()

    return 0


if __name__ == '__main__':
    sys.exit(main())
