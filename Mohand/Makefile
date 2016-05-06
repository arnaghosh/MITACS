all: tracker

tracker: tracker.cpp
	g++ -g $^ -o $@ -Wall `pkg-config opencv --cflags --libs`

