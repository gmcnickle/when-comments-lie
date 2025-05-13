import os
import django
from django.conf import settings
from django.db import connection, reset_queries

def setup():
    BASE_DIR = os.path.dirname(__file__)

    # Minimal Django settings for test execution
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
            }
        },
        INSTALLED_APPS=['testapp'],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )

    # Initialize Django
    django.setup()

    from django.core.management import call_command
    call_command('makemigrations', 'testapp', verbosity=0)
    call_command('migrate', verbosity=0)


    from testapp.models import Library, Book, Edition

    # Setup test data
    edition, _ = Edition.objects.get_or_create(name="First Edition")
    library, _ = Library.objects.get_or_create(name="Main Library")
    Book.objects.get_or_create(
        library=library,
        edition=edition,
        title="When Comments Lie: A Case Study in ORM Behavior"
    )

    return edition, library

def print_queries():
    print(f"\nTotal queries executed: {len(connection.queries)}")

    for i, q in enumerate(connection.queries, start=1):
        print(f"\nQuery {i} ({q['time']}s):\n{q['sql']}")


def test_original_path(library):
    if not library:
        print("No Library found — did you run setup?")
        return

    reset_queries() # reset before the call to .all()

    print(f"\r\n")
    print(f"Testing query count using .all and iteration before referencing the foreign key field 'edition'")
    print(f"------------------------------------------------------------------------------------------------------")
    books = library.books.all()
    for book in books:     
        _ = book.edition.name
        break

    print_queries()

def test_select_related(library):
    reset_queries() # reset before the call to .first()

    print(f"\r\n")
    print(f"Testing query count using .first and select_related before referencing the foreign key field 'edition'")
    print(f"------------------------------------------------------------------------------------------------------")
    book = library.books.select_related('edition').first()
    if book:
        _ = book.edition.name

    print_queries()


os.system('cls')
edition, library = setup()
test_original_path(library)
test_select_related(library)
