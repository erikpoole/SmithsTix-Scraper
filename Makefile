default:
	pyinstaller main.py --onefile
	mv ./dist/main ./scraper	
	# rm -r __pycache__
	rm -r dist
	rm -r build
	rm main.spec