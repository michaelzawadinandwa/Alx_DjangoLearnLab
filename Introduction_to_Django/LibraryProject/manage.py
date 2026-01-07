#!/usr/bin/env python
"""Local manage.py wrapper for LibraryProject checks.

This file mirrors the top-level manage.py so tools that expect a
manage.py inside the `LibraryProject` directory can find one.
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
