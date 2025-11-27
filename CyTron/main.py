# main.py
import click
import yaml
from core.controller import AivaController

@click.group()
def cli():
    pass

@cli.command()
@click.option('--config', default='config.yaml', help='Config file')
def run(config):
    """Start assistant in interactive loop"""
    with open(config, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    controller = AivaController(cfg)
    controller.start_interactive_loop()

@cli.command()
@click.option('--config', default='config.yaml', help='Config file')
@click.argument('report_type', type=click.Choice(['daily','weekly','summary']))
def report(config, report_type):
    with open(config, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    controller = AivaController(cfg)
    controller.run_report(report_type)

if __name__ == '__main__':
    cli()
