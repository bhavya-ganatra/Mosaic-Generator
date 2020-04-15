# Mosaic-Generator
It is Mosaic Generator using Opencv Python package.

## Getting Started
First of make sure that you have installed python 3 on your machine. Then download following python packages if you haven't these in your machine.

I have created two files one for mosaic generation and second for auto download images from website. Auto download script might not work on some url, but if you have already large dataset of images then you don't need this.

### Prerequisites
To get some idea of what is happening in code I strongly recommended that you have brief knowledge of python libraries like opencv, numpy and requests.

### Installing

What things you need to install the software and how to install them
1. numpy package
2. opencv package (cv2)

For auto download image script you need to download and install:
1. BeautifulSoup (bs4)
2. urllib
3. requests
4. tqdm

## mosaic_generator.py
Type following command in command prompt:
'''
python mosaic_generator.py -h
'''

You will get description like these:

'''
usage: mosaic_generator.py [-h] --target-image TARGET_IMAGE --input-folder
                           INPUT_FOLDER --grid-size GRID_SIZE GRID_SIZE
                           [--output-file OUTFILE]

Creates a photomosaic from input images

optional arguments:
  -h, --help            show this help message and exit
  --target-image TARGET_IMAGE
                        Input image on which we will perform operation and
                        make mosaic
  --input-folder INPUT_FOLDER
                        Input folder for small images
  --grid-size GRID_SIZE GRID_SIZE
                        Grid size in mosaic
  --output-file OUTFILE
                        Name of output file don't forget to use extension

'''

So, what you need is input folder which contains dataset of images and one input file.
Here to getting start with it first get height and width of image and divide it by 10 and
take this as your grid size. And then play with this parameter to get appropriate result.

Here. If you have very large image dataset or large images then you will need more memory and
maybe you'll need to wait a little more. To avoid this one techanique is that first resize all images 
down to let's say 128x128 or decrese your dataset.

### Example:
Type below line into your command prompt
'''
python mosaic_generator.py --target-image 'path for target image' --input-folder 'path for input folder' --grid-size 172 194 --output-file 'output file name +.png' 
'''

In above code don't use ''.

## auto_download_image.py
Type following line in commnd prompt
'''
python auto_download_image.py -h
'''


'''
usage: auto_download_image.py [-h] --url TARGET_URL
                              [--download-folder DOWNLOAD_FOLDER]

Creates a photomosaic from input images

optional arguments:
  -h, --help            show this help message and exit
  --url TARGET_URL      url of website
  --download-folder DOWNLOAD_FOLDER
                        download folder

'''

Script will download all images from given url

### Example:

'''
python  auto_download_image.py --url 'url' --download-folder 'path for download folder'
'''

## Resources:
There are many image dataset available, which you can download freely.
For example to build someone's FACE MOSAIC you can download celeba dataset from original site
[celebA dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) or from
[kaggle](https://www.kaggle.com/jessicali9530/celeba-dataset). I guarenteed that this will give amazing result even using 1000 images

To generate proper image you should have different coloured images.


## Acknowledgments
I have built this mosaic generator using refrence of
[Implementing Photomosaic](https://www.geeksforgeeks.org/implementing-photomosaics/)
where it was in PIL package instead of opencv

For autodownload image I have used 
[Download all images from google search](https://www.thepythoncode.com/article/download-web-page-images-python)
as refrence.


Feel free to ask doubts...




