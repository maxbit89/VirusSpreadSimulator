import imageio
import pathlib
from datetime import datetime


def make_gif(image_directory: pathlib.Path, frames_per_second: float, **kwargs):
    """
    Makes a .gif which shows many images at a given frame rate.
    All images should be in order (don't know how this works) in the image directory

    Only tested with .png images but may work with others.

    :param image_directory:
    :type image_directory: pathlib.Path
    :param frames_per_second:
    :type frames_per_second: float
    :param kwargs: image_type='png' or other
    :return: nothing
    """
    assert isinstance(image_directory, pathlib.Path), "input must be a pathlib object"
    image_type = kwargs.get('type', 'png')

    timestampStr = datetime.now().strftime("%y%m%d_%H%M%S")
    gif_dir = image_directory.joinpath(timestampStr + "_GIF.gif")

    print('Started making GIF')
    print('Please wait... ')

    images = []
    for file_name in image_directory.glob('*.' + image_type):
        images.append(imageio.imread(image_directory.joinpath(file_name)))
    imageio.mimsave(gif_dir.as_posix(), images, fps=frames_per_second)

    print('Finished making GIF!')
    print('GIF can be found at: ' + gif_dir.as_posix())