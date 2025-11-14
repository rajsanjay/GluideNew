"""
Database routers for multi-database setup.
Routes course-related models to the course_db database.
"""


class ProductionDatabaseRouter:
    """
    A router to control database operations for models in the
    multi-database setup (production/database mode).
    """

    course_db_apps = {'api'}  # Apps that use course_db
    course_db_models = ['models_course_db']  # Models that use course_db

    def db_for_read(self, model, **hints):
        """
        Route read operations for course models to course_db.
        """
        if model._meta.app_label in self.course_db_apps:
            if hasattr(model, '_database'):
                return model._database
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Route write operations for course models to course_db.
        """
        if model._meta.app_label in self.course_db_apps:
            if hasattr(model, '_database'):
                return model._database
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects in the same database.
        """
        db1 = obj1._state.db or 'default'
        db2 = obj2._state.db or 'default'
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that models only appear in the appropriate database.
        """
        if app_label in self.course_db_apps:
            if model_name and 'course' in model_name.lower():
                return db == 'course_db'
        return db == 'default'


class TestDatabaseRouter:
    """
    A router for test mode that uses SQLite databases.
    """

    def db_for_read(self, model, **hints):
        """
        Route read operations based on model metadata.
        """
        if hasattr(model, '_database'):
            return model._database
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Route write operations based on model metadata.
        """
        if hasattr(model, '_database'):
            return model._database
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow all relations in test mode.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations in test mode.
        """
        return True
