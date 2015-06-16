#!/usr/bin/env python

from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement
# objects
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(name="mozstumbler_leaderboard",
      version="1.0.0",
      description="A leaderboard to track points for Mozilla Stumbler users",
      author="Garvan Keeley",
      author_email="gkeeley@mozilla.com",
      maintainer="Victor Ng",
      maintainer_email="vng@mozilla.com",
      url="https://github.com/garvankeeley/leaderboard_backend",
      install_requires=reqs,
      packages=["leaderboard"],
      classifiers=["Programming Language :: Python"])
