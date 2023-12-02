from typing import Type, TypedDict

from .base import BaseView
from .root import App
from .home import HomeView
from .create_expense import CreateExpenseView
from .create_group import CreateGroupView
from .group import GroupView
from .history import HistoryView

class Frames(TypedDict):
    home: HomeView
    create_expense: CreateExpenseView
    create_group: CreateGroupView
    group: GroupView
    history: HistoryView

class View:
    def __init__(self):
        self.root = App("WeSplit", (800, 600))
        self.frames: Frames = {}

        self._add_frame(CreateExpenseView, "create_expense")
        self._add_frame(CreateGroupView, "create_group")
        self._add_frame(GroupView, "group")
        self._add_frame(HistoryView, "history")
        self._add_frame(HomeView, "home")

    def _add_frame(self, Frame: Type[BaseView], name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].place(relwidth=1, relheight=1)

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self) -> None:
        self.root.mainloop()
