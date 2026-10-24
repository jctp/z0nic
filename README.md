# Z0nic

![](https://img.shields.io/badge/Python-3.14-green)
![](https://img.shields.io/badge/Status-Pre%20Alpha-red)

Toy Sega Master System emulator in Python, built to understand the Z80. Currently in an extremely early state; it can currently debug a limited set of Z80 opcodes.

**If you're looking for a functional SMS emulator, you are in the wrong place.**

### Is it fast?
I have no idea, it's nowhere close to being able to run a commercial game.

### Is it complete?
Absolutely not. In fact, it was getting messy enough that I ripped out the entire Z80 implementation to replace it with an object-oriented version with "micro-operation" helpers for building up opcode behaviour. This set back progress, but made life easier.

### Is it vibe-coded?
No, this is a learning project so vibe-coding the whole thing would be pointless. I did use AI to help teach me things; my only emulator before this is a CHIP-8 interpreter and a the infinitely patient "experienced teacher" model works for me.

Some pieces have more LLM assistance than others:
- CPU - Limited, advisory and repetitive filling-out - this was the main goal of the project, to understand the Z80 through implementing it in software. This is the most hand-made part.
- VDP - Much more LLM support as it is not something I had any familiarity in. The goal here was to learn from the AI.

This is an AI disclosure for the sake of an AI disclosure, but if you want my full opinion on using a LLM as a teacher in an educational project like this, [Trixter](https://trixter.oldskool.org/2026/08/23/i-resent-ai-disclosure-policies-but-heres-mine/) has it about right.

### What does it look like?
At the moment, its output is simply logging what the Z80 and VDP are doing. In short, unless you can read the Matrix, you're not playing Sonic on this yet.

### How is it licenced?
It's MIT.
