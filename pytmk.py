import os
import struct
import numpy as np
import datetime

class Movie:
	def __init__(self, filename):
		self.filename = filename
		self.file = open(filename, 'r')

		self.read_movie_header()

		self.gap_between_frames = self.length_header + self.length_data #The periodicity of the data is length of data plus length of header
		self.data_start_index = self.length_header + self.movie_header_index  #fileHeader plus frameHeader... A little dumb

		self.file.seek(self.length_header)

		self.max_pixel_depth = 2**16 - 1

		self.n_frames = self.binary_n_frames()

	def read_movie_header(self):

		magic_word = 'TemI'

		def read(s):
			return struct.unpack(s, self.file.read(struct.calcsize(s)))[0]

		def find_magic():
			while True:
				buf = self.file.read(1)
				#Check if file has reached its end. If so, raise exception
				if not buf:
					raise Exception('Magic word not found!')
				else:
					if buf == magic_word[0]: #If read first letter of the magic_word...
						if self.file.read(len(magic_word) - 1) == magic_word[1:]: #Read the rest of the length of the word.
							movie_header_index = self.file.tell() - len(magic_word)
							self.file.seek(0)
							return movie_header_index 
						else:
							self.file.seek(-len(magic_word) + 1, 1)
	
		self.file.seek(0)

		self.movie_header_index = find_magic()

		self.header = self.file.read(self.movie_header_index)

		self.magic = struct.unpack('4s', self.file.read(4))[0]
		if self.magic != magic_word:
			raise Exception('Magic word not found!')
		self.movie_version = struct.unpack('I', self.file.read(4))[0]
		self.camera_type = struct.unpack('I', self.file.read(4))[0]

		pixel_mode_code = struct.unpack('I', self.file.read(4))[0]
		self.length_header = struct.unpack('I', self.file.read(4))[0]
		self.length_data = struct.unpack('I', self.file.read(4))[0]
		self.gap_between_frames = self.length_header + self.length_data #The periodicity of the data is length of data plus length of header
		self.data_start_index = self.length_header + self.movie_header_index  #fileHeader plus frameHeader... A little dumb

		if pixel_mode_code == 1:
			self.pixel_mode = 'MONO8'
		elif pixel_mode_code == 2:
			self.pixel_mode = 'MONO16BE'
		elif pixel_mode_code == 3:
			self.pixel_mode = 'MONO16LE'
		else:
			raise Exception('Invalid pixel mode: Must be 1 for MONO8, 2 for MONO16BE, and 3 for MONO16LE')

		if self.camera_type == 1:
			self.camera_name = 'IIDC'
#			self.length_header = struct.unpack('I', self.file.read(4))[0]
#			self.length_data = struct.unpack('I', self.file.read(4))[0]

			#64 
			self.gu_ID = struct.unpack('Q', self.file.read(8))[0] 
			self.vendor_ID = struct.unpack('I', self.file.read(4))[0]
			self.model_ID = struct.unpack('I', self.file.read(4))[0]

			#80
			self.video_more = struct.unpack('I', self.file.read(4))[0] 

			#84
			self.color_coding = struct.unpack('I', self.file.read(4))[0] 

			#88
			self.timestamp_us = struct.unpack('Q', self.file.read(8))[0] 

			#96
			self.size_x_max = struct.unpack('I', self.file.read(4))[0]
			self.size_y_max = struct.unpack('I', self.file.read(4))[0]
			self.size_x = struct.unpack('I', self.file.read(4))[0]
			self.size_y = struct.unpack('I', self.file.read(4))[0]
			self.position_x = struct.unpack('I', self.file.read(4))[0]
			self.position_y = struct.unpack('I', self.file.read(4))[0]
			
			#120
			self.pixnum = struct.unpack('I', self.file.read(4))[0] #Number of pixels
			self.stride = struct.unpack('I', self.file.read(4))[0] #Number of bytes per image line
			self.data_depth = struct.unpack('I', self.file.read(4))[0] #Number of bits per pixel
			self.image_bytes = struct.unpack('I', self.file.read(4))[0]
			self.total_bytes = struct.unpack('Q', self.file.read(8))[0]

			self.brightness_mode = struct.unpack('I', self.file.read(4))[0]
			self.brightness  = struct.unpack('I', self.file.read(4))[0]
			self.exposure_mode = struct.unpack('I', self.file.read(4))[0]
			self.exposure = struct.unpack('I', self.file.read(4))[0]
			self.gamma_mode = struct.unpack('I', self.file.read(4))[0]
			self.gamma = struct.unpack('I', self.file.read(4))[0]
			self.shutter_mode = struct.unpack('I', self.file.read(4))[0]
			self.shutter = struct.unpack('I', self.file.read(4))[0]
			self.gain_mode = struct.unpack('I', self.file.read(4))[0]
			self.gain = struct.unpack('I', self.file.read(4))[0]
			self.temperature_mode = struct.unpack('I', self.file.read(4))[0]
			self.temperature  = struct.unpack('I', self.file.read(4))[0]
			self.trigger_delay_mode = struct.unpack('I', self.file.read(4))[0]
			self.trigger_delay = struct.unpack('I', self.file.read(4))[0]
			self.trigger_mode = struct.unpack('I', self.file.read(4))[0]
			self.avt_channel_balance_mode = struct.unpack('I', self.file.read(4))[0]
			self.avt_channel_balance = struct.unpack('I', self.file.read(4))[0]


		elif self.camera_type == 2:
			self.camera_name = 'Andor'
			for attr, value in self.read_header(0).items():
				setattr(self, attr, value)

		elif self.camera_type == 3:
			self.camera_name = 'Ximea'
#			self.length_header = read('I')
#			self.length_data = read('I')
			self.mystery = read('100s')
			self.serial_number = read('I')
			self.timestamp_sec = read('Q')
			self.timestamp_nsec = read('Q')

			self.size_x_max = read('I')
			self.size_y_max = read('I')
			self.size_x = read('I')
			self.size_y = read('I')
			self.position_x = read('I')
			self.position_y = read('I')

			self.exposure = read('I')
			self.gain = read('f')
			self.downsampling = read('I')
			self.downsampling_type = read('I')
			self.bpc = read('I')
			self.lut = read('I')
			self.trigger = read('I')

			self.aeag = read('I')
			self.aeag_exposure_priority = read('f')
			self.aeag_exposure_max_limit = read('I')
			self.aeag_gain_max_limit = read('f')
			self.aeag_average_intensity = read('I')

			self.hdr = read('I')
			self.hdr_t1 = read('I')
			self.hdr_t2 = read('I')
			self.hdr_t3 = read('I')
			self.hdr_kneepoint1 = read('I')
			self.hdr_kneepoint2 = read('I')	
		else:
			raise Exception('Invalid camera type: Must be 1 for IIDC, 2 for Andor, and 3 for Ximea')

	def binary_n_frames(self):
		"""Finds number of frames using binary search"""
		def is_frame(i):
			self.file.seek(self.gap_between_frames*i)
			return len(self.file.read(self.gap_between_frames)) == self.gap_between_frames
		def is_last_frame(i):
			return is_frame(i) and not is_frame(i+1)

		l = 0
		r = 3000000
		mid = (r + l)/2

		while not is_last_frame(mid):
			if is_frame(mid):
				l = mid
			if not is_frame(mid):
				r = mid

			mid = (r+l)/2

		return mid + 1

	def local_folder(self):
		"""Return the name of the folder to save things in, and creates it if it does not exist"""
		name = os.path.splitext(self.filename)[0] + auxExt
		if not os.path.isdir(name):
			os.makedirs(name)
		return name

	def read_header(self, i):
		if self.camera_name == 'IIDC':
			#Time is in microseconds!
			struct_string = 6*"I" + "L" + 4*"I" + "L" + 10*"I" + "L" + 7*"II" + "IiI" 
			struct_labels = ['magic', 'movie_version', 'camera_type', 'pixel_mode_code', 'length_header', 'length_data', 'guid', 'vendor_id', 'model_id', 'video_mode', 'color_coding', 'timestamp', 'size_x_max', 'size_y_max', 'size_x', 'size_y', 'pos_x', 'pos_y', 'pix_num', 'stride', 'data_depth', 'image_bytes', 'total_bytes', 'brightness_mode', 'brightness', 'exposure_mode', 'exposure', 'gamma_mode', 'gamma', 'shutter_mode', 'shutter', 'gain_mode', 'gain', 'temperature_mode', 'temperature', 'trigger_delay_mode', 'trigger_delay', 'trigger_mode', 'avt_channel_balance_mode', 'avt_channel_balance']

		elif self.camera_name == 'Ximea':
			struct_string = 'IIIIII100sIQQIIIIIIIfIIIIIIfIfIIIIIII'
			struct_labels = ['magic', 'movie_version', 'camera_type', 'pixel_mode_code', 'length_header', 'length_data', 'mystery', 'serial_number', 'timestamp_sec', 'timestamp_nsec', 'size_x_max', 'size_y_max', 'size_x', 'size_y', 'position_x', 'position_y', 'exposure', 'gain', 'downsampling', 'downsampling_type', 'bpc', 'lut', 'trigger', 'aeag', 'aeag_exposure_priority', 'aeag_exposure_max_limit', 'aeag_gain_max_limit', 'aeag_average_intensity', 'hdr', 'hdr_t1', 'hdr_t2', 'hdr_t3', 'hdr_kneepoint1', 'hdr_kneepoint2']

		elif self.camera_name == 'Andor':
			struct_string = "6I" + "2L" + "8I" + "7I" + "f" + "6I"
			struct_labels = ['magic', 'movie_version', 'camera_type', 'pixel_mode_code', 'length_header', 'length_data', 'timestamp_sec', 'timestamp_nsec', 'size_x_max', 'size_y_max', 'x_start', 'x_end', 'y_start', 'y_end', 'x_bin', 'y_bin', 'ad_channel', 'amplifier', 'preamp_gain', 'em_gain', 'hs_speed', 'vs_speed', 'vs_amplitude', 'exposure', 'shutter', 'trigger', 'temperature', 'cooler', 'cooler_mode', 'fan']

		else:
			raise Exception('Camera {:s} is not supported.')

		self.file.seek(self.movie_header_index + self.gap_between_frames*i)
		header = struct.unpack(struct_string, self.file.read(self.length_header))
	
		header_dict = dict(zip(struct_labels, header))

		if self.camera_name == 'Andor':
			header_dict['size_x'] = header_dict['x_end'] - header_dict['x_start'] + 1
			header_dict['size_y'] = header_dict['y_end'] - header_dict['y_start'] + 1

		return header_dict

	def get_frame(self, i):
		"""Read the ith frame of data as an array of 16-bit quantities"""

		if i > self.n_frames - 1:
			return None

		self.file.seek(self.data_start_index + self.gap_between_frames*i) #Move to beginning of frame
		#Read the length of data with self.file.read. This is a string of length self.length_data.
		#Because of endianness, and convert it to an array of unsigned 16-bit integers ('H').
		#First argument of unpack is '>' to signify big-endian, then the format 	
		#Finally, reshape into a rectangle of the right dimensions

		#TODO This needs to take self.pixel_mode into account. This works for standard IIDC camera
		if self.pixel_mode == 'MONO16BE':
			return np.reshape( struct.unpack('>' + (self.length_data/2)*"H", self.file.read(self.length_data)), (self.size_y, self.size_x) ).astype('H')
		if self.pixel_mode == 'MONO16LE':
			return np.reshape( struct.unpack('<' + (self.length_data/2)*"H", self.file.read(self.length_data)), (self.size_y, self.size_x) ).astype('H')
		if self.pixel_mode == 'MONO8':
			return np.reshape( struct.unpack(self.length_data*"B", self.file.read(self.length_data)), (self.size_y, self.size_x)).astype("B")

	def frames(self, *args):
		"""Returns a generator of frames. Should work like range()"""
		iterable = False
		if len(args) == 0:
			start = 0
			stop = self.n_frames
			step = 1

		elif len(args) == 1:
			if hasattr(args[0], '__iter__'):
				iterable = True
			else:
				start = 0
				stop = args[0]
				step = 1

		elif len(args) == 2:
			start = args[0]
			stop = args[1]
			step = 1

		elif len(args) == 3:
			start = args[0]
			stop = args[1]
			step = args[2]

		elif len(args) > 3:
			raise TypeError

		if iterable:
			for i in args[0]:
				yield self.get_frame(i)

		else:
			for i in range(start, stop, step):
				yield self.get_frame(i)

	def destroy(self):
		self.file.close()
		self.file = None

	def frame_time(self, i, true_time = False):
		if self.camera_name == 'IIDC':
			time_delta = datetime.timedelta(0,0, self.read_header(i)['timestamp']) - datetime.timedelta(0,0, self.read_header(0)['timestamp'])
			total_seconds = time_delta.total_seconds()
			if true_time:
				return total_seconds
			hours = int(total_seconds) / (60*60)
			minutes = (int(total_seconds) % (60*60)) / (60)
			seconds = total_seconds % 60
			string = "Time = {:02d}:{:02d}:{:05.2f}".format(hours, minutes, seconds)
		elif self.camera_name == 'Ximea' or self.camera_name == 'Andor':
			seconds_elapsed = self.read_header(i)['timestamp_sec'] - self.read_header(0)['timestamp_sec']
			nanoseconds_elapsed = self.read_header(i)['timestamp_nsec'] - self.read_header(0)['timestamp_nsec']
			total_seconds= seconds_elapsed + nanoseconds_elapsed*(1E-9)
			if true_time:
				return total_seconds
			hours = int(total_seconds) / (60*60)
			minutes = (int(total_seconds) % (60*60)) / (60)
			seconds = total_seconds % 60
			string = "Time = {:02d}:{:02d}:{:05.3f}".format(hours, minutes, seconds)
			
		return string
