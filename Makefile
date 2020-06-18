test_filesize = 3G
test_args = "noResume" # could also be "resume(1|2)", for testing resuming capability

install_path = /usr/local/bin

# this also needs to be modified inside tests.py
tmp_path = ~/.tmp

pyrCaller_extern: src/pyrCaller_extern.c
	$(CC) -std=c99 -fPIC -shared -o $@.so $?

clean:
	rm -rf src/__pycache__ pyrCaller_extern.so main.spec build dist

test: pyrCaller_extern
	echo "Just a heads up this will take around an hour"
	echo "Also it is recommended but not required for any other file up/down"
	echo "progress to be finished before running this test"
	echo "Press enter to continue:"
	read a
	mkdir -p $(tmp_path)/tfilemgr
	mkdir -p downloads
	echo "Generating temp $(test_filesize) file out of random data"
	head -c $(test_filesize) </dev/urandom> $(tmp_path)/tfilemgr/rand
	echo "Starting python program"
	# The reason we start the test in the makefile is to not use
	# system specific commands in the python program so the tests can be
	# easily modified for other systems
	cd src && python tests.py $(test_args)
	echo "Checking if files are the same"
	diff $(tmp_path)/tfilemgr/rand downloads/tfilemk_rand
	echo "Finished test"
	echo "Deleting temporary files"
	rm $(tmp_path)/tfilemgr/rand downloads/tfilemk_rand

install: pyrCaller_extern
	pyinstaller src/main.py --add-data /usr/lib/python3.8/site-packages/pyrogram/client/ext/mime.types:pyrogram/client/ext --add-binary pyrCaller_extern.so:. --onefile

	cp dist/main $(install_path)/tgFileManager

.SILENT: test