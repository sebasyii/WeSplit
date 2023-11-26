class User:
    _id_counter = 0

    def __init__(self, name: str):
        """
        Initialize a new User with a unique ID and a name.
        The user can be a member of multiple groups.
        """
        self._id = User._id_counter
        User._id_counter += 1

        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name

        self.groups = []  # List to store group memberships

    @property
    def id(self) -> int:
        """Read-only property for the user's ID."""
        return self._id

    def add_group(self, group) -> None:
        """Add a group to the user's list of group memberships."""
        self.groups.append(group)

    def remove_group(self, group) -> None:
        """Remove a group from the user's list of group memberships."""
        self.groups.remove(group)

    def __str__(self) -> str:
        return self.name