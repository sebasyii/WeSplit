class User:
    """Represents a user in the app.

    This class encapsulates user details.
    Each user has a unique ID and can belong to multiple groups.

    Attributes:
        _id (int): A unique identifier for the user, automatically assigned.
        name (str): The name of the user.
        groups (list): A list to store group memberships.
    """

    _id_counter = 0

    def __init__(self, name: str):
        """Initialises a new instance of the User class.

        Args:
            name (str): The name of the user.

        Raises:
            ValueError: If the name provided is empty.
        """
        self._id = User._id_counter
        User._id_counter += 1

        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name

        self.groups = []  # List to store group memberships

    @property
    def id(self) -> int:
        """Read-only property for accessing the user's ID.

        Returns:
            int: The unique identifier of the user.
        """
        return self._id

    # def add_group(self, group) -> None:
    #     """Adds a group to the user's list of group memberships.

    #     Args:
    #         group (Group): The group to be added to the user's memberships.
    #     """
    #     self.groups.append(group)

    # def remove_group(self, group: Group) -> None:
    #     """Removes a group from the user's list of group memberships.

    #     Args:
    #         group (Group): The group to be removed from the user's memberships.

    #     Raises:
    #         ValueError: If the group is not found in the user's memberships.
    #     """
    #     try:
    #         self.groups.remove(group)
    #     except ValueError as e:
    #         raise ValueError("Group not found in the user's memberships.") from e

    def __str__(self) -> str:
        """String representation of the User.

        Returns:
            str: The name of the user.
        """
        return self.name
