#!/usr/bin/env python2

import StringIO

class Color(object):
    """Abstract base class for Colors."""

    def __init__(self, scale):
        self.scale = scale

    def get_rgb(self):
        raise NotImplementedError("""All end-use subclasses of Color should define
        a get_rgb method.""")

    def get_scale(self):
        """Half-abstract method. A scale attribute must be set first."""

        if not hasattr(self, "scale"):
            raise NotImplementedError("""All end-use subclasses of Color should define
            a get_scale method.""")

        return self.scale

class RGBColor(Color):
    """RGB color."""

    def __init__(self, scale, rgb):
        """Create a color based on an RGB tuple."""

        super(RGBColor, self).__init__(scale)
        self.rgb = rgb

    def get_rgb(self):
        return self.rgb


class GrayscaleColor(Color):
    """Grayscale color."""

    def __init__(self, scale, gray):
        """Create a color based on an grayscale color."""

        super(GrayscaleColor, self).__init__(scale)
        self.gray = gray

    def get_rgb(self):
        return tuple([self.gray] * 3)


class BinaryColor(Color):
    """Binary color."""

    def __init__(self, boolee):
        """Create a color based on an boolable value color."""

        super(BinaryColor, self).__init__(1)
        self.boolee = bool(boolee)

    def get_rgb(self):
        return tuple([int(self.boolee)] * 3)


class PixelSource(object):
    """Abstract base class for PixelSources.

    Your classes need not derive from it, though it'd be nic if they did,
    because:
        -> you only need to implement part of the methods then
        -> it raises exceptions when you don't override some of it's methods
            (which you ought to override).

    You see - it's for your own good!"""

    def get_width(self):
        if not hasattr(self, 'w'):
            raise NotImplementedError("""A PixelSource needs to implement a get_width
            method.""")

        return self.w

    def get_height(self):
        if not hasattr(self, 'h'):
            raise NotImplementedError("""A PixelSource needs to implement a
            get_height method.""")

        return self.h

    def get_size(self):
        return (self.get_width(), self.get_height())

    def pixels(self):
        raise NotImplementedError("""A PixelSource needs to implement a pixels
        method.""")

class PixelMatrix(PixelSource):
    def __init__(self, width, height, default=BinaryColor(False)):
        self.matrix = [[default for i in range(width)] for j in range(height)]
        self.w = width
        self.h = height

    def set_at(self, pos, color):
        i, j = pos
        self.matrix[i][j] = color

    def get_at(self, pos):
        i, j = pos
        return self.matrix[i][j]

    def pixels(self):
        for row in self.matrix:
            for pixel in row:
                yield pixel

class PAnyMImage(object):
    """Abstract base class for P*MImages."""

    def __init__(self, pixel_source, scale=255):
        self.pixel_source = pixel_source
        self.scale = scale

    def get_header(self):
        raise NotImplementedError("""A P*Image must implement a get_header
        method.""")

    def format_pixel(self):
        raise NotImplementedError("""A P*Image must implement a format_pixel
        method.""")

    def get_scale(self):
        return self.scale

    def get_content(self):
        c = StringIO.StringIO()

        for pixel in self.pixel_source.pixels():
            c.write("%s\n" % self.format_pixel(pixel))

        return c.getvalue()

    def get_file_content(self):
        """Return the content of a file of a given format."""
        s = StringIO.StringIO()

        s.write(self.get_header())
        s.write(self.get_content())

        return s.getvalue()

    def save_to(self, filelike_or_name):
        if hasattr(filelike_or_name, "write"):
            filelike_or_name.write(self.get_file_content())

        elif type(filelike_or_name) in (str, unicode):
            with open(filelike_or_name, 'w') as f:
                f.write(self.get_file_content())

class PPMImage(PAnyMImage):
    """PPM Image."""

    def get_header(self):
        w, h = self.pixel_source.get_size()
        return "P3 %d %d %d\n" % (w, h, self.get_scale())

    def format_pixel(self, pixel):
        return '%d %d %d' % tuple(int(channel * self.get_scale() / pixel.get_scale())
                for channel in pixel.get_rgb())

class PGMImage(PAnyMImage):
    """PGM Image."""

    def get_header(self):
        w, h = self.pixel_source.get_size()
        return "P2 %d %d %d\n" % (w, h, self.get_scale())

    def format_pixel(self, pixel):
        r, g, b = pixel.get_rgb()

        in_scale = pixel.get_scale()
        out_scale = self.get_scale()

        l = int((0.3  * r + 0.59 * g + 0.11 * g) * out_scale / in_scale)

        return '%d %d %d' % (l, l, l)

class PBMImage(PAnyMImage):
    """PBM Image."""

    def get_header(self):
        return "P2 %d %d\n" % self.pixel_source.get_size()

    def format_pixel(self, pixel):
        r, g, b = pixel.get_rgb()

        in_scale = pixel.get_scale()
        out_scale = self.get_scale()

        l = int((0.3  * r + 0.59 * g + 0.11 * g) * out_scale / in_scale)

        return str(l)

if __name__ == "__main__":
    size = 1000
    m = PixelMatrix(size, size)
    for i in range(m.get_height()):
        for j in range(m.get_width()):
            m.set_at((i, j), RGBColor(size, ((i * j) % size, 0, 0)))
    i = PPMImage(m, size)
    i.save_to('image.ppm')
