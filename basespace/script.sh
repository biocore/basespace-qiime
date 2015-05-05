#!/bin/bash
# 
# This script is intended to live inside the docker image that you setup
# for usage in basespace
git clone git://github.com/ElDeveloper/bsq.git
python bsq/script.py
