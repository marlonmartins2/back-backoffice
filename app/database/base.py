from pymongo import MongoClient

from settings import settings


class Index(type):
    """
    Metaclass to create indexes in MongoDB.
    Args:
        type (type): Metaclass.
    """

    def __init__(cls, *args, **kwargs):
        """
        Create index in MongoDB.
        """
        if hasattr(cls, "index"):
            cls.get_instance().create_index(cls.index, unique=True)
        super().__init__(*args, **kwargs)


class BaseConnection:
    """
    Base class to connect to MongoDB.
    """
    if settings.MONGO_SSL is True:
        connection = MongoClient(
            settings.MONGO_URL,
            tls=True,
            tlsCAFile=settings.PATH_CERT,
            tlsAllowInvalidHostnames=True,
            retryWrites=False,
            directConnection=True,
        )
    else:
        connection = MongoClient(settings.MONGO_URL)


class BaseDB(BaseConnection, metaclass=Index):
    """
    Base class to connect to MongoDB.

    :param BaseConnection: Base class to connect to MongoDB.
    :metaclass Index: Metaclass to create indexes in MongoDB.
    """
    database = settings.DATABASE_ENVIRONMENT


database = BaseDB.connection[BaseDB.database]
