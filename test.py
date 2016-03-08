from plumbium import processresult


@processresult.record_process('f')
def f(x):
    print 'some printed output from f'
    return x + 1


@processresult.record_process('g')
def g(x, y):
    print 'some printed output from g'
    return x + y


with processresult.recorder.begin('test analysis') as pr:
    x = f(10)
    x = g(4, 5)


with processresult.recorder.begin('test analysis 2') as pr:
    x = f(19)
    x = g(12, 5)
