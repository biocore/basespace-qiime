#!/usr/bin/env python

import sys
import json
import logging

from glob import glob
from os.path import join

from qcli import qcli_system_call
from biom import load_table
from skbio.util import create_dir
from qiime.util import guess_even_sampling_depth


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

    # OTU picking
    input_dir = join(output_dir, 'seqs.fna')
    output_dir = join(base, 'closed-ref')
    cmd = ("pick_closed_reference_otus.py "
           "-i '{input_seqs}' -o '{output_dir}'")
    params = {'input_seqs': input_dir, 'output_dir': output_dir}

    system_call(cmd.format(**params))
    for log_file in glob(join(output_dir, 'log_*')):
        with open(log_file, 'U') as fd_log:
            print fd_log.read()

    if spreadsheet_key:
        mapping_fp = join(base, 'mapping-file.txt')
        cmd = ("load_remote_mapping_file.py "
               "-k {spreadsheet_key} -o {mapping_fp}")
        params = {'spreadsheet_key': spreadsheet_key, 'mapping_fp': mapping_fp}

        system_call(cmd.format(**params))

        biom_fp = join(output_dir, 'otu_table.biom')
        tree_fp = glob(join(output_dir, '*.tree'))[0]
        output_dir = join(base, 'corediv-out')

        bt = load_table(biom_fp)

        if bt.is_empty():
            logging.error('BIOM table is empty, cannot perform diversity '
                          'analyses.')
            return 11

        # cast as int or core diversity will reject the value
        depth = int(guess_even_sampling_depth(bt.nonzero_counts('sample')))
        cmd = ("core_diversity_analyses.py "
               "-i {biom_fp} -o {output_dir} -m {mapping_fp} -e {depth} "
               "-t {tree_fp} -a -O {jobs}")
        params = {'biom_fp': biom_fp, 'output_dir': output_dir,
                'mapping_fp': mapping_fp, 'depth': depth, 'jobs': '30',
                'tree_fp': tree_fp}
        system_call(cmd.format(**params))

        for log_file in glob(join(output_dir, 'log_*')):
            with open(log_file, 'U') as fd_log:
                print fd_log.read()

    return 0


if __name__ == '__main__':
    sys.exit(main())
