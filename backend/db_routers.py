"""
Database router for multi-database setup.
Routes database operations based on model's managed flag.
"""


class ModelDatabaseRouter:
    """
    Routes database operations based on model's managed flag.
    - managed=False models → 'course_db' (existing course database)
    - managed=True models → 'default' (existing primary database)
    """

    def db_for_read(self, model, **hints):
        if model._meta.managed == False:
            return 'course_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.managed == False:
            return 'course_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db1 = 'course_db' if obj1._meta.managed == False else 'default'
        db2 = 'course_db' if obj2._meta.managed == False else 'default'
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # In DATABASE mode, never run migrations (tables exist)
        # In TEST mode, allow migrations to create schema
        from django.conf import settings
        if hasattr(settings, 'USE_TEST_MODE') and settings.USE_TEST_MODE:
            return True
        return False
