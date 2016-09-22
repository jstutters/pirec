import os
try:
    import pip
except ImportError:
    pass
import socket


def get_environment():
    env = {}
    try:
        env['python_packages'] = [str(p) for p in pip.get_installed_distributions()]
    except:
        pass
    env['hostname'] = socket.gethostname()
    env['uname'] = os.uname()
    env['environ'] = dict(os.environ)
    return env
