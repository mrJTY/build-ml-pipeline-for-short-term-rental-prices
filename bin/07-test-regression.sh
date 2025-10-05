#!/usr/bin/env bash

set -e

conda run -n components \
  mlflow run . \
  -P steps=test_regression_model \
  --env-manager=local
