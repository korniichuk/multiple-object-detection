#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: multiple-object-detection

from fabric.api import local

def git():
    """Configure Git"""

    local("git remote rm origin")
    local("git remote add origin https://korniichuk@github.com/korniichuk/multiple-object-detection.git")
