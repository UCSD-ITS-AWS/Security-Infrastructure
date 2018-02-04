import click
from .logs import logs
from .sec import sec

cli = click.CommandCollection(sources=[sec, logs])

if __name__ == '__main__':
    cli()