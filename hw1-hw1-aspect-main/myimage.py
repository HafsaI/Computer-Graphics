from PIL import Image, ImageDraw
import inspect


class MyImage:
    """A basic image manipulation class.

    The image is a grid of virtual pixels separated by grid lines. Each virtual
    pixel is a square of actual screen pixels. All virtual pixels have the same
    size.

    The used coornidate system has its origin at the top left of the image.
    """

    def __init__(self, size: (int, int), grid_width: int, pixel_size: int, mode: str = 'RGBA'):
        '''Creates an instance.

        mode must be RGBA or CMYK. In both cases, pixels will store a 4-tuple of
        integer values in [0,255]. The mode determines the color corresponding
        to a 4-tuple.

        All integer values MUST be non-negative.

        Arguments:
        self: automatic object reference.
        size: (xres, yres). xres columns and yres rows of virtual pixels in the created image.
        grid_width: thickness of the grid lines in the created image.
        pixel_size: size of each virtual pixel.
        mode: the mode of the image.

        Returns:
        None.
        '''
        # Save image parameters.
        self.size: (int, int) = size
        self.grid_width: int = grid_width
        self.pixel_size: int = pixel_size
        self.mode: str = mode
        # Determine the pixel resolution resolution of the image to create.
        xsize: int = grid_width + size[0] * (pixel_size + grid_width)
        ysize: int = grid_width + size[1] * (pixel_size + grid_width)
        # Create the image. It is blank (black for RGBA, white for CMKY).
        self.img: Image = Image.new(mode, (xsize, ysize))
        # Store an instance for drawing in the created image.
        self.idraw: ImageDraw = ImageDraw.Draw(self.img)

        # Draw gridlines.
        if grid_width > 0:
            gray: tuple = (128,) * 4  # gray value, good for both  modes.
            start = (grid_width-1) // 2  # account for width
            for x in range(start, xsize, pixel_size+grid_width):
                self.idraw.line((x, 0, x, ysize), fill=gray, width=grid_width)
            for y in range(start, ysize, pixel_size+grid_width):
                self.idraw.line((0, y, xsize, y), fill=gray, width=grid_width)

    def __iter__(self):
        '''Returns color of next row-wise virtual pixel.

        Arguments:
        self: automatic object reference.

        Returns:
        Color of next row-wise virtual pixel.
        '''
        for y in range(self.img.size[1]):
            for x in range(self.img.size[0]):
                yield self.getpixel((x, y))

    def show(self):
        '''Displays the image.

        Uses a suitable image viewing program installed on the system.

        Arguments:
        self: automatic object reference.

        Returns:
        None.
        '''
        # Use show method from PIL.
        self.img.show()

    def _get_bbox(self, xy: (int, int)) -> (int, int, int, int):
        '''Returns the bounding box of a virtual pixel in pixel coordinates.

        The bounding box is represented as (xmin, ymin, xmax, ymax).

        Arguments:
        self: automatic object reference.
        xy: (x, y) coordinates of the virutal pixel.

        Returns:
        The bounding box of the indicated virtual pixel.
        '''
        # Check for valid coordinates.
        vx, vy = xy
        assert 0 <= vx < self.size[0], \
            f"{__class__.__name__}.{inspect.stack()[0][3]}: "\
            f"bad x-coordinate {vx} for image of resolution {self.size}"
        assert 0 <= vy < self.size[1], \
            f"{__class__.__name__}.{inspect.stack()[0][3]}: "\
            f"bad y-coordinate {vy} for image of resolution {self.size}"
        # Compute top left of bbox, i.e. xmin, ymin.
        xmin = self.grid_width + vx * (self.pixel_size + self.grid_width)
        ymin = self.grid_width + vy * (self.pixel_size + self.grid_width)
        # Compute bottom right of bbox, i.e. xmax, ymax. These are offset from
        # the top left by the size of the virtual pixel. Subtract 1 to include
        # xmin and ymin.
        xmax = xmin + self.pixel_size - 1
        ymax = ymin + self.pixel_size - 1
        # Return bbox.
        return (xmin, ymin, xmax, ymax)

    def putpixel(self, xy: (int, int), color: (int,)*4):
        '''Sets the color of a virtual pixel.

        Arguments:
        self: automatic object reference.
        xy: (x, y) coordinates of the virutal pixel.
        color: the color to be set.

        Returns:
        None.
        '''
        # Fill the bounding box of the virtual pixel with color.
        self.idraw.rectangle(self._get_bbox(xy), fill=color)

    def getpixel(self, xy: (int, int)) -> (int,)*4:
        '''Returns the color of a virtual pixel.

        Arguments:
        self: automatic object reference.
        xy: (x, y) coordinates of the virutal pixel.

        Returns:
        The color of the virtual pixel.
        '''
        # Return the color of the top left pixel of the virtual pixel.
        return self.img.getpixel(self._get_bbox(xy)[:2])

    def getdata(self) -> [(int,)*4]:
        '''Returns the virtual pixels contained in the image.

        The list contains row-wise virtual pixels, each represented by its color
        value.

        Arguments:
        self: automatic object reference.

        Returns:
        The contained virtual pixels.
        '''
        # Fill and return a list of row-wise virtual pixels.
        pixels = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pixels.append(self.getpixel((x, y)))
        return pixels

    def putdata(self, data: [(int,) * 4]):
        '''Copy data to virtual pixels.

        data is a list of colors which will be assgined row-wise to the virtual
        pixels. As many colors are assigned as poassible. That, until either the
        list of the virtual pixels runs out.

        Arguments:
        self: automatic object reference.
        data: list of colors.

        Returns:
        None.
        '''
        # Find out the number of colors to assign.
        xres, yres = self.size
        num_colors = min(len(data), xres * yres)
        # Assign colors to virtual pixels.
        for i in range(num_colors):
            y, x = divmod(i, xres)
            self.putpixel((x, y), data[i])

    def fill(self, color: (int,) * 4):
        '''Set every virtual pixel to color.

        Arguments:
        self: automatic object reference.
        color: the color to fill.

        Returns:
        None.
        '''
        self.putdata([color] * self.size[0] * self.size[1])

    def open(fname: str) -> 'MyImage':
        '''Returns an instance loaded from an image file.

        All common image formats are supported. Note that this is a class
        method, not an instance method.

        Arguments:
        fname: path to the image file

        Returns:
        An instance loaded from the image file.
        '''
        # Use PIL to read the image and copy its data to a newly created
        # instance. There are no gridlines in the instance and virtual pixels
        # are the same size as screen pixels.
        img: Image = Image.open(fname)
        myimg = MyImage(img.size, 0, 1, img.mode)
        myimg.putdata(img.getdata())
        return myimg


def test_image():
    '''Test MyImage.

    Write a sample iamge. Copy its data to another image. Display each image.
    '''
    # Create first image.
    xres, yres = 4, 3
    grid_width = 20
    pixel_size = 100
    mode = 'RGBA'
    img = MyImage((xres, yres), grid_width, pixel_size, mode)
    # Fill image pixels: black at origin, increasing red in x-direction and
    # increasing green in y- direction.
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            img.putpixel((x, y), (255 * x // xres, 255 * y // yres, 0, 255))
    # Create new image with same number of pixels but different resolution. Copy data to it.
    img1 = MyImage((yres, xres), grid_width, pixel_size, mode)
    img1.putdata(img.getdata())
    # Display the images.
    img.show()
    img1.show()


if __name__ == '__main__':
    test_image()
