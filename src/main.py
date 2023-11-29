from controller.main import Controller
from models.main import Model
from views.main import View


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    main()
