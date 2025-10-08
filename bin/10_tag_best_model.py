#!/usr/bin/env python
"""
Find the best performing model (lowest MAE) and tag it as 'prod'
"""
import wandb
import sys


def main():
    api = wandb.Api()
    runs = api.runs("nyc_airbnb", filters={"jobType": "train_random_forest"})

    if not runs:
        print("No training runs found!", file=sys.stderr)
        sys.exit(1)

    # Find the run with the best (lowest) MAE
    best_run = None
    best_mae = float('inf')

    print("Analyzing runs:")

    for run in runs:
        mae = run.summary.get('mae')
        if mae is not None:
            print(f"Run: {run.name} | MAE: {mae:.4f}")
            if mae < best_mae:
                best_mae = mae
                best_run = run

    if best_run is None:
        print("No runs with MAE found!", file=sys.stderr)
        sys.exit(1)

    print(f"Best run: {best_run.name}")
    print(f"Best MAE: {best_mae:.4f}")
    print(f"Run ID: {best_run.id}")

    # Find the model artifact from the best run
    print("Fetching model artifact from best run...")

    artifacts = best_run.logged_artifacts()
    model_artifact = None

    for artifact in artifacts:
        if artifact.type == 'model_export':
            model_artifact = artifact
            break

    if model_artifact is None:
        print("No model export artifact found in best run!", file=sys.stderr)
        sys.exit(1)

    print(f"Found model artifact: {model_artifact.name}")

    # Tag it as 'prod'
    print("Tagging model as 'prod'...")

    # Check if 'prod' alias already exists
    if 'prod' in model_artifact.aliases:
        print(f"Model already has 'prod' tag!")
    else:
        model_artifact.aliases.append('prod')
        model_artifact.save()
        print(f"Successfully tagged {model_artifact.name} as 'prod'!")

    print("Best model tagged with 'prod' label!")


if __name__ == "__main__":
    main()
