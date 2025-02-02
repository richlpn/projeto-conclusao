from functools import wraps
from src.config.database.database import create_session
from sqlalchemy.exc import SQLAlchemyError


def handle_sqlalchemy_session(func):
    """
    A decorator to handle SQLAlchemy exceptions for class methods.
    Rolls back the transaction in case of an error.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            # Execute the decorated function
            self.db = create_session()
            result = func(self, *args, **kwargs)
            # Commit the transaction if successful
            self.db.commit()
            return result
        except SQLAlchemyError as e:
            # Rollback the transaction on error
            self.db.rollback()
            raise e  # Re-raise the exception for external handling
        except Exception as err:
            raise Exception(f"Error while executing '{func}': {err}") from err

    return wrapper
