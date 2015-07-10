from PIL import Image
import sys


info = """
This module uses the Python Image Library (specifically, the Pillow fork
which is actually maintained) to extract RGBA values from an image and
write them out to a textfile as '\\n'-separated strings of ones and zeroes.

It's kind of janky in its image analysis, and so it probably works best
with black-and-white or at least greyscale images. For the three RGB
color values each pixel has, this module will sum their total and compare
that value to 765 (255 * 3). If the sum total of a pixels colors are less
than half of 765, it will be considered black, and written to the file
as a zero; if greater than 765/2. it's considered white and written
as a one.
"""


misuse = """
ERROR: imgarray takes exactly two arguments.

$: python imgarray /location/of/image /desired/location/of/textfile

"""


def make_array(reading_document, writing_document):
    print "Opening file..."

    img = Image.open(reading_document, 'r')

    print "Extracting image data..."

    pxvals = list(img.getdata())
    row = []
    row_count = 0

    print "Image height: {h}".format(h=img.height)
    print "Image width: {w}".format(w=img.width)
    print "Processing image..."

    with open(writing_document, 'a') as fh:
        for x in pxvals:
            if (x[0] + x[1] + x[2]) < (3 * 255):
                px = b'0'
            else:
                px = b'1'

            row.append(px)

            if len(row) == img.width:
                row_count += 1
                smush_row = ''.join(row)

                if row_count % 100 == 0:
                    print "Writing row {r}".format(r=row_count)

                fh.write(smush_row + '\n')
                row = []

    print "Process completed. "
    print "Wrote {rc} rows to {wd}.".format(rc=row_count, wd=writing_document)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print info
    elif len(sys.argv) != 3:
        print misuse
    else:
        make_array(sys.argv[1], sys.argv[2])
