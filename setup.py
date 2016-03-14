from setuptools import setup

setup(
    name='plumbium',
    version='0.0.5',
    packages=['plumbium'],
    zip_safe=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        plumbium=plumbium.cli:cli
    ''',
    author='Jon Stutters',
    author_email='j.stutters@ucl.ac.uk',
    description='MRI image analysis tools',
    url='https://github.com/jstutters/plumbium',
    license='MIT',
    classifiers=[
    ]
)
