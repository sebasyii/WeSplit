class User:
    _id_counter: int = 0

    def __init__(self, name: str):
        self._id = User._id_counter
        User._id_counter += 1

        self.name = name

    @property
    def id(self) -> int:
        return self._id

    def __str__(self) -> str:
        return self.name
