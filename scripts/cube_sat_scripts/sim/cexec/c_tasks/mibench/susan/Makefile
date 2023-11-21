all: susan_corner_detector susan_edge_detector susan_smoothing

susan_corner_detector: susan_corner_detector.c Makefile
	gcc -static -O4 -g -o susan_corner_detector susan_corner_detector.c -lm

susan_edge_detector: susan_edge_detector.c Makefile
	gcc -static -O4 -g -o susan_edge_detector susan_edge_detector.c -lm

susan_smoothing: susan_smoothing.c Makefile
	gcc -static -O4 -g -o susan_smoothing susan_smoothing.c -lm

clean:
	rm -rf susan_corner_detector susan_edge_detector susan_smoothing output*
