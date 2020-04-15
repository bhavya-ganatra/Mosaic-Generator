import os, random, argparse 
import cv2
import imghdr 
import numpy as np

def getAverageRGB(image):
    """ 
    Given Image, return average value of color as (r, g, b) 
    """
    h,w,d = image.shape
    
    #get average
    return tuple(np.average(image.reshape((h*w,d)),axis=0))
    
def splitImage(image, size): 
    """ 
    Given Image and dims (rows, cols) returns an m*n list of Images  
    """
    H,W = image.shape[0],image.shape[1]
    n,m = size
    h,w = int(H/n), int(W/m)
    
    #img list
    imgs = []
    #generate list of dimensions
    for j in range(n):
        for i in range(m):
            imgs.append(image[ j*h:(j+1)*h , i*w:(i+1)*w ])
    return imgs

def getImages(imageDir): 
    """ 
    given a directory of images, return a list of Images 
    """
    files = os.listdir(imageDir)
    images = []
    filenames = []
    for file in files:
        filepath = os.path.abspath(os.path.join(imageDir,file))
        try:
        	imgType = imghdr.what(filepath)
        	if imgType:
            		filenames.append(filepath)
        except:
            print("Invalid image 1: %s" %(filepath,))
        
        try:
            im = cv2.imread(filepath)
            images.append(im)
        except:
            print("Invalid image: %s" %(filepath,))
        
    return images

def getBestMatchIndex(input_avg, avgs): 
    """ 
    return index of best Image match based on RGB value distance 
    """
    avg = input_avg
    index = 0
    min_index = 0
    min_dist = float('inf')
    
    for val in avgs:
        dist = ((val[0]-avg[0])*(val[0]-avg[0]) + (val[1]-avg[1])*(val[1]-avg[1]) + (val[2]-avg[2])*(val[2]-avg[2]))
        if dist < min_dist:
            min_dist = dist
            min_index = index
        index= index + 1
        
    return min_index

def createImageGrid(images, dims): 
    """ 
    Given a list of images and a grid size (m, n), create  
    a grid of images.  
    """
    n,m = dims
    #sanity check
    assert m*n == len(images)
    print("len of imgs:",len(images))

    # get max height and width of images 
    # ie, not assuming they are all equal 
    height = max([img.shape[0] for img in images])
    width = max([img.shape[1] for img in images])

    #creating output image
    grid_img = np.zeros((n*height,m*width,3),np.uint8)

    index=0
    count=0
    for j in range(n):
        for i in range(m): 
            try:
                grid_img[j*height:(j+1)*height , i*width:(i+1)*width] = images[index] 
            except Exception as e:
                print(e)
                count+=1
            index+=1
    print(count)
    return grid_img



def createPhotomosaic(target_image, input_images, grid_size,reuse_images=True): 
    """ 
    Creates photomosaic given target and input images. 
    """
    print('splitting image...')
    target_images = splitImage(target_image,grid_size)
    
    print('finding image matches..')    
    #for each target pick one image from input
    output_images = []
    
    count = 0
    batch_size = int(len(target_images)/10)
    
    avgs = []
    for img in input_images:
        avgs.append(getAverageRGB(img))
    print("**** done input_images")
    for img in target_images:
        avg = getAverageRGB(img) 
        match_index = getBestMatchIndex(avg, avgs)
        
        output_images.append(input_images[match_index])
        
        if count>0 and batch_size > 10 and count%batch_size==0:
            print('processed %d of %d...' %(count, len(target_images)))
        count+=1
        if not reuse_images: 
            input_images.remove(match_index)
            
    print('creating mosaic...') 
    
    mosaic_image = createImageGrid(output_images, grid_size)
    
    return mosaic_image


def main(): 
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    #add arguments
    parser.add_argument('--target-image', dest='target_image', required=True,
                        help='Input image on which we will perform operation and make mosaic')
    parser.add_argument('--input-folder', dest='input_folder', required=True,
                        help='Input folder for small images')
    parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True,
                        help='Grid size in mosaic')
    parser.add_argument('--output-file', dest='outfile', required=False,
                        help="Name of output file don't forget to use extension")
    
    args = parser.parse_args()
    
    ### INPUT ###
    target_image = cv2.imread(args.target_image)
    
    print('reading input folder...')
    input_images = getImages(args.input_folder)
    # check if any valid input images found
    if input_images == []:
        print('No input images found in %s. Exiting.' % (args.input_folder, ))
        exit()
        
    random.shuffle(input_images)
    
    #grid size
    grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))
    print("grid_Size",grid_size)
    output_filename = 'mosaic2.png'
    if args.outfile:
        output_filename = args.outfile
    
    reuse_images = True
    resize_input = True
    
    ### END INPUTS ###
    
    print('starting photomosaic creation...')
    # if images can't be reused, ensure m*n <= num_of_images
    if not reuse_images:
        if grid_size[0]*grid_size[1] > len(input_images):
            print('grid size less than number of images') 
            exit()
    
    if resize_input:
        print('resizing input images...')
        print('target image shape',target_image.shape[0], target_image.shape[1])
        print('grid size---------',grid_size[0],grid_size[1])
        d1 = int(target_image.shape[0]//grid_size[0])
        d2 = int(target_image.shape[1]//grid_size[1])
        dims = (d1,d2)
        
        print('max tile dimensions:',dims)
        resized_input =[]
        for img in input_images:
            img = cv2.resize(img,dims,interpolation=cv2.INTER_AREA)
            #print(img.shape)
            resized_input.append(img)
    mosaic_image = createPhotomosaic(target_image, resized_input, grid_size,reuse_images)
    #mosaic_image.save(output_filename, 'PNG')
    cv2.imwrite(output_filename,mosaic_image)    
    print("saved output to %s" % (output_filename,))
    print('done...')
        
if __name__ == '__main__':
    main()
