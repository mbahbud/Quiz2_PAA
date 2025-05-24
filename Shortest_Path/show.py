import pygame
from math import sqrt

def type_check(name, correct_type):
    """
    Decorator function for checking correctness of input type
    name: attribute name --> str
    correct_type: correct_type of name attribute --> type
    Procedure:
    1. Call type_check first, return prop setter, and convert name to private attribute. Store private_name & correct_type information.
    2. Class initializing attribute
    3. When initializing name attribute, it'll call prop and check type of input. If type is wrong, raise error; or set attribute by setattr function.
    """
    private_name = '_' + name

    @property
    def prop(self):
        return getattr(self, private_name)
    
    @prop.setter
    def prop(self, value):
        if not isinstance(value, correct_type):
            raise ValueError("{} must be a {}".format(private_name, correct_type))
        setattr(self, private_name, value)

    return prop

class CirButton:
    """
    Create circular Button object for different usage
    
    center: center of circle --> tuple
    top: radius of circle --> int
    text: text of button --> str
    textcolor: color of text --> tuple, ex:(0,0,0)
    rectcolor: color of button --> tuple, ex:(255, 255, 255)
    screen: pygame object "pygame.display.set_mode()"
    font: font of text
    """
    # Do not allow adding other attributes
    __slots__ = ["_center", "_radius", "_text", 
                 "_textcolor", "_circolor",
                 "_screen", "_font"]

    textcolor = type_check("textcolor", tuple)
    circolor = type_check("circolor", tuple)

    def __init__(self, center:tuple, radius:int, text:str, 
                       textcolor:tuple, circolor:tuple,
                       screen:pygame, font:pygame):
        self._radius = radius
        self._center = center
        self._text = text
        self._screen = screen
        self._font = font
        self.textcolor = textcolor
        self.circolor = circolor

    def __call__(self):
        button_text = self._font.render(self._text, True, self._textcolor)
        button_rect = button_text.get_rect()
        button_rect.center = self._center
        pygame.draw.circle(self._screen, self._circolor, self._center, self._radius)
        self._screen.blit(button_text, button_rect)
    
    def color_change(self, color:tuple):
        """
        Change color of button

        color: color of button --> tuple, ex:(255, 255, 255)
        """
        self.circolor = color
    
    def distance(self, mouse_pos:tuple)->float:
        """
        Compute distance between button and mouse

        mouse_pos: position of mouse --> tuple, ex:(x, y)
        """
        return sqrt((self._center[0]-mouse_pos[0])**2 + (self._center[1]-mouse_pos[1])**2)

class RectButton:
    """
    Create rectangular Button object for different usage

    left: left boundary of button --> int
    top: top boundary of button --> int
    width: width of button --> int
    height: height of button --> int
    text: text of button --> str
    textcolor: color of text --> tuple, ex:(0,0,0)
    rectcolor: color of button --> tuple, ex:(255, 255, 255)
    screen: pygame object "pygame.display.set_mode()"
    font: font of text
    """
    # Do not allow adding other attributes
    __slots__ = ["_left", "_top", "_width", "_height", 
                 "_text", "_textcolor", "_rectcolor",
                 "_screen", "_font", "rect"]

    textcolor = type_check("textcolor", tuple)
    rectcolor = type_check("rectcolor", tuple)

    def __init__(self, left:int, top:int, width:int, height:int, 
                       text:str, textcolor:tuple, rectcolor:tuple,
                       screen:pygame, font:pygame):
        self._left = left
        self._top = top
        self._width = width
        self._height = height
        self._text = text
        self._screen = screen
        self._font = font
        self.rect = pygame.Rect(self._left, self._top, self._width, self._height)
        self.textcolor = textcolor
        self.rectcolor = rectcolor

    def __call__(self):
        # Draw border (darker shade for a raised effect)
        border_rect = pygame.Rect(self._left - 2, self._top - 2, self._width + 4, self._height + 4)
        pygame.draw.rect(self._screen, (20, 20, 20), border_rect)  # Darker border
        # Draw main button
        button_text = self._font.render(self._text, True, self._textcolor)
        button_rect = button_text.get_rect()
        button_rect.center = self.rect.center
        pygame.draw.rect(self._screen, self._rectcolor, self.rect)
        self._screen.blit(button_text, button_rect)
    
    def color_change(self, color:tuple):
        """
        Change color of button
        color: color of button --> tuple, ex:(255, 255, 255)
        """
        self.rectcolor = color

class ShowText:
    """
    Create Text object for different usage

    center: center of text --> tuple, ex:(x, y)
    text: text to show --> list, each element for different row
    textcolor: color of text --> tuple, ex:(0,0,0)
    screen: pygame object "pygame.display.set_mode()"
    font: font of text
    """
    # Do not allow adding other attributes
    __slots__ = ["_center", "_text", "_textcolor",
                 "_screen", "_font"]

    text = type_check("text", list)
    center = type_check("center", tuple)
    textcolor = type_check("textcolor", tuple)

    def __init__(self, center:tuple, text:list, textcolor:tuple, screen:pygame, font:pygame):
        self._screen = screen
        self._font = font
        self.center = center
        self.text = text
        self.textcolor = textcolor

    def __call__(self):
        for text in self._text:
            showtext = self._font.render(text, True, self._textcolor)
            textrect = showtext.get_rect()
            textrect.center = self._center
            self._screen.blit(showtext, textrect)