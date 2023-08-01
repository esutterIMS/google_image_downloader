from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import os
from urllib.request import *
import time
import pandas as pd

NAMES_PATH = "C:/Users/usuario/Desktop/Image Search/google_image_downloader/Faltantes.xlsx"

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"

def get_header():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }
    return headers

def get_names(path_):
	df = pd.read_excel(path_, sheet_name='Hoja1')
	names = df['nombre'].tolist()
	return names

def main():
	
	ext = ['jpg', 'png', 'jpeg']

	searchtexts = get_names(NAMES_PATH)
	num_requested = 5

	headers = get_header()

	driver = webdriver.Chrome()

	for searchtext in searchtexts:

		searchtext = searchtext.replace(".", " ")
		searchtext = searchtext.replace("  ", " ")

		if not os.path.exists(download_path + searchtext.replace(" ", "_")):
			os.makedirs(download_path + searchtext.replace(" ", "_"))

		url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
		driver.get(url)

		img_count = 0
		downloaded_img_count = 0
		
		for i in range(num_requested):
			try:
				img_box = driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i + 1}]/a[1]/div[1]/img')
				img_box.click()

				time.sleep(2)
				img = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')

			except:
				continue

			img_count += 1
			img_url = img.get_attribute('src')
			img_url = img_url.replace("medium", "big")
			print(img_url)
			img_type = img_url.split(".")[-1]
			if img_type not in ext:
				img_type = 'png'
			try:
				req = Request(img_url, headers=headers)
				raw_img = urlopen(req).read()
				f = open(download_path+searchtext.replace(" ", "_")+"/"+str(downloaded_img_count)+"."+img_type, "wb")
				f.write(raw_img)
				f.close
				downloaded_img_count += 1
			except Exception as e:
				print ("Download failed: {}".format(e))
		print ("Total downloaded: {}/{}".format(downloaded_img_count,img_count))

	driver.quit()

if __name__ == "__main__":
	main()