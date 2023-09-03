COMPILE_SRC=start.py

all:
	pyinstaller --onefile --hidden-import	fastapi --hidden-import	fastapi.middleware.cors --hidden-import	requests $(COMPILE_SRC)

clean:
	rm -r build dist *.spec *.log

format:
	black *.py

run:
	./dist/start
