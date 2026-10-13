# CD      CALL nn
# C4      CALL NZ

# CC      CALL Z

# C9      RET

# C0      RET NZ
# C8      RET Z


def execute(self, opcode):

    match opcode:

        # CALL nn
        # Push current PC onto stack and jump to nn
        case 0xCD:
            opcode_t_states = 17

            # -----
            # Opcode logic:
            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            high = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            destination = (high << 8) | low
            return_address = self.pc
            self.sp -= 1
            self.memory.write8(
                self.sp,
                (return_address >> 8) & 0xFF
            )
            self.sp -= 1
            self.memory.write8(
                self.sp,
                return_address & 0xFF
            )
            self.pc = destination
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="CALL nn",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Called {destination:04X}, return address {return_address:04X}",
                implemented=True,
            )

            return opcode_t_states
        
        # RET
        # Return to caller
        case 0xC9:

            opcode_t_states = 10

            # -----
            # Opcode logic:
            return_address = self.pop16()
            self.pc = return_address
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="RET",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Returned to {return_address:04X}",
                implemented=True,
            )

            return opcode_t_states

    return None
