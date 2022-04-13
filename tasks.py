from invoke import task
from d2py.tools.write import site


@task
def init(ctx):
    ctx.run("pip install .[doc]")
    ctx.run("pip install --upgrade nbconvert xarray")


namespace = site("docs", target="output/html")
namespace.add_task(init)
