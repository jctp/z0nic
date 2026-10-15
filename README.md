# Z0nic

![](https://img.shields.io/badge/Python-3.14-green)
![](https://img.shields.io/badge/Status-Pre%20Alpha-red)

Toy Sega Master System emulator in Python, built to understand the Z80. Currently in an extremely early state; it can currently debug a limited set of Z80 opcodes.

**If you're looking for a functional SMS emulator, you are in the wrong place.**

### Is it fast?
I have no idea, it's nowhere close to being able to run a commercial game. I would strongly suspect that it won't be - Python is hardly the best environment for a CPU and given its purpose logging is cranked up to the uber-max by default.

### Is it complete?
Absolutely not.

### Is it vibe-coded?
No, this is a learning project so vibe-coding the whole thing would be pointless. I did use AI to help in that process.
    
I've used a hands-off LLM (i.e. not running in the IDE or with direct access to the code) to guide me on the Z80 in a teaching capacity, help me with the Zilog manual, help keep track of opcodes, and type some repetitive parts and where I got stuck translating opcodes into Python. Which, considering this is my first emulator, was more than a few times. Quite a lot of the opcode implementations themselves are currently LLM-generated; I want to look at them again once I'm more confident with the hardware (and emulation in general!), but this gets things rolling.

Long story short, I wrote the structure and flow, the LLM helped me with the opcodes and the VDP.

Update (15th Oct 2026): I had to cheat in one place. Un-implemented opcodes were causing a CPU desync bug. I have a handler to manage this, but it needs the stub for the missing opcode to be present. I had Claude handle making the stubs for approx. 170 missing opcodes because it's a repetitive, incredibly uninteresting task and my time to work on this is limited. Broke the rules, but they're my rules, and this is a hobby/educational project so I don't consider myself to be having fun wrong or learning wrong.

### What does it look like?
At the moment, its output is simply logging what the Z80 is doing, and looks like this:

```
DEBUG:main:1CE8:       10 [DJNZ e      ] ( 13) - B=03 C=18 jumped from 1CEB to 1CE8
DEBUG:main:1CE8:       10 [DJNZ e      ] ( 13) - B=02 C=18 jumped from 1CEB to 1CE8
DEBUG:main:1CE8:       10 [DJNZ e      ] ( 13) - B=01 C=18 jumped from 1CEB to 1CE8
DEBUG:main:1CEC:       10 [DJNZ e      ] (  8) - B=00 C=18 jumped from 1CEB to 1CEC
DEBUG:main:1C87:       C9 [RET         ] ( 10) - Returned to 1C87
DEBUG:main:1C8B: FD CB 86 [RES b,(IY+d)] ( 23) - Reset bit 0 at 0002
DEBUG:main:1C8F: FD CB 8E [RES b,(IY+d)] ( 23) - Reset bit 1 at 0002
DEBUG:main:05E2:       CD [CALL nn     ] ( 17) - Called 05E2, return address 1C92
DEBUG:main:05E5:       21 [LD rr,nn    ] ( 10) - Loaded D000 into 02
DEBUG:main:05EA:       01 [LD rr,nn    ] ( 10) - Loaded 00BD into 00
DEBUG:main:05EC:       3E [LD r,n      ] (  7) - Value E0 loaded to register 07
DEBUG:main:05ED:       12 [LD rr,A     ] (  7) - Loaded 0001 into D218
DEBUG:main:05EF:       12 [LD rr,A     ] (  7) - Loaded 0001 into D218
DEBUG:main:05F3: ED    B0 [LDIR        ] (3969) - Copied 189 bytes from D000 to D218
DEBUG:main:05F7: FD    36 [LD (IY+d),n ] ( 19) - Stored 40 to 000A (IY+10)
DEBUG:main:05F8:       AF [XOR A       ] (  4) - A cleared to 00
DEBUG:main:05FB:       32 [LD (nn),A   ] ( 13) - Stored A (00) at D2B4
DEBUG:main:1C92:       C9 [RET         ] ( 10) - Returned to 1C92
DEBUG:main:1287:       CD [CALL nn     ] ( 17) - Called 1287, return address 1C95
DEBUG:main:128F:       32 [LD (nn),A   ] ( 13) - Stored A (00) at D219
DEBUG:main:1293: FD CB 86 [RES b,(IY+d)] ( 23) - Reset bit 0 at 0000
DEBUG:main:031C:       CD [CALL nn     ] ( 17) - Called 031C, return address 1296
DEBUG:main:0320: FD CB 46 [BIT b,(IY+d)] ( 20) - Tested bit 0 of value F3 at 0000
DEBUG:main:1296:       C9 [RET         ] ( 10) - Returned to 1296
DEBUG:main:1299:       21 [LD rr,nn    ] ( 10) - Loaded 2000 into 02
DEBUG:main:129C:       11 [LD rr,nn    ] ( 10) - Loaded 0000 into 01
DEBUG:main:129E:       3E [LD r,n      ] (  7) - Value 09 loaded to register 07
DEBUG:main:0405:       CD [CALL nn     ] ( 17) - Called 0405, return address 12A1
DEBUG:main:0406:       F3 [DI          ] (  4) - Disabled interrupts
DEBUG:main:0407:       F5 [PUSH qq     ] ( 11) - Pushed 0914
DEBUG:main:040A:       FE [CP nn       ] (  7) - Compared 40 with A (09)
DEBUG:main:0414:       38 [JR C,e      ] ( 12) - C=1 jumped from 040B to 0414
DEBUG:main:IO WRITE port=BF value=09
DEBUG:main:0417:       D3 [OUT A       ] ( 11) - Wrote value 09 to BF
DEBUG:main:IO WRITE port=BF value=09
DEBUG:main:041C:       D3 [OUT A       ] ( 11) - Wrote value 09 to BF
```

In short, unless you can read the Matrix, you're not playing Sonic on this yet.

### How is it licenced?
It's MIT.