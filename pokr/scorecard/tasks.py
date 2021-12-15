from invoke import task


@task
def livereload(c):
    c.run("QUART_APP=scorecard:app quart run")
