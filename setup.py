import os
import setuptools
import subprocess


def parse_requirements():
    """Parse requirements.txt."""
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, 'requirements.txt')) as f:
        lines = f.readlines()
    lines = [
        l
        for l in map(lambda l: l.strip(), lines)
        if l != '' and l[0] != '#'
    ]
    return lines

requirements = parse_requirements()

setuptools.setup(
    name='cpilot-health-reporter',
    version='0.2.4',
    packages=setuptools.find_packages(),
    description="Health Reporter for CognitivePilot",
    url=(
        "https://gitlab.cognitivepilot.com/ar13/health_reporter/"
    ),
    author="Igor Dranitskiy",
    author_email="i.dranitskiy@cognitivepilot.com",
    license="MIT",
    install_requires=requirements,
)
