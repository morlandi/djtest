import django
import unittest
import importlib
import inspect
import pkgutil


class AppInspector(object):

    def __init__(self, app):
        self.app = app

    def is_test_class(self, klass):
        try:
            if issubclass(klass, django.test.TestCase):
                return True
        except:
            pass
        try:
            if issubclass(klass, django.test.TransactionTestCase):
                return True
        except:
            pass
        try:
            if issubclass(klass, unittest.TestCase):
                return True
        except:
            pass
        return False

    def enumerate_test_methods(self, filter=''):
        result = []
        filters = [f.strip() for f in filter.split(',')] if filter is not None else ['', ]
        for f in filters:
            result += self.enumerate_test_methods_for_filter(f)
        return result

    def enumerate_test_methods_for_filter(self, filter=''):
        """
        Return the list of optionally filtered) test methods
        available for specified app as follows:

        [
            ...
            {
                'module': 'frontend_api.tests.test_frontend_api',
                'class': 'FrontEndApiTest',
                'method': 'test_unprocessed_transactions_listing',
            },
            {
                'module': 'frontend_api.tests.test_frontend_api',
                'class': 'FrontEndApiTest',
                'method': 'test_withdrawal_ex_listing',
            },
        ]
        """

        # import test module for this app
        test_module = importlib.import_module(self.app + '.tests')

        # list submodules
        submodules = pkgutil.iter_modules(test_module.__path__)
        # example: ['base_case', 'test_count_beans']

        result = []

        # Hack to retrieve submodule names in different environments
        submodules = [s for s in submodules]
        try:
            submodule_names = [s.name for s in submodules]
        except:
            submodule_names = [s[1] for s in submodules]

        for submodule_name in submodule_names:

            # import submodule
            test_submodule = importlib.import_module(self.app + '.tests.' + submodule_name)

            # list test classes
            classes = [k[1] for k in inspect.getmembers(test_submodule, inspect.isclass)]
            test_classes = [k for k in classes if self.is_test_class(k)]

            for test_class in test_classes:

                methods = [f[1] for f in inspect.getmembers(test_class, predicate=inspect.isfunction)]
                test_methods = [m for m in methods if m.__name__.startswith('test_')]

                if len(test_methods):

                    for test_method in test_methods:
                        result.append(
                            '.'.join([
                                test_module.__name__,
                                submodule_name,
                                test_class.__name__,
                                test_method.__name__,
                            ])
                        )

        if filter:
            result = [method for method in result if filter in method]

        return result
