// inspired by https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step4/babymetal/babymetal.cpp
// where the insert_shellcode.py tool is first needed

This is tricky;
C code simulation;
Must not be overwritten;

unsigned char buf[] = "Leave me be";

unsigned char buf[] =
"So not touch"
"This buf"
;

//right before
    unsigned char buf[] =
"\x91\x25\xee\x89\x9d\x85\xa1\x6d\x6d\x6d\x2c\x3c\x2c\x3d\x3f"
"\x91\x25\xee\x89\x9d\x85\xa1\x6d\x6d\x6d\x2c\x3c\x2c\x3d\x3f"
"\x91\x25\xee\x89\x9d\x85\xa1\x6d\x6d\x6d\x2c\x3c\x2c\x3d\x3f"
"\x91\x25\xee\x89\x9d\x85\xa1\x6d\x6d\x6d\x2c\x3c\x2c\x3d\x3f"
;
// right after


But the shellcode must be overwritten and extended.

unsigned char buf[] = "Leave me be";

unsigned char buf[] =
"So not touch"
"This buf"
;