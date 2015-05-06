import os
import fnmatch
import sys
import json
import logging

from qcli import qcli_system_call
from skbio.util import create_dir
from os.path import join


def main():

    # load json file
    jsonfile = open('/data/input/AppSession.json')
    jsonObject = json.load(jsonfile)

    # determine the number of properties
    numberOfPropertyItems = len(jsonObject['Properties']['Items'])

    # loop over properties
    sampleID = []
    sampleHref = []
    sampleName = []
    sampleDir = []

    for index in range(numberOfPropertyItems):
        # set project ID
        if jsonObject['Properties']['Items'][index]['Name'] == 'Input.Projects':
            projectID = jsonObject['Properties']['Items'][index]['Items'][0]['Id']

    for index in range(numberOfPropertyItems):
        # set sample parameters
        if jsonObject['Properties']['Items'][index]['Name'] == 'Input.Samples':
            for sample in range(len(jsonObject['Properties']['Items'][index]['Items'])):
                sampleID.append(jsonObject['Properties']['Items'][index]['Items'][sample]['Id'])
                sampleHref.append(jsonObject['Properties']['Items'][index]['Items'][sample]['Href'])
                sampleName.append(jsonObject['Properties']['Items'][index]['Items'][sample]['Name'])
                sampleDir = '/data/input/samples/%s/Data/Intensities/BaseCalls' %(sampleID[sample])

                logging.error('The sampleDir name is %s', sampleDir)
                logging.error('The directory exists? %s', os.path.exists(sampleDir))

                if not os.path.exists(sampleDir):
                    sampleDir = '/data/input/samples/%s' %(sampleID[sample])

                logging.error('The sampleDir name is %s', sampleDir)
                logging.error('The directory exists? %s', os.path.exists(sampleDir))

                fwd_reads = []
                rev_reads = []

                for root, dirs, files in os.walk(sampleDir):
                    matches = fnmatch.filter(files, '*_R1_*')
                    fwd_reads += [join(root, match) for match in matches]
                    matches = fnmatch.filter(files, '*_R2_*')
                    rev_reads += [join(root, match) for match in matches]

                logging.error('R1files: %s', fwd_reads)
                logging.error('R2files: %s', rev_reads)

                sampleOutDir = '/data/output/appresults/%s/%s' % (projectID,
                                                                  sampleName[sample])
                create_dir(sampleOutDir)

                fn = '%s/seqs-summary.txt' % (sampleOutDir)

                # unzip all the sequences so count_seqs.py can read the data
                for f in fwd_reads + rev_reads:
                    cmd = 'gunzip %s' % f
                    logging.error(cmd)
                    rets = qcli_system_call(cmd)
                    logging.error(rets)

                cmd = "count_seqs.py -i %s" % (','.join(fwd_reads+rev_reads))
                cmd = cmd.replace('.gz', '')
                logging.error(cmd)

                out, err, ret = qcli_system_call(cmd)
                logging.error(out)
                logging.error(err)
                logging.error('return code is: %s', ret)

                logging.error('writting file to %s', fn)
                with open(fn, 'wa') as fd:
                    fd.write(out)


if __name__ == '__main__':
    sys.exit(main())
