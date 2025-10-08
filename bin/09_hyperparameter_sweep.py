#!/usr/bin/env python
"""
Hyperparameter sweep script using Hydra multirun
Reads configurations from sweep_configs.csv and builds a single Hydra multirun command
"""
import pandas as pd
import subprocess
import sys
from pathlib import Path
from collections import defaultdict


def main():
    script_dir = Path(__file__).parent
    config_file = script_dir / "sweep_configs.csv"

    print("Starting hyperparameter sweep with Hydra multirun...")
    print(f"Reading configurations from: {config_file}")

    if not config_file.exists():
        print(f"Error: Configuration file not found: {config_file}", file=sys.stderr)
        sys.exit(1)

    try:
        configs_df = pd.read_csv(config_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate required columns
    required_cols = ['n_estimators', 'max_depth', 'min_samples_split',
                     'min_samples_leaf', 'max_features', 'max_tfidf_features']
    missing_cols = set(required_cols) - set(configs_df.columns)
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}", file=sys.stderr)
        sys.exit(1)

    # Extract unique values for each parameter
    param_values = defaultdict(set)
    for col in required_cols:
        for val in configs_df[col]:
            param_values[col].add(val)

    # Build Hydra multirun string
    hydra_params = []
    hydra_params.append(f"modeling.random_forest.n_estimators={','.join(map(str, sorted([int(x) for x in param_values['n_estimators']])))}")
    hydra_params.append(f"modeling.random_forest.max_depth={','.join(map(str, sorted([int(x) for x in param_values['max_depth']])))}")
    hydra_params.append(f"modeling.random_forest.min_samples_split={','.join(map(str, sorted([int(x) for x in param_values['min_samples_split']])))}")
    hydra_params.append(f"modeling.random_forest.min_samples_leaf={','.join(map(str, sorted([int(x) for x in param_values['min_samples_leaf']])))}")
    hydra_params.append(f"modeling.random_forest.max_features={','.join(map(str, sorted(param_values['max_features'])))}")
    hydra_params.append(f"modeling.max_tfidf_features={','.join(map(str, sorted([int(x) for x in param_values['max_tfidf_features']])))}")

    hydra_opts = " ".join(hydra_params) + " -m"

    print("Hydra multirun parameters:")
    print(hydra_opts)
    print("Running sweep...")

    # Run mlflow with Hydra multirun
    cmd = ["mlflow", "run", ".", "--env-manager=local", "-P", f"hydra_options={hydra_opts}"]

    try:
        subprocess.run(cmd, check=True)
        print("Hyperparameter sweep complete!")
        print("Check W&B for results: https://wandb.ai/<your-username>/nyc_airbnb")
    except subprocess.CalledProcessError as e:
        print(f"Error during sweep: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
