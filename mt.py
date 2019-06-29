from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import os

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name', nargs = 1,
            type = str
        )
        parser.add_argument(
            'test_name', nargs = 1,
            type = str
        )

    def see_if_test_already_exists(self, **options):
        tests = [file for file in os.walk(f"./{options['app_name'][0]}/tests")]
        for a in tests:
            for b in a:
                if f"test_{options['test_name'][0]}.py" in b:
                    return "Exists."


    def ask_user_if_he_wants_to_overwrite_test(self):
        user_input = str(input(
"""
Test already exists.
Press y to overwrite,
press anything else to cancel:
 """
        ))
        if user_input == 'y' or user_input == 'Y':
            return "continue"
        else:
            self.stderr.write("Exiting.")

    def see_if_tests_dir_present(self, **options):
        try:
            dirs = os.listdir(f"./{options['app_name'][0]}")
            if 'tests' not in dirs:
                self.stderr.write("tests folder missing.")
        except FileNotFoundError:
            raise CommandError(
                f"{options['app_name'][0]} not found."
            )

    def see_if_init_present_in_tests(self, **options):
        pys = []
        for p, d, f in os.walk(f"./{options['app_name'][0]}/tests"):
            for file in f:
                if file.endswith('.py'):
                    pys.append(file)
        if "__init__.py" in pys:
            self.stdout.write("init present")
        else:
            raise CommandError("init missing.")

    def create_test(self, **options):
        pth = os.path.abspath(
            os.path.join(
                options['app_name'][0],
                f"tests/test_{options['test_name'][0]}.py"
            )
        )

        with open(pth, "w") as outbound:
            outbound.write(
f"""from django.test import TestCase, RequestFactory
from django.urls import reverse

class Test{options['test_name'][0]}(TestCase):

    def test_(self):
        response = self.client.get(
            reverse('name')
        )
        self.assertEqual(
            response.status_code,
            200
        )
            """)
        self.stdout.write(
            f"{options['test_name'][0]} created."
        )

    def handle(self, *args, **options):
        self.see_if_tests_dir_present(**options)
        self.see_if_init_present_in_tests(**options)
        if self.see_if_test_already_exists(**options) == "Exists.":
            if self.ask_user_if_he_wants_to_overwrite_test() == "continue":
                self.create_test(**options)
        else:
            self.create_test(**options)
