#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    #if (len(sys.argv) == 2) and (argv[1] == 'clean'):
    #    find . -type f \( -name '*.pyc' -o -name '*~' \) -delete
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
