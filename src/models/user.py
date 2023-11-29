class User:
    _id_counter = 0

    def __init__(self, name: str):
        self._id = User._id_counter
        User._id_counter += 1

        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name

    @property
    def id(self) -> int:
        return self._id

    def __str__(self) -> str:
        return self.name
