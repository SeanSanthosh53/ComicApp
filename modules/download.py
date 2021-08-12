import requests
from os import system
from urllib.parse import unquote


def download(url, filename):
	print('Request starts')
	response = requests.get(url, stream=True)
	total = response.headers.get('content-length')
	file = response.url.split('/')[-1]
	print(unquote(file))
	with open(filename, 'wb') as f:		
		if total is None:
			f.write(response.content)
		
		else:
			downloaded = 0
			total = int(total)
			for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
				downloaded += len(data)
				f.write(data)
				done = int(50*downloaded/total)
				s = '\r[{}{}]'.format('█' * done, '•' * (50-done))
				system('clear')
				print(s)
   
download(input("Link: "), f"/storage/emulated/0/#Comics/{input('File name: ')}.cbz")