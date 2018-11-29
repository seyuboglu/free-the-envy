"""
"""
import json
import os

import click

from split import SplitCli
from noisy import NoisySimulation


def get_process(process_name):
    """
    """
    process_name = ''.join(x.capitalize() or '_' for x in process_name.split('_'))
    assert(process_name in globals())
    return globals()[process_name]
    


@click.command()
@click.option(
    "--process",
    type=str,
    default="Split"
)
@click.option(
    "--dir",
    type=str,
    default="experiments/split/first_split"
)
def main(process, dir):
    print("Spliddit Analysis")
    print("-----------------")

    split = get_process(process)(dir)
    split.run()

if __name__ == "__main__":
    main()