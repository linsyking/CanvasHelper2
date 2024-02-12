START_SRC=start.py

all:
	pyinstaller -F $(START_SRC)

windows:
	wine pyinstaller -F $(START_SRC)

clean:
	rm -r build dist *.spec *.log

format:
	black .

run:
	./dist/start
