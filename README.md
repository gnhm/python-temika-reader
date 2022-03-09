# python-temika-reader
A lightweight python class to read .movie files and do the basics.

## A quick how-to
First clone the repository
```
git clone git@github.com:gnhm/python-temika-reader.git
```
or, if this is complicated for you, download it.

If you want to add pytmk to your python environment, an easy way is to create a symbolic link to the repo
```
cd <path>/lib/python3.8/site-packages
ln -s <another-path>/python-temika-reader/pytmk
```

Next, import the `Movie` class and create an instance of it
```
from pytmk import Movie

m = Movie("/home/crsid/data/super_cool_experiment.movie")
```

Now you can use `m` in a variety of ways

`get_frame_header(int i)` gives you the Temika header information for the ith frame in the format of a dictionary.

```
m.get_frame_header(10)
```

```
{'avt_channel_balance': 31092,
 'avt_channel_balance_mode': 0,
 'brightness': 120,
 'brightness_mode': 2,
 'camera_type': 1,
 'color_coding': 357,
 'data_depth': 16,
 'exposure': 236,
 'exposure_mode': 1,
 'gain': 0,
 'gain_mode': 2,
 'gamma': 1024,
 'gamma_mode': 1,
 'guid': 49712223535706612,
 'image_bytes': 100352,
 'length_data': 100352,
 'length_header': 172,
 'magic': 1231906132,
 'model_id': 1,
 'movie_version': 1,
 'pix_num': 50176,
 'pixel_mode_code': 2,
 'pos_x': 368,
 'pos_y': 34,
 'shutter': 252,
 'shutter_mode': 2,
 'size_x': 224,
 'size_x_max': 1920,
 'size_y': 224,
 'size_y_max': 1200,
 'stride': 448,
 'temperature': 3167,
 'temperature_mode': 2,
 'timestamp': 1620385231858162,
 'total_bytes': 100352,
 'trigger_delay': 0,
 'trigger_delay_mode': 1,
 'trigger_mode': 4294967295,
 'vendor_id': 45213,
 'video_mode': 0}
```
`get_frame_header(int i)` gives you the Temika header information for the ith frame in the format of a dictionary.

To get the ith frame as a numpy array, use

```
m.get_frame(10)
```
You can then manipulate the frame, analyze it, save it as a `.tiff` or `.png` using `PIL`, or do whatever else you feel like!

A convenient method is `m.frames()`. This returns a generator for frames. It functions like the Python `range` function.

```
m.frames() #Generator for all frames in the movie
m.frames(100) #For the first 100 frames
m.frames(20, 100, 2) #For frames 20 to 100, in steps of 2
```

A few useful attributes are

```
m.filename
m.n_frames
m.header
```
```
'/home/crsid/data/super_cool_experiment.movie'
5000
'Temika header describing what I did.'
```


