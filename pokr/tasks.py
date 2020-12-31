import invoke


@invoke.task
def livereload(c):
    c.run('QUART_APP=scorecard:app quart run')
