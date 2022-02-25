import random
from myimage import MyImage

def blow(path: str):
    '''Displays the original image, blows it up, displays the blown up version along with the filtered versions.

    Arguments:
    path: the file name passed as a string.

    Returns:
    None.
    '''
   
    img = MyImage.open(path)
    pixels = img.getdata()
    img.show()

    img1 = MyImage(img.size, 1, img.pixel_size*2 , img.mode)

    # We copy the old image to the new, blown up one
    img1.putdata(pixels)
    img1.show()

    # We only select the 'R' channel
    img1.putdata([(i[0], 0, 0, i[3]) for i in pixels])
    img1.show()

    # We only select the 'G' channel
    img1.putdata([(0, i[1], 0, i[3]) for i in pixels])
    img1.show()

    # We only select the 'B' channel
    img1.putdata([(0, 0, i[2], i[3]) for i in pixels])
    img1.show()

    # We change the mode of the image to CMYK, and change our calculation to accomodate this.
    img1.mode = 'CMYK'
    img1.putdata([(255-i[0], 255-i[1], 255-i[2], 255) for i in pixels])
    img1.show()


def resize(path: str):
    '''Displays the original image, resizes it and uses bilinear interpolation to determine 
    pixel colors around each mapped pixel.

    Arguments:
    path: the file name passed as a string.

    Returns:
    None.
    '''

    img = MyImage.open(path)
    img.show()
    
    # The resolution is doubled.
    img1 = MyImage((img.size[0]*2, img.size[1]*2), 1, img.pixel_size, img.mode)

    for i in range(img.size[0]):

        for j in range(img.size[1]):
            
            # We first color every other pixel using the original image, while leaving the surrounding pixels blank.
            img1.putpixel((i*2,j*2), (img.getpixel((i,j))))

            # This corresponds to 'R' from the image of this problem in the homework file.
            x = (i*2)+1
            y = (j*2)+1

            # The boundary pixels cannot be colored the same way.
            if x < img1.size[0]-1 and y < img1.size[1]-1:

                # Getting a, b, c, d from the original image.
                a = img.getpixel((i,j)) 
                b = img.getpixel((i, j+1))
                c = img.getpixel((i+1, j))
                d = img.getpixel((i+1, j+1))

                # Calculating p, t, q, s, r via bilinear interpolation.
                p = (int(0.5*(a[0]+b[0])), int(0.5*(a[1]+b[1])), int(0.5*(a[2]+b[2])), int(0.5*(a[3]+b[3])))
                t = (int(0.5*(c[0]+d[0])), int(0.5*(c[1]+d[1])), int(0.5*(c[2]+d[2])), int(0.5*(c[3]+d[3])))
                q = (int(0.5*(c[0]+a[0])), int(0.5*(c[1]+a[1])), int(0.5*(c[2]+a[2])), int(0.5*(c[3]+a[3])))
                s = (int(0.5*(b[0]+d[0])), int(0.5*(b[1]+d[1])), int(0.5*(b[2]+d[2])), int(0.5*(b[3]+d[3])))

                r = (int((a[0]+b[0]+c[0]+d[0]+p[0]+t[0]+q[0]+s[0])/8),
                     int((a[1]+b[1]+c[1]+d[1]+p[1]+t[1]+q[1]+s[1])/8),
                     int((a[2]+b[2]+c[2]+d[2]+p[2]+t[2]+q[2]+s[2])/8),
                     int((a[3]+b[3]+c[3]+d[3]+p[3]+t[3]+q[3]+s[3])/8))

                img1.putpixel((x, y-1), q)
                img1.putpixel((x, y+1), s)
                img1.putpixel((x-1, y), p)
                img1.putpixel((x+1, y), t)
                img1.putpixel((x,y), r)

            # If we are on the boundary, we have to use the pixel to the left of it for calculation, 
            # as well as using this for the pixel below / to the right of it.
            if j < img.size[1] and i == img.size[0]-1:

                p = img.getpixel((i,j))
                img1.putpixel((x,y), p)

                if j < img.size[1]-1:
                    img1.putpixel((x,y+1), p)

            if i <= img.size[0] and j == img.size[1]-1:
                p = img.getpixel((i,j))
                
                img1.putpixel((x,y), p)

                if i < img.size[0]-1:
                    img1.putpixel((x+1,y), p)

    img1.show()



def sierpinski(img: MyImage, iterations: int, p1: tuple, p2: tuple, p3: tuple):
    '''Displays the Sierpinski Triangle using the chaos game method.

    Arguments:
    img: An instance of MyImage that the triangle is constructed on.
    iterations: The number of iterations to repeat the chaos game for. A higher number gives a more dense sierpinski triangle.
    p1: The first imaginary vertex.
    p2: The second imaginary vertex.
    p3: The third imaginary vertex.

    Returns:
    None.
    '''

    # We can arbitrarily choose a point within the triangle to start at.
    current = list(p1)

    for i in range(iterations):

        moveto = ()
        
        # We choose a random value between 0 and 1 to determine which vertex to move towards.
        prob = random.random()

        if prob <= (1/3):
            moveto = p1
        elif prob <= (2/3):
            moveto = p2
        else:
            moveto = p3

        # We calculate the new coordinate / update the current position as per the rules of the chaos game, 
        # between the random vertex chosen, and the current position.

        # Rounding the value to an integer is necessary as we are going to color a discrete pixel.
        current[0] += int((moveto[0]-current[0])/2)
        current[1] += int((moveto[1]-current[1])/2)

        # Only 1 pixel is colored, and it is a shade of pink.
        img.putpixel((current[0], current[1]), (random.randint(220, 255), random.randint(0, 40), random.randint(120, 160), 255))

    img.show()





if __name__ == '__main__':
    blow('images/logo.png')
    resize('images/logo.png')

    img = MyImage((300, 300), 1, 1, 'RGBA')
    sierpinski(img, 50000, (0, 299), (149, 0), (299, 299))
