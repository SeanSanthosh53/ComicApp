def change_page(link, change):
	if link.split('/?s=')[0][-1] == 'o':
		page = 1
	else:
		page = int(link.split('/?s=')[0].split('/')[-1])
	
	q = link.split('/?s=')[1]
	if change == 'add':
		return page + 1, f'https://getcomics.info/page/{page + 1}/?s={q}'
	elif change == 'subtract' and page != 1:
		if page == 2:
			return page - 1, 'https://getcomics.info/?s='+q
		else:
			return page - 1, f'https://getcomics.info/page/{page - 1}/?s={q}'
	elif page == 1:
		return page, None
		
