import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import argparse

def is_valid(url):
	""
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
	"""
	Returns all image URLs on a single `url`
	"""
	soup = bs(requests.get(url).content, "html.parser")

	urls = []
	for img in tqdm(soup.find_all("img"), "Extracting images"):
		img_url = img.attrs.get("src")
		if not img_url:
			# if img does not contain src attribute, just skip
				continue
		
		
		
		img_url = urljoin(url, img_url)
		try:
			pos = img_url.index("?")
			img_url = img_url[:pos]
		except ValueError:
			pass

		# finally, if the url is valid
		if is_valid(img_url):
			urls.append(img_url)
	return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(256), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def main(url, path):
    
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(img, path)
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
	parser.add_argument('--url', dest='target_url', required=True)
	parser.add_argument('--download-folder', dest='download_folder', required=False)
	args = parser.parse_args()
	
	download_path = 'autodownloaded'
	if args.download_folder:
		download_path = args.download_folder	
	main(args.target_url,download_path)