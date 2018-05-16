from requests import get
from PIL import Image
from io import BytesIO
import argparse

parser = argparse.ArgumentParser(description='Downloads a Youtube video thumbnail.')
parser.add_argument('url', help='A Youtube video URL.')
parser.add_argument('-file', help="A downloaded file name, minus the extension. Defaults to 'thumbnail'.jpg.", default='thumbnail')
url = parser.parse_args().url.strip(' /')
if 'youtu.be' in url:
    id = url.rsplit('youtu.be/')[-1]
else:
    id = url.rsplit('watch?v=')[-1]
response = get('http://img.youtube.com/vi/' + id + '/maxresdefault.jpg')
image = Image.open(BytesIO(response.content))
filename = parser.parse_args().file + '.jpg'
fp = open(filename, 'w')
image.save(fp)
