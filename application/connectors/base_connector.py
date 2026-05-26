class BaseConnector():
    def __init__(self, config):
        self.config = config

    def test_connection(self):
        raise NotImplementedError