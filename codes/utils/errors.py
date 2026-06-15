class MapError(Exception):
    """Map error
    """
    def __init__(self, *args: object) -> None:
        """Initializing the exception error
        """
        super().__init__(*args)
