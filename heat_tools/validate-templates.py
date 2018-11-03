#!/usr/bin/env python

import os
import re
import subprocess
import sys


EXCLUDED_DIRS = ('contrib', 'elements', 'invalid')


def main(args):
    if len(args) != 1:
        raise SystemExit("Takes one argument, the path to the templates")

    path = args[0]
    got_error = False
    for root, dirs, files in os.walk(path):
        for excluded in EXCLUDED_DIRS:
            if excluded in dirs:
                dirs.remove(excluded)
        for name in files:
            if name.endswith((".yaml", ".template")):
                got_error = validate(root, name) or got_error
    sys.exit(int(got_error))


def validate(base, name):
    basename, ext = os.path.splitext(name)
    if basename.endswith("_env"):
        return False
    args = ["heat",
            "template-validate",
            "-f",
            os.path.join(base, name),
            "--ignore-errors",
            '99001']
    base_env = "%s_env%s" % (basename, ext)
    env = os.path.join(base, base_env)
    if os.path.exists(env):
        args.extend(["-e", env])
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print "Got error validating %s/%s , %s" % (base, name, e.output)
        return True
    else:
        return False


if __name__ == '__main__':
    main(sys.argv[1:])
