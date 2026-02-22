CC      := clang
TARGET  := rogue0
SRC     := src/main.c

$(TARGET): $(SRC)
	$(CC) $(SRC) -o $(TARGET) -lncurses && ./$(TARGET)

clean:
	rm -f $(TARGET)
