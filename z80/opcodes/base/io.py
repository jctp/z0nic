# DB      IN
# D3      OUT


def execute(self, opcode):

    match opcode:
        # IN A, (n)
        # Loads one byte from the data bus at port n into the accumulator a
        case 0xDB:
            opcode_t_states = 11

            # -----
            # Opcode logic:
            # Put contents of IO address port_number into a
            port_number = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            self.a = self.io.read(port_number)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="IN A",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Read value {self.a:02x} from {port_number:02X}",
                implemented=True,
            )
            return opcode_t_states

        # OUT (n), A
        # Places byte from the accumulator onto the given address
        case 0xD3:
            opcode_t_states = 11  # TODO: Check correct

            # -----
            # Opcode logic:
            # Write contents of a to port_number
            port_number = self.memory.read8(self.pc)
            self.inc_pc(increment=1)
            self.io.write(port_number, self.a)
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="OUT A",
                prefix="",
                opcode_t_states=opcode_t_states,
                message=f"Wrote value {self.a:02X} to {port_number:02X}",
                implemented=True,
            )
            return opcode_t_states

    return None
