from io import BytesIO
from PIL import Image
import os
import sys


def compress(image, not_compressed_dir, compressed_dir):
    im = Image.open(not_compressed_dir + image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    with open(compressed_dir + 'Compressed_' + image.split(".")[0] + '.jpg', 'wb') as file:
        file.write(im_io.getvalue())
    original_image_size = os.path.getsize(not_compressed_dir + image)
    compressed_image_size = os.path.getsize(compressed_dir + 'Compressed_' + image.split(".")[0] + '.jpg')
    print('Original Lena Size : ', original_image_size, '\nCompressed Lena Size : ', compressed_image_size,
          '\nCompression Percent : ', original_image_size / compressed_image_size * 100, '%')


if len(sys.argv) != 3:
    sys.exit(-1)
else:
    notCompressedDir = sys.argv[1]
    compressedDir = sys.argv[2]

file_list = os.listdir(notCompressedDir)
for file in file_list:
    compress(file, notCompressedDir, compressedDir)
