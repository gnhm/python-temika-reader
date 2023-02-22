from pytmk import Movie
import struct
from itertools import chain

import matplotlib.pyplot as plt
import numpy as np

mule_f = "/home/gn299/code/python-temika-reader/mule.movie"


def write_frames_to_movie(new_file, frames):
    m = Movie(mule_f)

    first_frame = next(frames)
    plt.imshow(first_frame)
    (
        new_size_y,
        new_size_x,
    ) = first_frame.shape  # Yes, the order is correct. y first, then x.
    length_data = new_size_y * new_size_x * 2

    frames_g = chain((xx for xx in [first_frame]), frames)

    with open(new_file, "wb") as new_movie:
        new_movie.seek(0)
        m.file.seek(0)

        # Write the movie header
        new_movie.write(m.file.read(m.movie_header_index))

        for i, frame in enumerate(frames_g):
            m.file.seek(m.movie_header_index)

            new_movie.write(m.file.read(20))

            new_movie.write(struct.pack("I", length_data))
            m.file.seek(4, 1)

            new_movie.write(m.file.read(m.movie_header_index + 64 - m.file.tell()))
            new_movie.write(struct.pack("I", new_size_x))
            new_movie.write(struct.pack("I", new_size_y))
            m.file.seek(8, 1)

            new_movie.write(
                m.file.read(m.movie_header_index + m.length_header - m.file.tell())
            )  # Write the frame header

            s = tuple(frame.flatten())
            new_movie.write(struct.pack(">" + (length_data // 2) * "H", *s))
