#!/usr/bin/env bash

set -e

conda run -n components \
  mlflow run . \
  -P steps=data_check \
  --env-manager=local
