from PIL import Image


def mix(a, b, ratio_b):
    return a * (1-ratio_b) + b * ratio_b


def mix_colors(c1, c2, ratio_c2):
    return (round(mix(c1[0], c2[0], ratio_c2)),
            round(mix(c1[1], c2[1], ratio_c2)),
            round(mix(c1[2], c2[2], ratio_c2)))


def hsv_adjust_range(color, current_range):
    return (round(255*color[0]/current_range[0]),
            round(255*color[1]/current_range[1]),
            round(255*color[2]/current_range[2]))


class PixelPalette:
    """
    Can be used to create a color palette using hsv colors

    Attributes
    ----------
    hsv_range : Tuple[int, int, int]
        The range of (hue, saturation, value) of the colors used.
        Asesprite uses (360,100,100), GIMP let's you choose between (100,100,100) and (255,255,255).
        default here is (100,100,100)

    Methods
    -------
    add_gradient(color1, color2, number_in_between, hue_ascending=True)
         Adds a row to the palette with colors of a gradient

    add_shades(base_color, shift, number_down, number_up)
        Adds a row to the palette with shades of a base color. Shades can shift in hue, saturation and value.
    """
    def __init__(self, hsv_range=(100, 100, 100)):
        self.rows = []
        self.hsv_range = hsv_range
        return

    def add_gradient(self, color1, color2, number_in_between, hue_ascending=True):
        """
        Adds a row to the palette with colors of a gradient

        :param color1: Tuple[int, int, int]
            Start color of the gradient as (hue, saturation, value)
        :param color2: Tuple[int, int, int]
            End color of the gradient as (hue, saturation, value)
        :param number_in_between: int
            Number of colors in between the start and end colors
        :param hue_ascending: bool, optional
            Defines which part of the hue spectrum is used in the gradient.
            Orange -> Purple with hue_ascending=True creates a gradient [Orange->Yellow->Green->Blue->Purple].
            Orange -> Purple with hue_ascending=False creates a gradient [Orange->Red->Pink->Purple].
        :return:
        """
        color1 = hsv_adjust_range(color1, self.hsv_range)
        color2 = hsv_adjust_range(color2, self.hsv_range)
        new_row = [color1]

        if not hue_ascending:
            color1 = (color1[0] + 255, color1[1], color1[2])

        for i in range(number_in_between):
            c = mix_colors(color1, color2, (i+1)/(number_in_between+1))
            c = (c[0] % 255, c[1], c[2])
            new_row.append(c)
        new_row.append(color2)
        self.rows.append(new_row)

    def add_shades(self, base_color, shift, number_down, number_up):
        """
        Adds a row to the palette with shades of a base color. Shades can shift in hue, saturation and value.

        :param base_color: the base color as (hue, saturation, value)
        :param shift: the amount of shift in (hue, saturation, value) each shade should have
        :param number_down: the number of shades darker (with the shift substracted)
        :param number_up:  the number of shades lighter (with the shift added)
        :return:
        """
        base_color = hsv_adjust_range(base_color, self.hsv_range)
        shift = hsv_adjust_range(shift, self.hsv_range)
        new_row = []
        for i in range(-number_down, number_up+1):
            new_row.append((base_color[0] + shift[0]*i,
                            base_color[1] + shift[1]*i,
                            base_color[2] + shift[2]*i))
        self.rows.append(new_row)

    def save_as_image(self, filename):
        width = 0
        for row in self.rows:
            width = max(width, len(row))

        image = Image.new('HSV', (width, len(self.rows)))
        pixels = []
        for row in self.rows:
            for i in range(width):
                pixels.append(row[i] if i < len(row) else (0, 0, 0))
        image.putdata(pixels)
        image = image.convert('RGB')
        image.save(filename)


# No interface (yet), input has to be hard coded
palette = PixelPalette(hsv_range=(360, 100, 100))
palette.add_gradient((48, 19, 99), (16, 60, 99), 2)
palette.add_gradient((16, 60, 99), (217, 25, 12), 5, False)
palette.add_shades((138, 32, 77), (-10, -10, 25), 2, 1)
palette.add_shades((25, 56, 77), (10, -10, 25), 3, 3)
palette.save_as_image("palette.png")
