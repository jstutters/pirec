import click
import pipelines
from pipelinerun import PipelineRun


@click.group()
def cli():
    pass


@cli.command()
@click.argument('t1', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2_lesions', type=click.Path(exists=True, dir_okay=False))
def fill_and_extract_brain(t1, t2, t2_lesions):
    fill_and_extract_run = PipelineRun(
        pipelines.mtr,
        Image(t1),
        Image(t2),
        Image(t2_lesions)
    )
    fill_and_extract_run.run()


@cli.command()
@click.argument('t1', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2_lesions', type=click.Path(exists=True, dir_okay=False))
@click.argument('mton_short', type=click.Path(exists=True, dir_okay=False))
@click.argument('mtoff_short', type=click.Path(exists=True, dir_okay=False))
@click.argument('mton_long', type=click.Path(exists=True, dir_okay=False))
@click.argument('mtoff_long', type=click.Path(exists=True, dir_okay=False))
def mtr(t1, t2, t2_lesions, mton_short, mtoff_short, mton_long, mtoff_long):
    mtr_run = PipelineRun(
        pipelines.mtr,
        Image(t1),
        Image(t2),
        Image(t2_lesions),
        Image(mton_short),
        Image(mtoff_short),
        Image(mton_long),
        Image(mtoff_long)
    )
    mtr_run.run()


if __name__ == '__main__':
    cli()
