class ApiDatabaseRouter:
    """
    A router to direct database operations for the 'api' app to the 'api' database,
    while other apps (like auth, sessions) use the 'default' database.
    """

    def db_for_read(self, model, **hints):
        """
        Direct read operations for 'api' app models to the 'api' database.
        All other apps use the 'default' database.
        """
        if model._meta.app_label == "api":
            return "api_db"
        elif model._meta.app_label == "reference":
            return "reference_db"
        return "default"

    def db_for_write(self, model, **hints):
        """
        Direct write operations for 'api' app models to the 'api' database.
        All other apps use the 'default' database.
        """
        if model._meta.app_label == "api":
            return "api_db"

        elif model._meta.app_label == "reference":
            return "reference_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relationships only between models in the same database.
        Prevents cross-database relationships unless explicitly allowed.
        """
        db_list = ("default", "api_db", "reference_db")
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return obj1._state.db == obj2._state.db
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure 'api' app models are only migrated to the 'api' database.
        Other apps (like auth, sessions) are migrated to the 'default' database.
        """
        if app_label == "api":
            return db == "api_db"
        elif app_label == "reference":
            return db == "reference_db"

        elif app_label in ["auth", "admin", "contenttypes", "sessions"]:
            return db in ["default", "api_db"]
        return db == "default"
