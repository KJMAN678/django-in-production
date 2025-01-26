from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Returns total number of blogs"

    def add_arguments(self, parser):
        parser.add_argument("custom_inputs", nargs="+", type=int)
        parser.add_argument(
            "--custom",
            type=int,
            help="custom help optional param",
        )

    def handle(self, *args, **options):
        print(f"Custom inputs - {options['custom_inputs']}")
        print(f"Custom - {options['custom']}")
