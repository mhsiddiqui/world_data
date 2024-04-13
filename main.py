from pathlib import Path

import click

BASE_DIR = Path(__file__).resolve(strict=True)
CLEAN_DATA = str(BASE_DIR / "cleaned")
DIRTY_DATA = str(BASE_DIR / "dirty")


@click.group()
def cli():
    pass


@cli.command()
@click.option('--country', required=True, help='Country code')
@click.option(
    '--data', required=True,
    type=click.Choice(['country', 'state', 'city', 'places']),
    help='Data points'
)
@click.option(
    '--save', required=True, is_flag=True, default=False, help='Save if verified'
)
def verify(country, data):
    click.echo('Initialized the database')


if __name__ == '__main__':
    cli()
