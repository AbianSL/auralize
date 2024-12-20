BIN=auralize
FLAGS=`pkg-config --cflags --libs gtk4`

test: build
	./bin/auralize

build:
	mkdir -p bin
	gcc -o bin/${BIN} $(FLAGS) interface/*.c
