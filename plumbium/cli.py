import click
from artefacts import Image
import pipelines
from processresult import recorder


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = {'DEBUG': debug}


@cli.command()
@click.argument('t1', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2_lesions', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def fill_and_extract_brain(ctx, t1, t2, t2_lesions):
    recorder.run(
        'fill_and_extract_brain',
        pipelines.fill_and_extract_brain,
        Image(t1),
        Image(t2),
        debug=ctx.obj['DEBUG']
    )


@cli.command()
@click.argument('t1', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2', type=click.Path(exists=True, dir_okay=False))
@click.argument('t2_lesions', type=click.Path(exists=True, dir_okay=False))
@click.argument('mton_short', type=click.Path(exists=True, dir_okay=False))
@click.argument('mtoff_short', type=click.Path(exists=True, dir_okay=False))
@click.argument('mton_long', type=click.Path(exists=True, dir_okay=False))
@click.argument('mtoff_long', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def mtr(ctx, t1, t2, t2_lesions, mton_short, mtoff_short, mton_long, mtoff_long):
    recorder.run(
        'mtr',
        pipelines.mtr,
        Image(t1),
        Image(t2),
        Image(t2_lesions),
        Image(mton_short),
        Image(mtoff_short),
        Image(mton_long),
        Image(mtoff_long),
        debug=ctx.obj['DEBUG']
    )


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def test(ctx, input_file):
    recorder.run(
        'test',
        pipelines.test,
        Image(input_file),
        debug=ctx.obj['DEBUG']
    )


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def fail_test(ctx, input_file):
    recorder.run(
        'test_failure',
        pipelines.fail_test,
        Image(input_file),
        debug=ctx.obj['DEBUG']
    )

if __name__ == '__main__':
    cli()
