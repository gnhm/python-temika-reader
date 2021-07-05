from pytmk import Movie
import struct
import numpy as np

mule_f = 'mule.movie'

new_file = 'new_movie.movie'

m = Movie(mule_f)
m.file.seek(0)

m.file.seek(0)
m.file.seek(m.movie_header_index + 64)

im = np.zeros((200, 500))
new_size_y, new_size_x = im.shape #Yes, the order is correct. y first, then x.
frames = [im]

#new_size_x = 200
#new_size_y = 200
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
		new_movie.write(m.file.read(m.length_header))
		s = tuple(frame.flatten())
		new_movie.write(struct.pack('>' + (length_data//2)*"H", *s))
		#new_movie.write(m.file.read(m.data_start_index - new_movie.tell()))
#m.length_data
