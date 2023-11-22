class Expense:
    def __init__(self, description, amount, paid_by, split_type, split_details):
        # Validate description
        if not description:
            raise ValueError("Description cannot be empty")

        # Validate amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")

        # Validate payer ID
        if not paid_by:
            raise ValueError("Payer ID cannot be empty")

        # Validate split type
        if split_type not in ["equal", "percentage", "exact"]:
            raise ValueError("Invalid split type")
        
        # If split type == equal, then all values in split_details must be amount / len(split_details)
        if split_type == "equal":
            indiv_amount = amount / len(split_details)
            for id, amount in split_details.items():
                if amount != indiv_amount:
                    raise ValueError("Split amounts must be equal")

        if split_type == "percentage" and sum(split_details) != 100:
            raise ValueError("Percentage split amounts must sum to 100")

        if split_type == "exact":
            if sum(split_details.values()) != amount:
                raise ValueError("Exact split amounts must sum to the total amount")

        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.split_type = split_type
        self.split_details = split_details

    # def add_participant(self, user_id):
    #     # Validate user ID
    #     if not user_id:
    #         raise ValueError("User ID cannot be empty")

    #     # Validate split amount
    #     if not isinstance(split_amount, (int, float)) or split_amount <= 0:
    #         raise ValueError("Split amount must be a positive number")

    #     # Check if user is already a participant
    #     if user_id in self.split_amounts:
    #         raise ValueError("User is already a participant")

    #     # Update split amounts
    #     self.split_amounts[user_id] = split_amount

    # def update_split_amount(self, user_id, new_split_amount):
    #     # Validate user ID
    #     if not user_id:
    #         raise ValueError("User ID cannot be empty")

    #     # Validate new split amount
    #     if not isinstance(new_split_amount, (int, float)) or new_split_amount <= 0:
    #         raise ValueError("New split amount must be a positive number")

    #     # Check if user is a participant
    #     if user_id not in self.split_amounts:
    #         raise ValueError("User is not a participant")

    #     # Update split amounts
    #     self.split_amounts[user_id] = new_split_amount
