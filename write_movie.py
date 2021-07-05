from pytmk import Movie
import struct

mule_f = 'mule.movie'

def write_frames_to_movie(new_file, frames):
	m = Movie(mule_f)
	m.file.seek(0)
	m.file.seek(m.movie_header_index + 64)

	new_size_y, new_size_x = frames[0].shape #Yes, the order is correct. y first, then x.
	length_data = new_size_y*new_size_x*2 

	with open(new_file, 'wb') as new_movie:
		new_movie.seek(0)
		m.file.seek(0)

		#Write length_data and before
		new_movie.write(m.file.read(m.movie_header_index + 20))
		new_movie.write(struct.pack('I', length_data))

		#Write sizes and before
		new_movie.write(m.file.read(m.movie_header_index + 64 - new_movie.tell()))
		new_movie.write(struct.pack('I', new_size_x))
		new_movie.write(struct.pack('I', new_size_y))

		#Write everything up to where data starts
		new_movie.write(m.file.read(m.data_start_index - new_movie.tell()))
		for frame in frames:
			if frame.shape != (new_size_y, new_size_x):
				raise Exception('Frames are of different dimensions!')
			if frame.dtype != 'uint16':
				frame = frame.astype('uint16')
			new_movie.write(m.file.read(m.length_header))
			s = tuple(frame.flatten())
			new_movie.write(struct.pack('>' + (length_data//2)*"H", *s))
