#!/usr/bin/env bash

set -e

mlflow run . \
  -P steps="data_check"