#include "utils.hpp"
#include "compressor.hpp"
#include "uarray.h"
#include <iostream>
#include <vector>
#include <cstring>
#include <math.h>
#include "abbrevs.h"
#include "malloc_count.h"
#include "stack_count.h"


using namespace std;
map<string, string> operations{
    {"-c", "compress"},
    {"-d", "decompress"},
    {"-e", "extract"}
};

void error(const char *msg) {
    cout << "\x1b[31m[ERROR]\x1b[0m " << msg << endl;
    exit(EXIT_FAILURE);
}

void isFileOpen(FILE * file, const char *msg) {
    if(file != NULL) return;
    error(msg);
}

int padding(i32 textSize, int coverage){
    if(textSize % coverage != 0){
        return coverage - (textSize % coverage);
    }
    return coverage;
}

void radixSort(const i32 *text, i32 nTuples, i32 *&tuples, i32 sigma, int coverage){
    bool newAllocation = false;
    i32 *tupleIndexTemp;
    i32 *bucket;

    if(nTuples >= sigma) {
        tupleIndexTemp = &tuples[nTuples];
        bucket = &tuples[nTuples*2];
    } else {
        tupleIndexTemp = (i32*)calloc(coverage*nTuples, sizeof(i32));
        bucket = (i32*)calloc(sigma, sizeof(i32));
    }

    for(int i=0, j=0; i < nTuples; i++, j+=coverage)tuples[i] = j;

    for(int d= coverage-1; d >=0; d--) {
        for(int i=0; i < sigma;i++)bucket[i]=0;//TODO
        for(int i=0; i < nTuples; i++) bucket[text[tuples[i] + d]+1]++; 
        for(int i=1; i < sigma; i++) bucket[i] += bucket[i-1];

        for(int i=0; i < nTuples; i++) {
            tupleIndexTemp[bucket[text[tuples[i] + d]]++] = tuples[i];
        }
        for(int i=0; i < nTuples; i++) tuples[i] = tupleIndexTemp[i];
    }

    if(newAllocation) {
        free(tupleIndexTemp);
        free(bucket);
    }
}

void createLexNames(const i32 *text, i32 *tuples, i32 *rank, i32 &qtyRules, long int nTuples, int coverage) {
    i32 name = 1;
    rank[tuples[0]/coverage] = name;
    for(i32 i=1; i < nTuples; i++) {
        bool equal = true;
        for(int j=0; j < coverage; j++){
            if(text[tuples[i-1]+j] != text[tuples[i]+j]){
                equal = false;
                break;
            }
        }
        if(equal) rank[tuples[i]/coverage] = name;
        else rank[tuples[i]/coverage] = ++name;
    }

    qtyRules = name;
}

void generateReport(char *fileName, double duration, void *base) {
    FILE *file = fopen(fileName, "a");
    isFileOpen(file, "Unable to open report to enter time and memory consumption information");
    long long int peak = malloc_count_peak();
    long long int stack = stack_count_usage(base);
    fprintf(file, "%lld|%lld|%5.15lf|", peak,stack,duration);
    fclose(file);
}