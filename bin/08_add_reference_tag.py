#!/usr/bin/env python
"""
Add 'reference' tag to the clean_sample.csv artifact in W&B
"""
import wandb

# Initialize a W&B run
run = wandb.init(project='nyc_airbnb', job_type='add_tag')

# Get the latest version of clean_sample.csv
artifact = run.use_artifact('clean_sample.csv:latest')

# Add the 'reference' alias
artifact.aliases.append('reference')
artifact.save()

print(f"Added 'reference' tag to {artifact.name}")

run.finish()
