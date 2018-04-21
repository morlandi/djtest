#!/usr/bin/env python

"""
(c) 2015-2018 Mario Orlandi, Brainstorm S.n.c.
"""

__author__    = "Mario Orlandi"
__version__   = "1.4.1"
__copyright__ = "Copyright (c) 2015-2018, Brainstorm S.n.c."
__license__   = "GPL"

test_settings_modulename = "{project}.settings.test_settings"
test_no_migrations_modulename = "{project}.settings.test_settings_no_migrations"






def enumerate_test_methods(test_module_name, filter=None):
    """
    List all test methods in specified module;
    Sample result:
        ['myapp.tests.MyTestCase.test_func1',
         'myapp.tests.MyTestCase.test_func2',
         ...
        ]
    """

    def list_submodule_names(module):
        # Python 3:
        return [submodule.name for submodule in pkgutil.iter_modules(module.__path__)]
        # Python 2:
        return list_subitems(module, 'module')

    def list_classes(module):
        # Python 3
        return [item[1] for item in inspect.getmembers(test_submodule, inspect.isclass)]
        # Python 2:
        return list_subitems(module, 'type')

    def list_methods(klass):
        """
        Return a list of items as follows:
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

        # Python 3:
        members = inspect.getmembers(klass, predicate=inspect.isfunction)
        return [{
            'module': item[1].__module__,
            'class': klass.__name__,
            'method': item[1].__name__,
        } for item in members]
        # Python 2:
        return list_subitems(klass, 'instancemethod')

    def list_subitems(module_or_class, subitem_type_name):
        """
        Examples:
            my_module = importlib.import_module('my_module')
            submodule_names = list_subtimes(my_module, 'module')
        or:
            method_names = list_subtimes(MyClass, 'instancemethod')
        """
        # pprint.pprint([(name, type(getattr(module_or_class,name)).__name__) for name in module_or_class.__dict__])
        return [name for name in module_or_class.__dict__ if type(getattr(module_or_class, name)).__name__==subitem_type_name]

    test_method_names = []
    test_module = importlib.import_module(test_module_name + '.tests')
    #test_submodules_names = list_subitems(test_module, 'module')
    test_submodules_names = list_submodule_names(test_module)
    for name in test_submodules_names:
        test_submodule = importlib.import_module(test_module_name + '.tests.' + name)
        #klasses = [getattr(test_submodule, name) for name in list_subitems(test_submodule, 'type')]
        klasses = list_classes(test_submodule)
        test_classes = [obj for obj in klasses if issubclass(obj, django.test.TestCase) or issubclass(obj, django.test.TransactionTestCase)]
        for test_class in test_classes:
            #test_methods = [name for name in list_subitems(test_class, 'instancemethod') if name.startswith('test_')]
            test_methods = [item for item in list_methods(test_class) if item['method'].startswith('test_')]
            for test_method in test_methods:
                # test_method_names.append(('%s.tests.%s.%s' % (
                #     test_module_name,
                #     test_class.__name__,
                #     test_method
                # )))
                test_method_names.append(
                    '.'.join([test_method['module'], test_method['class'], test_method['method']])
                )

    if filter:
        test_method_names = [method for method in test_method_names if filter in method]

    return test_method_names















def main():









if __name__ == "__main__":
    main()

