"""
"""
import json
import os

import click

from split import Split
from methods.fairness import FairnessMethod

@click.command()
@click.option(
    "--dir",
    type=str,
    default="experiments/first_experiment"
)
def main(dir):
    print("Spliddit Analysis")
    print("-----------------")

    with open(os.path.join(dir, "params.json")) as f:
        params = json.load(f)
    split = Split(params)
    split.solve(method_class=FairnessMethod)
    split.output_results()


if __name__ == "__main__":
    main()