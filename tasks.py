from invoke import task
from d2py.tools.write import site


@task
def init(ctx):
    ctx.run("pip install .[doc]")
    ctx.run("pip install --upgrade nbconvert")


namespace = site("docs", target="docs/_build")
namespace.add_task(init)
