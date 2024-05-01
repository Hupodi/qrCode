import numpy as np
import png

png.from_array([[255, 0, 0, 255], [0, 255, 255, 0]], "L").save("small_smiley.png")

#    So an RGB image that is 16 pixels high and 8 wide will
#     occupy a 2-dimensional array that is 16x24
#     (each row will be 8*3 = 24 sample values).
#
#     *mode* is a string that specifies the image colour format in a
#     PIL-style mode.  It can be:
#
#     ``'L'``
#       greyscale (1 channel)
#     ``'LA'``
#       greyscale with alpha (2 channel)
#     ``'RGB'``
#       colour image (3 channel)
#     ``'RGBA'``
#       colour image with alpha (4 channel)

white = 255
black = 0
png.from_array([[white] * 100] * 100 + [[black] * 100] * 50, mode="L").save("test.png")

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255] * 3
black = [0] * 3
png.from_array(
    np.array(
        [red * 100] * 50
        + [green * 100] * 50
        + [blue * 100] * 50
        + [white * 100] * 50
        + [black * 100] * 50
    ),
    mode="RGB",
).save("test.png")
