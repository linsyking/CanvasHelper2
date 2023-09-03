COMPILE_SRC=start.py

all:
	pyinstaller -F $(COMPILE_SRC)

clean:
	rm -r build dist *.spec *.log

format:
	black .

run:
	./dist/start
