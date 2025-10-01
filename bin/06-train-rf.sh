#!/usr/bin/env bash

set -e

conda run -n components \
  mlflow run . \
  -P steps=train_random_forest \
  --env-manager=local
