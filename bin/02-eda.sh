#!/usr/bin/env bash

set -e

conda run -n components \
  mlflow run src/eda
