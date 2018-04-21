djtest
======

An interactive test runner for Django projects.

Installation
------------

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
                            Filtering: run only test methods matching specified
                            pattern
      -l, --list            List available test methods

    Available apps: tasks, wallet_clients, frontend_api, trading_api, backend


Sample config file
------------------

A sample "skeleton" config file "./.djtest.conf" is authomatically created on first run.

You should edit it to add the list of apps to be tested.

::

  [general]
  project=myproject
  test_settings_module=myproject.settings.test_settings
  test_settings_no_migrations_module=myproject.settings.test_settings_no_migrations
  media_folder="../public/test_media/"
  apps=app1, app2, appN


Credits
-------

- `Tutorial on how to structure Python packages <https://github.com/storborg/python-packaging>`_
