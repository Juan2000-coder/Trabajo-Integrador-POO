# makefile written for gnu make
SRCDIR = ./src
BUILDDIR = ./build
INCLDIR = ./include/xmlrpc
CXX		= g++
CPPFLAGS	= -I$(INCLDIR)
DEBUG		= -g
OPTIMIZE	= -O2
GCCWARN		= -Wall
CXXFLAGS	= $(DEBUG) $(GCCWARN) $(OPTIMIZE)

LIB		= ./build/libXmlRpc.a
SYSTEMLIBS	= -lws2_32

LDLIBS		= $(LIB) $(SYSTEMLIBS)

SOURCES		= $(wildcard $(SRCDIR)/*cpp)
OBJECTS		= $(patsubst $(SRCDIR)/%.cpp, $(BUILDDIR)/%.o, $(SOURCES))
EXECUTABLE	= ./build/Cliente.exe

$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c $< -o $@


$(EXECUTABLE):	$(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDLIBS)


.PHONY: all clean

all:		$(OBJECTS)

clean:
	rm -f $(BUILDDIR)/*.o $(EXE)
