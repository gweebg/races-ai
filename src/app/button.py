import pygame


# Button colors.
TOP_COLOR = '#475F77'
BOT_COLOR = '#354B5E'
TXT_COLOR = '#FFFFFF'
HVR_COLOR = '#D74B4B'
DST_COLOR = '#9a9b9c'
DSB_COLOR = '#4d4e4f'


class Button:
    """
    This class represents an elevated button.

    First we set up the button: b = Button(...)
    We set its position: b.set_position((x,y))
    Then, we set its event handler: b.set_handler(func, *args)
    Finally, we draw it on our app loop: b.draw()
    """

    def __init__(self, text: str, width: int, height: int, elevation: int, screen, font) -> None:
        """
        Constructor of a button!

        :param text: The text the button should display.
        :param width: The width of the button.
        :param height: The height of the button.
        :param elevation: Button's elevation, if set to 0 it's a normal button.
        :param screen: The screen where to put the button.
        :param font: The text font.
        """

        # The text_rect and text_surf represent the text that's going onto the button!
        self.text_rect, self.text_surf = None, None

        # Represents the bottom rectangle to give the impression of elevation.
        self.bottom_color, self.bottom_rect = None, None

        # The main rectangle (button) where almost all logic goes onto.
        self.top_color, self.top_rect = None, None

        # Storing the original y position, since this will vary with time.
        self.original_y_pos = None

        # The state that indicates whether the button is pressed or not.
        self.pressed = False
        self.disabled = False

        # The handle and respective arguments to the button on click event.
        self.handle, self.args = None, None

        # Here lies the screen where to put the button and the font for the text.
        self.screen = screen
        self.font = font

        # Storing the button width and height and position.
        self.pos = None
        self.width, self.height = width, height

        # Elevation handles.
        self.elevation = elevation  # Button base elevation.
        self.dynamic_elevation = elevation  # Button current elevation.

        # Button top and bottom rectangle colors.
        self.top_color = TOP_COLOR
        self.bottom_color = BOT_COLOR

        # Text render for the button.
        self.text_surf = self.font.render(text, True, TXT_COLOR)

    def set_position(self, position: tuple) -> None:
        """
        Since there's no position positional parameter on the constructor for this class, we have to set
        the button's position using this method. Besides setting the position, it also creates or updates
        every necessary components.

        :param position: Tuple of numeric values like (x, y).
        :return: None
        """

        # Storing essential values.
        self.pos = position
        self.original_y_pos = int(position[1])

        # Creating the top rectangle of the elevated button.
        self.top_rect = pygame.Rect(self.pos, (self.width, self.height))

        # Creating the bottom rectangle!
        self.bottom_rect = pygame.Rect(self.pos, (self.width, self.elevation))

        # Setting the text in the center of the top rectangle.
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def set_handle(self, handle, *args) -> None:
        """
        This is the event handler setter.

        :param handle: The function it should run.
        :param args: The arguments to the handle function.
        :return: None
        """
        self.handle = handle
        self.args = args

    def disable(self):
        """
        Disable the button turning it gray!
        :return: None
        """

        self.disabled = True
        self.top_color = DST_COLOR
        self.bottom_color = DSB_COLOR

    def enable(self):
        """
        Enable the button turning it back to normal!
        :return: None
        """

        self.disabled = False
        self.top_color = TOP_COLOR
        self.bottom_color = BOT_COLOR

    def draw(self) -> None:
        """
        Method responsible for drawing the button into the screen.
        :return: None
        """

        # Elevation logic.
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        # Drawing the bottom rectangle.
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)

        # Drawing the top rectangle and rendering the text in its center.
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)

        self.on_click(self.handle, *self.args)

    def on_click(self, on_click_event=None, *args) -> None:
        """
        This method checks whether the button was clicked or not and executes the 'on_click_event' if so.

        :param on_click_event: A function that acts as the on click event.
        :param args: The arguments to the function 'on_click_event'.
        :return: None
        """

        if not self.disabled:

            # Getting our mouse position!
            mouse_pos = pygame.mouse.get_pos()

            # Checking if the mouse is colliding with our button.
            if self.top_rect.collidepoint(mouse_pos):

                self.top_color = HVR_COLOR  # Changing the button color on hover.

                if pygame.mouse.get_pressed()[0]:  # Checking if the mouse button was clicked.
                    self.dynamic_elevation = 0  # Resetting the elevation.
                    self.pressed = True

                elif self.pressed:
                    # Setting elevation to original state.
                    self.dynamic_elevation = self.elevation

                    # The button was pressed!
                    self.pressed = False

                    if on_click_event:
                        on_click_event(*args)

            else:
                # Setting elevation to original state.
                self.dynamic_elevation = self.elevation

                # Setting the color to its original state.
                self.top_color = TOP_COLOR
