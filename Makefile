BIN=auralize
FLAGS=`pkg-config --cflags --libs gtk4`

build:
	mkdir -p bin
	gcc -o bin/${BIN} $(FLAGS) interface/*.c
