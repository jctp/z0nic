# LDI
# LDIR
# LDD
# LDDR

# CPIR
# CPDR

# NEG

# IN
# OUT

# RETN
# RETI


def execute(self):
    opcode = self.memory.read8(self.pc)
    self.inc_pc(increment=1)

    match opcode:
        # region Interrupt Mode

        # ED 40,48,50,58,60,68,78
        # IN r,(C)
        case 0x40 | 0x48 | 0x50 | 0x58 | 0x60 | 0x68 | 0x78:
            opcode_t_states = 12

            # -----
            # Opcode logic:
            register = (opcode >> 3) & 0x07

            value = self.io_read_bc()

            self.set_register(register, value)

            self.flag_s = bool(value & 0x80)
            self.flag_z = value == 0
            self.flag_h = False
            self.flag_pv = self.parity(value)
            self.flag_n = False
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="IN r,(C)",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=f"IO read {value:02X} from {(self.get_bc() & 0xFFFF):04X}",
                implemented=True,
            )

            return opcode_t_states

        # ED 41,49,51,59,61,69,79
        # OUT (C),r
        case 0x41 | 0x49 | 0x51 | 0x59 | 0x61 | 0x69 | 0x79:
            opcode_t_states = 12

            # -----
            # Opcode logic:
            register = (opcode >> 3) & 0x07
            value = self.get_register(register)
            self.io_write_bc(value)
            # -----
            self.log_opcode(
                opcode=opcode,
                asm="OUT (C), r",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=f"IO write {value:02X} to {register:04X}",
                implemented=True,
            )
            return opcode_t_states

        # ED 56
        # Set interrupt mode to 1
        case 0x56:
            opcode_t_states = 2

            # -----
            # Opcode logic:
            self.interrupt_mode = 1
            # -----

            self.log_opcode(
                opcode=opcode,
                asm="IM 1",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Interrupt mode set to 1",
                implemented=True,
            )
            return opcode_t_states

        # endregion
        # region 16-bit Direct Load/Store

        # ED 43      LD (nn),BC
        # ED 4B      LD BC,(nn)
        #
        # ED 53      LD (nn),DE
        # ED 5B      LD DE,(nn)
        #
        # ED 63      LD (nn),HL
        # ED 6B      LD HL,(nn)
        #
        # ED 73      LD (nn),SP
        # ED 7B      LD SP,(nn)
        # ED 16-bit direct load/store
        case 0x43 | 0x4B | 0x53 | 0x5B | 0x63 | 0x6B | 0x73 | 0x7B:
            opcode_t_states = 20

            # -----
            # Opcode logic:

            low = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            high = self.memory.read8(self.pc)
            self.inc_pc(increment=1)

            # Gets the 16-bit address from the two 8-bit bytes
            # Pushes the high byte 8 bits to the left and attaches the low byte to get 16
            address = (high << 8) | low

            if opcode in (0x4B, 0x5B, 0x6B, 0x7B):
                low = self.memory.read8(address)
                high = self.memory.read8(address + 1)

                value = (high << 8) | low

                match opcode:
                    case 0x4B:
                        self.set_register_pair(0, value)
                        asm = "LD BC,(nn)"

                    case 0x5B:
                        self.set_register_pair(1, value)
                        asm = "LD DE,(nn)"

                    case 0x6B:
                        self.set_register_pair(2, value)
                        asm = "LD HL,(nn)"

                    case 0x7B:
                        self.sp = value
                        asm = "LD SP,(nn)"

                message = f"Loaded {value:04X} from {address:04X}"

            else:
                match opcode:
                    case 0x43:
                        value = self.get_register_pair(0)
                        asm = "LD (nn),BC"

                    case 0x53:
                        value = self.get_register_pair(1)
                        asm = "LD (nn),DE"

                    case 0x63:
                        value = self.get_register_pair(2)
                        asm = "LD (nn),HL"

                    case 0x73:
                        value = self.sp
                        asm = "LD (nn),SP"

                self.memory.write8(
                    address,
                    value & 0xFF,
                )

                self.memory.write8(
                    address + 1,
                    (value >> 8) & 0xFF,
                )

                message = f"Stored {value:04X} to {address:04X}"

            # -----

            self.log_opcode(
                opcode=opcode,
                asm=asm,
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=message,
                implemented=True,
            )

            return opcode_t_states

        # endregion
        # region 16-bit Arithmetic

        # ED 42  SBC HL,BC
        # ED 52  SBC HL,DE
        # ED 62  SBC HL,HL
        # ED 72  SBC HL,SP

        # ED 4A  ADC HL,BC
        # ED 5A  ADC HL,DE
        # ED 6A  ADC HL,HL
        # ED 7A  ADC HL,SP
        # HL = HL - BC - Carry
        case 0x42 | 0x52 | 0x62 | 0x72 | 0x4A | 0x5A | 0x6A | 0x7A:
            opcode_t_states = 15

            # -----
            # Opcode logic:

            hl = self.get_register_pair(2)

            match opcode:
                case 0x42 | 0x4A:
                    rhs = self.get_register_pair(0)
                    rhs_name = "BC"

                case 0x52 | 0x5A:
                    rhs = self.get_register_pair(1)
                    rhs_name = "DE"

                case 0x62 | 0x6A:
                    rhs = self.get_register_pair(2)
                    rhs_name = "HL"

                case 0x72 | 0x7A:
                    rhs = self.sp
                    rhs_name = "SP"

            carry = int(self.flag_c)

            if opcode & 0x08:
                result = hl + rhs + carry

                asm = f"ADC HL,{rhs_name}"

                self.flag_h = ((hl & 0x0FFF) + (rhs & 0x0FFF) + carry) > 0x0FFF

                self.flag_pv = (~(hl ^ rhs) & (hl ^ result) & 0x8000) != 0

                self.flag_n = False

            else:
                result = hl - rhs - carry

                asm = f"SBC HL,{rhs_name}"

                self.flag_h = ((hl & 0x0FFF) - (rhs & 0x0FFF) - carry) < 0

                self.flag_pv = ((hl ^ rhs) & (hl ^ result) & 0x8000) != 0

                self.flag_n = True

            self.flag_s = bool(result & 0x8000)

            self.flag_z = (result & 0xFFFF) == 0

            self.flag_c = result > 0xFFFF if opcode & 0x08 else result < 0

            result &= 0xFFFF

            self.set_register_pair(2, result)

            # -----

            self.log_opcode(
                opcode=opcode,
                asm=asm,
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=(f"HL={result:04X} RHS={rhs:04X}"),
                implemented=True,
            )

            return opcode_t_states

        # endregion
        # region Output Block

        # OUTI
        # Byte at address HL is written to I/O port BC
        # B is decremented
        # HL is incremented
        case 0xA3:
            opcode_t_states = self.block_out(increment=1, repeat=False)

        # OUTD
        # Byte at address HL is written to I/O port BC
        # B is decremented
        # HL is decremented
        case 0xAB:
            opcode_t_states = self.block_out(increment=-1, repeat=False)

        # OTIR
        # Repeated OUTI until B becomes zero
        case 0xB3:
            opcode_t_states = self.block_out(increment=1, repeat=True)

        # OTDR
        # Repeated OUTD until B becomes zero
        case 0xBB:
            opcode_t_states = self.block_out(increment=-1, repeat=True)

        # endregion
        # region Block Transfer

        # ED A0
        # LDI
        case 0xA0:
            opcode_t_states = self.block_transfer_helper(increment=1, repeat=0)

            self.log_opcode(
                opcode=opcode,
                asm="LDI",
                prefix="A0",
                opcode_t_states=opcode_t_states,
                message=("LDI Block Transfer"),
                implemented=True,
            )
            return opcode_t_states

        # ED B0
        # LDIR
        case 0xB0:
            opcode_t_states = self.block_transfer_helper(increment=1, repeat=1)

            self.log_opcode(
                opcode=opcode,
                asm="LDIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=("LDIR Repeating Block Transfer"),
                implemented=True,
            )
            return opcode_t_states

        # ED A8
        # LDD
        case 0xA8:
            opcode_t_states = self.block_transfer_helper(increment=0, repeat=0)

            self.log_opcode(
                opcode=opcode,
                asm="LDD",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=("LDD Block Transfer"),
                implemented=True,
            )
            return opcode_t_states

        # ED B8
        # LDDR
        case 0xB8:
            opcode_t_states = self.block_transfer_helper(increment=0, repeat=1)

            self.log_opcode(
                opcode=opcode,
                asm="LDIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message=("LDDR Repeating Block Transfer"),
                implemented=True,
            )
            return opcode_t_states

        # endregion
        # region Block Compare

        # TODO: ED A1
        # CPI

        # TODO: ED B1
        # CPIR

        # TODO: ED A9
        # CPD

        # TODO: ED B9
        # CPDR

        # endregion

        # region Block I/O (Input)

        # INI
        case 0xA2:
            opcode_t_states = self.block_in(increment=1, repeat=False)

            self.log_opcode(
                opcode=opcode,
                asm="INI",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Input from port BC to memory at HL",
            )

            return opcode_t_states

        # IND
        case 0xAA:
            opcode_t_states = self.block_in(increment=-1, repeat=False)

            self.log_opcode(
                opcode=opcode,
                asm="IND",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Input from port BC to memory at HL",
            )

            return opcode_t_states

        # INIR
        case 0xB2:
            opcode_t_states = self.block_in(increment=1, repeat=True)

            self.log_opcode(
                opcode=opcode,
                asm="INIR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Repeated input from port BC to memory at HL",
            )

            return opcode_t_states

        # INDR
        case 0xBA:
            opcode_t_states = self.block_in(increment=-1, repeat=True)

            self.log_opcode(
                opcode=opcode,
                asm="INDR",
                prefix="ED",
                opcode_t_states=opcode_t_states,
                message="Repeated input from port BC to memory at HL",
            )

            return opcode_t_states

        # endregion
        # region Block I/O (Output)

        # Not implemented
        case _:
            self.opcode_not_implemented(f"ED {opcode:02X}", "Unknown mnemonic")

    return None
