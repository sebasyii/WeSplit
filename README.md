#### Scenario
WeSplit is an application designed for groups of friends, family members, or colleagues who frequently engage in shared expenses, whether it's for meals, trips, or communal purchases. Managing shared expenses can often lead to confusion and misunderstandings about who owes what to whom. WeSplit aims to simplify this process, making it transparent and stress-free.

Imagine a group of college friends living together or a family on vacation. They often find themselves in situations where expenses are not split evenly, and tracking who has paid for what becomes a challenge. WeSplit provides a solution by allowing users to create groups, add members, record expenses, and calculate how to settle debts in the most efficient way possible.

#### Description of the Application
WeSplit is an application that facilitates the management of shared expenses within a group. Users can create a group, and start adding expenses right away. Each expense can be recorded with details such as the amount, who paid for it, and how it should be split among the members. The application supports various splitting methods, including equal split, exact amounts, and percentages.

The core features of WeSplit include:
- **Group Creation**: Users can create a new group, give it a name and description, and add members.
- **Expense Recording**: Users can log each expense, specify who paid, and choose the split type.
- **Balance Calculation**: The application calculates how much each member owes or is owed, streamlining the process of settling up.
- **Debt Settlement**: WeSplit suggests the minimum number of transactions required to settle all debts within the group.
- **Data Export**: Users have the option to export the group's expenses and settlements to a CSV file for external use or record-keeping.

The application is designed with a clean and intuitive interface, making it easy for users to navigate and perform actions with minimal clicks.

To run,

### Create a Virtual Environment

```bash
python3 -m venv env
```

### Activate the Virtual Environment

#### For MacOS

```bash
source ./env/bin/activate
```

#### For Windows

```bash
.\env\Scripts\activate
```

### Install the requirements

```bash
pip install -r requirements.txt
```

### Run

```bash
python3 src/main.py
```