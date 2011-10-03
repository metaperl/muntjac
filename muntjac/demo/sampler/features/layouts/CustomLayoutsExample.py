# -*- coding: utf-8 -*-
# from com.vaadin.ui.PasswordField import (PasswordField,)


class CustomLayoutsExample(VerticalLayout):

    def __init__(self):
        self.setMargin(True)
        # Create the custom layout and set it as a component in
        # the current layout
        custom = CustomLayout('../../sampler/layouts/examplecustomlayout')
        self.addComponent(custom)
        # Create components and bind them to the location tags
        # in the custom layout.
        username = TextField()
        custom.addComponent(username, 'username')
        password = PasswordField()
        custom.addComponent(password, 'password')
        ok = Button('Login')
        custom.addComponent(ok, 'okbutton')