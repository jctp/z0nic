# ED A2  INI
# ED AA  IND
# ED B2  INIR
# ED BA  INDR

# ED A3  OUTI
# ED AB  OUTD
# ED B3  OTIR
# ED BB  OTDR

def execute(self, opcode):

    match opcode:

        # INI
        case 0xA2:

            opcode_t_states = self.block_in(
                increment=1,
                repeat=False
            )

            self.log_opcode(
                opcode=opcode,
                asm="INI",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Input from port BC to memory at HL"
            )

            return opcode_t_states

        # IND
        case 0xAA:

            opcode_t_states = self.block_in(
                increment=-1,
                repeat=False
            )

            self.log_opcode(
                opcode=opcode,
                asm="IND",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Input from port BC to memory at HL"
            )

            return opcode_t_states

        # INIR
        case 0xB2:

            opcode_t_states = self.block_in(
                increment=1,
                repeat=True
            )

            self.log_opcode(
                opcode=opcode,
                asm="INIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Repeated input from port BC to memory at HL"
            )

            return opcode_t_states

        # INDR
        case 0xBA:

            opcode_t_states = self.block_in(
                increment=-1,
                repeat=True
            )

            self.log_opcode(
                opcode=opcode,
                asm="INDR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Repeated input from port BC to memory at HL"
            )

            return opcode_t_states

        # OUTI
        case 0xA3:

            opcode_t_states = self.block_out(
                increment=1,
                repeat=False
            )

            self.log_opcode(
                opcode=opcode,
                asm="OUTI",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Output from memory at HL to port BC"
            )

            return opcode_t_states

        # OUTD
        case 0xAB:

            opcode_t_states = self.block_out(
                increment=-1,
                repeat=False
            )

            self.log_opcode(
                opcode=opcode,
                asm="OUTD",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Output from memory at HL to port BC"
            )

            return opcode_t_states

        # OTIR
        case 0xB3:

            opcode_t_states = self.block_out(
                increment=1,
                repeat=True
            )

            self.log_opcode(
                opcode=opcode,
                asm="OTIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Repeated output from memory at HL to port BC"
            )

            return opcode_t_states

        # OTDR
        case 0xBB:

            opcode_t_states = self.block_out(
                increment=-1,
                repeat=True
            )

            self.log_opcode(
                opcode=opcode,
                asm="OTDR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Repeated output from memory at HL to port BC"
            )

            return opcode_t_states

    return None