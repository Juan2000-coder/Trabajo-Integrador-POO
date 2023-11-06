CXX = /c/msys64/mingw64/bin/g++
CXXFLAGS = -fdiagnostics-color=always -g -Wall -I./CLIENTE/include/xmlrpc
LDFLAGS = -lws2_32
SRC_DIR = ./CLIENTE/src
OBJ_DIR = ./CLIENTE/build
OUTPUT = ./CLIENTE/build/Cliente

# Lista de archivos fuente
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Generar nombres de archivos objeto
OBJS = $(SRCS:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

all: $(OUTPUT)

$(OUTPUT): $(OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(OUTPUT)

.PHONY: all clean
