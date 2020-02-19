djtest
======

An interactive test runner for Django projects.

Purposes:

- keep the list of apps available for test in a local configuration file
- display the list of all available unit tests (-l option)
- run unit tests for apps specified on command line
- cleanup a test "media folder" before each execution
- optionally filter the list of unit tests to be executed (-f option)

Installation
------------

::

    pip install djtest

or:

::

    pip install git+https://github.com/morlandi/djtest


Sample usage
------------

::

    Using config file "./.djtest.conf"
    usage: djtest [-h] [-v {0,1,2,3}] [-m] [-n] [-f FILTER] [-l] [apps [apps ...]]

    Targets may specify either: 'all' for all available apps, and app name (one or
    more), or a specific test module/method

    positional arguments:
      apps

    optional arguments:
      -h, --help            show this help message and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level. (default: 2)
      -m, --no-migrations   Skip migrations. (default: False)
      -n, --dry-run         Don't execute commands, just pretend. (default: False)
      -f FILTER, --filter FILTER
                            Filtering: run only test methods matching specified pattern
                            (multiple patterns separated by ',')
      -l, --list            List available test methods
      --version             show program's version number and exit

    Available apps: tasks, wallet_clients, frontend_api, trading_api, backend


Sample config file
------------------

A sample "skeleton" config file "./.djtest.conf" is automatically created on first run.

You should edit it to specify the list of testable apps.

::

  [general]
  project=myproject
  test_settings_module=myproject.settings.test_settings
  test_settings_no_migrations_module=myproject.settings.test_settings_no_migrations
  media_folder="../public/test_media/"
  apps=app1, app2, appN


Sample "test settings" module
-----------------------------

::

    from myproject.settings.settings import *

    LANGUAGE_CODE = 'en'
    TIME_ZONE = 'UTC'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    ...

Sample "test settings - no migrations" module
---------------------------------------------

::

    from myproject.settings.test_settings import *

    class DisableMigrations(object):

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            #return "notmigrations"
            return None


    MIGRATION_MODULES = DisableMigrations()
