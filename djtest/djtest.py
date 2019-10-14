#!/usr/bin/env python
from __future__ import print_function
"""
(c) 2015-2018 Mario Orlandi, Brainstorm S.n.c.
"""
import sys
import os
import argparse
import django
import pprint
import platform

try:
    import configparser
except:
    from six.moves import configparser
    from six.moves import input

from djtest.app_inspector import AppInspector


def get_version():
    try:
        import djtest
        version = djtest.__version__
        version += " (python: %s)" % platform.python_version()
        return version
    except:
        return '???'


def run_command(command, dry_run):
    if dry_run:
        print("\x1b[1;37;40m# " + command + "\x1b[0m")
    else:
        print("\x1b[1;37;40m" + command + "\x1b[0m")
        rc = os.system(command)
        if rc != 0:
            raise Exception(command)


def read_config_file():
    """
    Parse the config file if exists;
    otherwise, create a default config file and exit
    """

    def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

    def create_default_config_file(config_filename):

        default_config = """
[general]
project={project}
test_settings_module={project}.settings.test_settings
test_settings_no_migrations_module={project}.settings.test_settings_no_migrations
media_folder="../public/test_media/"
apps=app1, app2
"""

        cwd = os.getcwd()
        project = os.path.split(cwd)[-1]
        text = default_config.format(
            project=project,
        )
        with open(config_filename, 'w') as configfile:
            configfile.write(text)

    config_filename = './.%s%sconf' % (os.path.splitext(os.path.basename(__file__))[0], os.path.extsep)
    config = configparser.ConfigParser()
    success = len(config.read(config_filename)) > 0
    if success:
        print('Using config file "%s"' % config_filename)
    else:
        # if not found, create a default config file and exit
        if query_yes_no('Create default config file "%s" ?' % config_filename):
            create_default_config_file(config_filename)
            print('Default config file "%s" has been created; please check it before running this script again' % config_filename)
        exit(-1)

    return config


def main():

    # Make sure cwd is in path
    sys.path.insert(0, os.getcwd())

    # Read config file
    config = read_config_file()
    project = config.get('general', 'project').strip()
    media_folder = config.get('general', 'media_folder').strip()
    available_apps = config.get('general', 'apps').replace(',', ' ').split()
    test_settings_module = config.get('general', 'test_settings_module')
    test_settings_no_migrations_module = config.get('general', 'test_settings_no_migrations_module')

    # Parse command line
    parser = argparse.ArgumentParser()
    parser.description = "Targets may specify either: 'all' for all available apps, and app name (one or more), or a specific test module/method"
    parser.epilog = 'Available apps: ' + ', '.join(available_apps)
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2, 3], default=2, help="Verbosity level. (default: 2)")
    parser.add_argument('-m', '--no-migrations', action='store_true', default=False, help="Skip migrations. (default: False)")
    parser.add_argument('-n', '--dry-run', action='store_true', default=False, help="Don't execute commands, just pretend. (default: False)")
    parser.add_argument('-f', '--filter', help="Filtering: run only test methods matching specified pattern")
    parser.add_argument('-l', '--list', action='store_true', default=False, help="List available test methods")
    parser.add_argument('-d', '--deprecations', action='store_true', default=False, help="Show deprecation warnings")
    parser.add_argument('apps', nargs='*')
    parser.add_argument('--version', action='version', version='%(prog)s ' + get_version())
    parsed = parser.parse_args()
    #print('Result:',  vars(parsed))

    # Adjust test_runner command according to given options
    test_runner = "python %s manage.py test --traceback --verbosity=%d --settings=" % (
        '-Wd' if parsed.deprecations else '',
        parsed.verbosity,
    )
    if parsed.no_migrations:
        test_runner += test_settings_no_migrations_module
    else:
        test_runner += test_settings_module

    # Count targets
    if len(parsed.apps) <= 0:
        parser.print_help()
        return -1

    # Load app list from "apps" option
    apps = []
    for app in parsed.apps:
        if app == "all":
            apps += available_apps
        #elif app in available_apps or '.' in app:
        elif app in available_apps:
            apps.append(app)
        else:
            raise Exception('Unknown app "%s"' % app)

    # Remove duplicates
    apps = list(set(apps))

    available_methods = []
    if parsed.list or parsed.filter:
        os.environ['DJANGO_SETTINGS_MODULE'] = test_settings_no_migrations_module
        django.setup()
        for app in apps:
            app_inspector = AppInspector(app)
            available_methods += app_inspector.enumerate_test_methods(parsed.filter)

    if parsed.list:
        print('Available methods:')
        pprint.pprint(available_methods)
        exit(0)

    if parsed.filter:
        test_labels = ' '.join(available_methods)
    else:
        test_labels = ' '.join(apps)

    # Run tests
    run_command("rm -fr " + media_folder, parsed.dry_run)
    run_command("mkdir " + media_folder, parsed.dry_run)
    run_command(test_runner + ' ' + test_labels, parsed.dry_run)


if __name__ == "__main__":
    main()

