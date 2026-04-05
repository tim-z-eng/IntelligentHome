from controller.controller import AuthController
# from controller.controller import MainController
from view.view import LoginView
from view.view import MainView

if __name__ == "__main__":
    auth_controller = AuthController()
    login_view = LoginView(auth_controller, "Login - Intelligent Home Appliance Control System", 300, 400)
    login_view.run()

    main_controller = AuthController()
    main_view = MainView(main_controller, "Main", 900, 600)
    main_view.run()