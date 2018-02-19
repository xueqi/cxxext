#include <string>
#include <vector>
using namespace std;
class A {
public:
    char cmem;
    unsigned char ucmem;
    short shmem;
    unsigned short usmem;
    int imem;
    unsigned int uimem;
    long long llmem;
    long int limem;
    unsigned umem;
    unsigned long long ullmem;
    unsigned long int ulimem;
    float fmem;
    double dmem;
    vector<int> vimem;
    string smem;
    const char * cstrmem;
    char * cxmem;

public: 
    A();
    void func_a(int);
};
