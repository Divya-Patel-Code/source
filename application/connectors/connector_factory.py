from application.models.providers import Provider
from application.utils.exceptions import AppException

CONNECTORS = {}

def register_connector(name: str):
    def decorator(cls):
        key = name.lower()

        if key in CONNECTORS:
            raise Exception(f"Connector '{name}' already registered")

        CONNECTORS[key] = cls
        return cls

    return decorator


class ConnectorFactory:

    @staticmethod
    def get_connector(provider: Provider, config: dict):
        connector_class = CONNECTORS.get(provider.value.lower())

        if not connector_class:
            raise AppException(f"Unsupported provider: {provider.title}", 400)

        try:
            connector = connector_class(**config)
            return connector

        except TypeError as e:
            raise AppException(f"Invalid configuration: {str(e)}", 400)

        except Exception as e:
            raise AppException(f"Failed to initialize {provider.value} connector: {str(e)}", 400)