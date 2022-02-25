from myimage import MyImage

# 1


def draw_line_dda(img: MyImage, start: (int, int), end: (int, int)):
    ''' 
    Draws a line between two points provided

    Arguments:
    start: start coordinate of the line to be drawn
    end:   end coordinate of the line to be drawn

    Returns:
    None.

    '''

    x0 = start[0]
    y0 = start[1]
    x1 = end[0]
    y1 = end[1]

    # change in coordinates
    dx = x1 - x0
    dy = y1 - y0
    xinc = 0
    yinc = 0

    # calculates steps required for generating pixels
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    # increment in x & y for each step
    if steps != 0:
        xinc = dx / steps
        yinc = dy / steps

    x = x0
    y = y0

    # puts pixel for each step
    for i in range(steps + 1):
        # white color for start and end pt
        if i == 0 or i == steps:
            color = (255, 255, 255, 0)
        else:
            color = (27, 163, 156, 180)
        img.putpixel((round(x), round(y)), color)
        # incrementing x and y coordinates
        x += xinc
        y += yinc


# 2
def draw_line(img: MyImage, p_start: (int, int), p_end: (int, int), c_start: (int,) * 4, c_end: (int,) * 4) -> [((int, int), (int, int, int, int))]:
    ''' 
    Draws a line between two points with a color gradient 

    Arguments:
    p_start: start coordinate of the line to be drawn
    p_end:   end coordinate of the line to be drawn
    c_start: start pixel color of the line to be drawn
    c_end:   end pixel color of the line to be drawn

    Returns:
    A list of coordinates and color of each line pixel
    '''

    dictt = dict()
    pixelList = []
    x0 = p_start[0]
    y0 = p_start[1]
    x1 = p_end[0]
    y1 = p_end[1]

    # rgb & alpha being assigned for start and end point
    r0 = c_start[0]
    r1 = c_end[0]
    g0 = c_start[1]
    g1 = c_end[1]
    b0 = c_start[2]
    b1 = c_end[2]
    t0 = c_start[3]
    t1 = c_end[3]

    # change in coordinates
    dx = x1 - x0
    dy = y1 - y0
    dr = r1 - r0
    dg = g1 - g0
    db = b1 - b0
    dt = t1 - t0

    # initialising - if putting a single point, no increments required
    xinc = 0
    yinc = 0
    rinc = 0
    ginc = 0
    binc = 0
    tinc = 0

    # calculating steps required for generating pixels
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    # increment in x, y & rgba values for each step
    if steps != 0:
        xinc = dx / steps
        yinc = dy / steps
        rinc = dr / steps
        ginc = dg / steps
        binc = db / steps
        tinc = dt / steps

    x = x0
    y = y0
    r = r0
    g = g0
    b = b0
    t = t0

    # puts pixel and color for each step
    steps = int(steps)
    for i in range(steps + 1):
        if i == 0:
            color = c_start
        elif i == steps:
            color = c_end
        else:
            color = (round(r), round(g), round(b), round(t))

        coordinate = (round(x), round(y))
        img.putpixel(coordinate, color)

        # stores coordinate and color of each line pixel
        pixelList.append((coordinate, color))

        # increments x,y & rgba values
        x += xinc
        y += yinc
        r += rinc
        g += ginc
        b += binc
        t += tinc

    return pixelList


# 3
def draw_polygon_dda(img: MyImage, points: ((int, int)), colors: ((int, int, int, int))):
    ''' 
    Draws a polygon by drawing lines between vertices. For each y coordinate of boundary drawn, stores x coordinates and colors in a dictionary.

    Arguments:
    points: vertices of polygons
    colors: colors of vertices in same order

    Returns:
    A dictionary of the form: {ycoordinate: [(xcoordinate, color)]}

    '''
    number_of_points = len(points)
    dictt = dict()
    for i in range(number_of_points):
        # if only a point to be drawn
        if number_of_points == 1:
            img.putpixel(points[0], colors[0])
            dictt[points[0][1]] = [(points[0][0], colors[0])]

        # connects last vertex with the first vertex - closes the polygon and stores x coordinates and colors in a dict
        elif i == number_of_points-1 and number_of_points != 1:
            pixelList = draw_line(
                img, points[i], points[0], colors[i], colors[0])
            # adding coordinates and colors of boundary pixels to a dictionary with y coordinates as keys - dict[y] = [(x, color)]
            for tupl in pixelList:
                if tupl[0][1] in dictt:
                    dictt[tupl[0][1]].append((tupl[0][0], tupl[1]))
                else:
                    dictt[tupl[0][1]] = [(tupl[0][0], tupl[1])]

        # connects one vertex with the next successive vertex and stores x coordinates and colors in a dict
        else:
            pixelList = draw_line(
                img, points[i], points[i+1], colors[i], colors[i+1])
            for tupl in pixelList:
                if tupl[0][1] in dictt:
                    dictt[tupl[0][1]].append((tupl[0][0], tupl[1]))
                else:
                    dictt[tupl[0][1]] = [(tupl[0][0], tupl[1])]

    # sorts x coordinates for each y coordinate in ascending order
    for key, value in dictt.items():
        valuee = sorted(value, key=lambda x: x[0])
        dictt[key] = valuee

    return dictt


# 4
def draw_polygon(img: MyImage, points: ((int, int)), colors: ((int, int, int, int)), bools: bool = True):
    ''' 
    Draws a polygon by calling draw_polygon_dda(). Next, it fills by iterating over scanlines and drawing a horizontal line between successive pair of points in a particular line.

    Arguments:
    points: vertices of polygons
    colors: colors of vertices in same order
    bools:  optional boolean variable to fill the drawn polygon or not

    Returns:
    None.

    '''
    number_of_points = len(points)
    # no fill required
    if bools == False:
        draw_polygon_dda(img, points, colors)

    else:
        # with 2 points no fill required
        if number_of_points <= 2:
            draw_polygon_dda(img, points, colors)

        else:
            # iterates over scanlines(keys in dict storing y coordinates), and then draws lines between successive points
            dictt = draw_polygon_dda(img, points, colors)
            for key, valuelist in dictt.items():
                for i in range(len(valuelist)):
                    if (i != len(valuelist) - 1):
                        p_start = (valuelist[i][0], key)
                        p_end = (valuelist[i + 1][0], key)
                        c_start = valuelist[i][1]
                        c_end = valuelist[i + 1][1]
                        draw_line(img, p_start, p_end, c_start, c_end)


def colour_black(img: MyImage):
    ''' colors the image black'''
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            img.putpixel((x, y), (0, 0, 0, 255))


if __name__ == '__main__':

    ''' 1'''
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    draw_line_dda(img, (3, 8), (18, 2))
    img.show()

    ''' 2'''
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    pixelList = draw_line(img, (3, 8), (18, 2),
                          (255, 0, 0, 255), (0, 255, 0, 255))
    print("Pixel List", pixelList)
    img.show()

    '''3'''
    # -- triangle --
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    points = ((1, 8), (10, 1), (18, 8))
    colors = ((255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255))
    dictt = draw_polygon_dda(img, points, colors)
    img.show()
    # -- rectangle --
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    points = ((1, 9), (1, 1), (18, 1), (18, 9))
    colors = ((255, 0, 0, 255), (0, 255, 0, 255),
              (0, 0, 255, 255), (255, 255, 255, 255))
    draw_polygon_dda(img, points, colors)
    img.show()
    # -- n = 1 --
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    points = ((1, 9),)
    colors = ((255, 0, 0, 255),)
    draw_polygon_dda(img, points, colors)
    img.show()

    '''4'''
    # -- triangle --
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    points = ((1, 8), (10, 1), (18, 8))
    colors = ((255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255))
    draw_polygon(img, points, colors, True)
    img.show()
    # -- rectangle --
    img = MyImage((20, 10), 20, 100, 'RGBA')
    colour_black(img)
    points = ((1, 9), (1, 1), (18, 1), (18, 9))
    colors = ((255, 0, 0, 255), (0, 255, 0, 255),
              (0, 0, 255, 255), (255, 255, 255, 255))
    draw_polygon(img, points, colors, True)
    img.show()
