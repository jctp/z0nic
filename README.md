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

When I switched to the OO paradigm, I had MAI stub out all ~700 opcodes according to the rules I set it. Once I'd set out the first hundred or so with the uOps, I had it fill in the other million almost identical opcodes. Could have orthoganalised, but wanted to keep it separate for each opcode. Using this opcode of an example of where the LLM was used:

```python
def _and_n_iy(self):
    self.A.set(self.alu_and(self.A.get(), self.ingest_next_byte()))
    return 15
```

The helpers were mine, implementing some of them was me, implementing the rest of the boring forest of very similar opcodes was the LLM. This is the kind of thing that LLMs excel at; keep your brain in charge, let the machine do the repetitive things.

### What does it look like?
At the moment, its output is simply logging what the Z80 and VDP are doing. In short, unless you can read the Matrix, you're not playing Sonic on this yet.

### How is it licenced?
It's MIT.
