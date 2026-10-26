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
No and yes. Some parts (CPU, memory, cartridge) are handmade. Some parts have more AI assistance. Some parts (VDP) are completely AI-generated. This is the first emulator I’ve made more complex than the CHIP-8 and it’s been incredibly helpful as a teaching tool for what the right answers should look like. My next emulator, which will also be SMS, will be far more handcrafted using what I’ve learned here (and through documentation, other code etc). 

This isn’t an emulator really meant for public use. There are already a million far better SMS emulators out there. The only reason this repo is public is because there’s no real reason for it not to be. If you’re here to get all salty that I used AI to help me learn a new skill, please know in your heart that I don’t care.

### What does it look like?
At the moment, its output is simply logging what the Z80 and VDP are doing. In short, unless you can read the Matrix, you're not playing Sonic on this yet.

### How is it licenced?
It's MIT.
