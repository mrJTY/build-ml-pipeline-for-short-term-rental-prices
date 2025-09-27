#!/usr/bin/env bash

set -e

conda run -n components \
  python main.py main.steps=data_check
