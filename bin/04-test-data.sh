#!/usr/bin/env bash

set -e

export PATH="/opt/miniconda3/envs/components/bin:$PATH"
python main.py main.steps=data_check
