djtest
======

An interactive test runner for Django projects.

Installation
------------

::

    pip install https://github.com/morlandi/djtest


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

