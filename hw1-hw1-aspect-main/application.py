import math
from api import *
from myimage import MyImage

def circle(radius: int, iterations: int) -> 'MyImage':
    '''Creates a image based on the iterations and radius that show a circle being iteratively 
       refined into a greater number of points, giving the illusion of smoothness.

    Arguments:
    radius: the radius of each circle.
    iterations: the number of repetitions, this is also the number of circles going to be contained in the output.

    Returns:
    A MyImage instance containing the circles side by side.
    '''

    # The width of the image depends on how many circles we want, so we can fit them side to side.
    width = radius*(iterations+1)+1

    # The circles will be created right at the beginning of the image, and then later be shifted to be shown side by side.
    origin = (radius, radius)

    img = MyImage((width*2, radius*2+1), 1, 1, 'RGBA')

    # We set the original 4 points so that at 0 iterations we still get a diamond. We will use it to store all points after each iteration.
    points = [[(origin[0]-radius, origin[1]), (origin[0], origin[1]-radius), (origin[0]+radius, origin[1]), (origin[0], origin[1]+radius), (origin[0]-radius, origin[1])]]

    # This will contain double the points after each iteration.
    newpoints = []

    for j in range(iterations):

        newpoints = []

        # To calculate the new smoother circle, we only need the last set of circle points created.
        for i in range(len(points[-1])):

            if i < len(points[-1])-1:

                # We need a point and the next point to create a third point.
                # A helper function is used to keep the code readable.

                newpoints.append([i for i in circle_helper(points[-1][i], points[-1][i+1], origin, radius)])

        # Although we reset our newpoints, we store them in points.
        points.append(([o for x in newpoints for o in x]))

    lst = []
    colors = [(255, 255, 255, 255) for i in range(len(points[-1]))]
    count = 0
    
    # We need to now shift each of the circles to the right by a distance of the diameter of the circle.
    for i in points:
        lst = []
        for j in i:
            lst.append((j[0]+(2*radius*count), j[1]))
        draw_polygon_dda(img, lst, colors)
        count += 1

    return img



def circle_helper(point1: (int, int), point2: (int, int), origin: (int, int), radius: int):
    '''Given 2 points, it determines a third that is in line with a circle.

    Arguments:
    point1: The first point.
    point2: The second point.
    origin: origin of the circle that point1 and point2 use.
    radius: radius of the circle that point1 and point2 use.

    Returns:
    A list of 3 points.
    '''

    # A list which is returned at the end, containing 3 output points given 2 input points. The first and last elements are the inputs.
    newpoints = [point1]

    # These are the coordinates of the midpoint between point1 and point2.
    newpointx = (point1[0] + point2[0]) / 2
    newpointy = (point1[1] + point2[1]) / 2

    # We create a vector from the point to the origin using point-point subtraction.
    vector = [newpointx - origin[0], newpointy - origin[1]]

    # We need to scale the vector to fit in line with this circle.
    # We can do this by dividing the radius by the magnitude of the vector. This gives us how much bigger or smaller the vector is from the radius.
    scalar = radius / ((vector[0]**2 + vector[1]**2)**(1/2))

    # We multiply this value to get the ideal sized vector.
    vector[0] *= scalar
    vector[1] *= scalar

    # The point where the line should be is if we fix this scaled vector from the origin.
    newpoints.append((origin[0]+int(vector[0]), origin[1]+int(vector[1])))
    newpoints.append(point2)

    return newpoints


#############################################################################################################################################################################################


def draw_sierpinski_fill(img: MyImage, x: int, y: int, l: int):
    '''It draws a filled polygon based on the coordinate received.

    Arguments:
    img: A MyImage instance upon which the image is created.
    x: The x coordinate of the left most vertex of a triangle.
    y: The y coordinate of the left most vertex of a triangle.
    l: The length of the triangle.

    Returns:
    None.
    '''

    # This code determines the points of the triangle to be filled, given the bottom left coordinate.
    x1 = (x, y)
    x2 = (x+(l//2),  int(y-math.sin(math.pi/3)*l))
    x3 = (x+l, y)

    draw_polygon(img, (x1, x2, x3), ([(255, 255, 255, 255) for i in range(len((x1,x2,x3)))]), True)



def recurse_sierpinski(img: MyImage, x: int, y: int, l: int, rec_count: int):
    '''Main recursion happens in this function.

    Arguments:
    img: A MyImage instance upon which the image is created.
    x: The x coordinate of the left most vertex of a triangle.
    y: The y coordinate of the left most vertex of a triangle.
    l: The length of the triangle.
    rec_count: recursion depth/count, it is the same as 'iterations' passed by the user.

    Returns:
    None.
    '''

    # Base Case.
    if rec_count == 0:

        draw_sierpinski_fill(img, x, y, l)

    else:

        # We want to display the triangle, then shift the x coordinate only, and display shrunken 3 more triangles.
        draw_sierpinski_fill(img, x, y, l)

        # 340 is the arbritary length chosen in the parent function, and it stays the same each iteration.
        # We recurse while reducing the recursion depth, and each triangle needs to be placed in an order, all having half the length as the previous one.

        # The first triangle is the same x and y coordinate.
        recurse_sierpinski(img, x+340, y, l//2, rec_count-1)

        # The second triangle is the uppermost one, and since y coordinate is at our bottom left triangle, we need to 
        # subtract the height of an equilateral triangle, to get the position of the uppermost sierpinski triangle.
        recurse_sierpinski(img, x + (l//4)+340, y - int(math.sin(math.pi/3)*(l/2)), l//2, rec_count-1)

        # The third triangle lays next to the first, just shifted more towards the right, by a factor of length/2.
        recurse_sierpinski(img, x + (l//2)+340, y, l//2, rec_count-1)
        


def sierpinski(iterations: int) -> 'MyImage':
    '''Is the main function that holds the image and sets the dimensions.

    Arguments:
    iterations: the recursion depth to be chosen.

    Returns:
    A MyImage instance that contains all recursion levels of the sierpinski triangle side by side.
    '''

    # 170 is based on the arbritary length chosen, 340.
    width = 170*(iterations+1)+1
    img = MyImage((width*2, 301), 1, 1, 'RGBA')

    # This provides the starting point, 0 for x axis, 300 for y axis (as the leftmost point on the triangle).
    recurse_sierpinski(img, 0, 300, 340, iterations)

    return img


if __name__ == '__main__':

    img = circle(100, 6)
    img.show()

    img = sierpinski(9)
    img.show()
