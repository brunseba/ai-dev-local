import click

@click.group()
def cli():
    pass

@cli.command()
def start():
    click.echo("Starting AI Dev Local...")

if __name__ == '__main__':
    cli()
