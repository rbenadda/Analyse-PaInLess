SRCS = $(shell find . -name "*.cpp")

OBJS = $(addsuffix .o, $(basename $(SRCS)))

EXEC = painless

LIBS = -lmapleCOMSPS -L../mapleCOMSPS/build/release/lib/ \
       -lm4ri -L../mapleCOMSPS/m4ri-20140914/.libs \
       -lpthread -lz -lm -static

CXXFLAGS = -I../mapleCOMSPS -I../mapleCOMSPS/m4ri-20140914 \
           -D __STDC_LIMIT_MACROS -D __STDC_FORMAT_MACROS \
           -std=c++11 -O3 -fpermissive 

$(EXEC): $(OBJS)
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)

%.o: %.cpp
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(LIBS)

clean:
	rm -f $(OBJS) $(EXEC)
