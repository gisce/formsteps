from setuptools import setup, find_packages


setup(
    name='formsteps',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/gisce/formsteps',
    install_requires=[
        'marshmallow-jsonschema'
    ],
    license='MIT',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    description='Simple Step Forms Library'
)