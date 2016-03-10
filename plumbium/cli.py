import click
from artefacts import Image
import pipelines
from processresult import recorder


@click.group()
def cli():
    pass


@cli.command()
@click.argument('t1', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2_lesions', type=click.Path(exists=True, dir_okay=False))
def fill_and_extract_brain(t1, t2, t2_lesions):
    recorder.run(
        'fill_and_extract_brain',
        pipelines.fill_and_extract_brain,
        Image(t1),
        Image(t2)
    )


@cli.command()
@click.argument('t1', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2_lesions', type=click.Path(exists=True, dir_okay=False))
@click.argument('mton_short', type=click.Path(exists=True, dir_okay=False))
@click.argument('mtoff_short', type=click.Path(exists=True, dir_okay=False))
@click.argument('mton_long', type=click.Path(exists=True, dir_okay=False))
@click.argument('mtoff_long', type=click.Path(exists=True, dir_okay=False))
def mtr(t1, t2, t2_lesions, mton_short, mtoff_short, mton_long, mtoff_long):
    recorder.run(
        'mtr',
        pipelines.mtr,
        Image(t1),
        Image(t2),
        Image(t2_lesions),
        Image(mton_short),
        Image(mtoff_short),
        Image(mton_long),
        Image(mtoff_long)
    )


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
def test(input_file):
    recorder.run(
        'test',
        pipelines.test,
        Image(input_file)
    )


if __name__ == '__main__':
    cli()
