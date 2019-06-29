# django_testing_boilerplate_scaffolding
A django management command which creates testing files and testing classes.

It's akin to php artisan make:test.
It requires that tests be placed inside app level designated "tests" directories.

It requires that these "tests" directories contain an __init__.py.

It checks for duplicate tests and warns the user if they want to overwrite them.

It automatically prependes "test_" and appends ".py" to the name of the file, respectively.

Call it like any other management command(from the project folder):

```python
python manage.py mt app_name test_name
```

