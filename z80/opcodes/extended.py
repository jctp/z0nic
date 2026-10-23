OPCODES = [
    {
        "opcode": "0x40",
        "mnemonic": "IN B,(C)",
        "description": "Input a byte from port C into B",
    },
    {"opcode": "0x41", "mnemonic": "OUT (C),B", "description": "Output B to port C"},
    {
        "opcode": "0x42",
        "mnemonic": "SBC HL,BC",
        "description": "Subtract BC from HL with carry",
    },
    {
        "opcode": "0x43",
        "mnemonic": "LD (nn),BC",
        "description": "Store BC at absolute address nn",
    },
    {"opcode": "0x44", "mnemonic": "NEG", "description": "Negate accumulator"},
    {
        "opcode": "0x45",
        "mnemonic": "RETN",
        "description": "Return from non-maskable interrupt",
    },
    {"opcode": "0x46", "mnemonic": "IM 0", "description": "Set interrupt mode 0"},
    {"opcode": "0x47", "mnemonic": "LD I,A", "description": "Load I with A"},
    {
        "opcode": "0x48",
        "mnemonic": "IN C,(C)",
        "description": "Input a byte from port C into C",
    },
    {"opcode": "0x49", "mnemonic": "OUT (C),C", "description": "Output C to port C"},
    {
        "opcode": "0x4A",
        "mnemonic": "ADC HL,BC",
        "description": "Add BC to HL with carry",
    },
    {
        "opcode": "0x4B",
        "mnemonic": "LD BC,(nn)",
        "description": "Load BC from absolute address nn",
    },
    {
        "opcode": "0x4C",
        "mnemonic": "stub: ED 4C",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0x4D", "mnemonic": "RETI", "description": "Return from interrupt"},
    {
        "opcode": "0x4E",
        "mnemonic": "IM 0/1",
        "description": "Placeholder for interrupt mode selector",
    },
    {"opcode": "0x4F", "mnemonic": "LD R,A", "description": "Load R with A"},
    {
        "opcode": "0x50",
        "mnemonic": "IN D,(C)",
        "description": "Input a byte from port C into D",
    },
    {"opcode": "0x51", "mnemonic": "OUT (C),D", "description": "Output D to port C"},
    {
        "opcode": "0x52",
        "mnemonic": "SBC HL,DE",
        "description": "Subtract DE from HL with carry",
    },
    {
        "opcode": "0x53",
        "mnemonic": "LD (nn),DE",
        "description": "Store DE at absolute address nn",
    },
    {
        "opcode": "0x54",
        "mnemonic": "stub: ED 54",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x55",
        "mnemonic": "stub: ED 55",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0x56", "mnemonic": "IM 1", "description": "Set interrupt mode 1"},
    {"opcode": "0x57", "mnemonic": "LD A,I", "description": "Load A with I"},
    {
        "opcode": "0x58",
        "mnemonic": "IN E,(C)",
        "description": "Input a byte from port C into E",
    },
    {"opcode": "0x59", "mnemonic": "OUT (C),E", "description": "Output E to port C"},
    {
        "opcode": "0x5A",
        "mnemonic": "ADC HL,DE",
        "description": "Add DE to HL with carry",
    },
    {
        "opcode": "0x5B",
        "mnemonic": "LD DE,(nn)",
        "description": "Load DE from absolute address nn",
    },
    {
        "opcode": "0x5C",
        "mnemonic": "stub: ED 5C",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x5D",
        "mnemonic": "stub: ED 5D",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0x5E", "mnemonic": "IM 2", "description": "Set interrupt mode 2"},
    {"opcode": "0x5F", "mnemonic": "LD A,R", "description": "Load A with R"},
    {
        "opcode": "0x60",
        "mnemonic": "IN H,(C)",
        "description": "Input a byte from port C into H",
    },
    {"opcode": "0x61", "mnemonic": "OUT (C),H", "description": "Output H to port C"},
    {
        "opcode": "0x62",
        "mnemonic": "SBC HL,HL",
        "description": "Subtract HL from HL with carry",
    },
    {
        "opcode": "0x63",
        "mnemonic": "LD (nn),HL",
        "description": "Store HL at absolute address nn",
    },
    {
        "opcode": "0x64",
        "mnemonic": "stub: ED 64",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x65",
        "mnemonic": "stub: ED 65",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x66",
        "mnemonic": "stub: ED 66",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x67",
        "mnemonic": "RRD",
        "description": "Rotate right digit in A and memory",
    },
    {
        "opcode": "0x68",
        "mnemonic": "IN L,(C)",
        "description": "Input a byte from port C into L",
    },
    {"opcode": "0x69", "mnemonic": "OUT (C),L", "description": "Output L to port C"},
    {
        "opcode": "0x6A",
        "mnemonic": "ADC HL,HL",
        "description": "Add HL to HL with carry",
    },
    {
        "opcode": "0x6B",
        "mnemonic": "LD HL,(nn)",
        "description": "Load HL from absolute address nn",
    },
    {
        "opcode": "0x6C",
        "mnemonic": "stub: ED 6C",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x6D",
        "mnemonic": "stub: ED 6D",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x6E",
        "mnemonic": "stub: ED 6E",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x6F",
        "mnemonic": "RLD",
        "description": "Rotate left digit in A and memory",
    },
    {"opcode": "0x70", "mnemonic": "IN F,(C)", "description": "Reserved input form"},
    {"opcode": "0x71", "mnemonic": "OUT (C),0", "description": "Reserved output form"},
    {
        "opcode": "0x72",
        "mnemonic": "SBC HL,SP",
        "description": "Subtract SP from HL with carry",
    },
    {
        "opcode": "0x73",
        "mnemonic": "LD (nn),SP",
        "description": "Store SP at absolute address nn",
    },
    {
        "opcode": "0x74",
        "mnemonic": "stub: ED 74",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x75",
        "mnemonic": "stub: ED 75",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x76",
        "mnemonic": "stub: ED 76",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x77",
        "mnemonic": "stub: ED 77",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x78",
        "mnemonic": "IN A,(C)",
        "description": "Input a byte from port C into A",
    },
    {"opcode": "0x79", "mnemonic": "OUT (C),A", "description": "Output A to port C"},
    {
        "opcode": "0x7A",
        "mnemonic": "ADC HL,SP",
        "description": "Add SP to HL with carry",
    },
    {
        "opcode": "0x7B",
        "mnemonic": "LD SP,(nn)",
        "description": "Load SP from absolute address nn",
    },
    {
        "opcode": "0x7C",
        "mnemonic": "stub: ED 7C",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x7D",
        "mnemonic": "stub: ED 7D",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x7E",
        "mnemonic": "stub: ED 7E",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0x7F",
        "mnemonic": "stub: ED 7F",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0xA0", "mnemonic": "LDI", "description": "Load and increment"},
    {"opcode": "0xA1", "mnemonic": "CPI", "description": "Compare and increment"},
    {"opcode": "0xA2", "mnemonic": "INI", "description": "Input and increment"},
    {"opcode": "0xA3", "mnemonic": "OUTI", "description": "Output and increment"},
    {
        "opcode": "0xA4",
        "mnemonic": "stub: ED A4",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xA5",
        "mnemonic": "stub: ED A5",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xA6",
        "mnemonic": "stub: ED A6",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xA7",
        "mnemonic": "stub: ED A7",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0xA8", "mnemonic": "LDD", "description": "Load and decrement"},
    {"opcode": "0xA9", "mnemonic": "CPD", "description": "Compare and decrement"},
    {"opcode": "0xAA", "mnemonic": "IND", "description": "Input and decrement"},
    {"opcode": "0xAB", "mnemonic": "OUTD", "description": "Output and decrement"},
    {
        "opcode": "0xAC",
        "mnemonic": "stub: ED AC",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xAD",
        "mnemonic": "stub: ED AD",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xAE",
        "mnemonic": "stub: ED AE",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xAF",
        "mnemonic": "stub: ED AF",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0xB0", "mnemonic": "LDIR", "description": "Load, increment, repeat"},
    {"opcode": "0xB1", "mnemonic": "CPIR", "description": "Compare, increment, repeat"},
    {"opcode": "0xB2", "mnemonic": "INIR", "description": "Input, increment, repeat"},
    {"opcode": "0xB3", "mnemonic": "OTIR", "description": "Output, increment, repeat"},
    {
        "opcode": "0xB4",
        "mnemonic": "stub: ED B4",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xB5",
        "mnemonic": "stub: ED B5",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xB6",
        "mnemonic": "stub: ED B6",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xB7",
        "mnemonic": "stub: ED B7",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {"opcode": "0xB8", "mnemonic": "LDDR", "description": "Load, decrement, repeat"},
    {"opcode": "0xB9", "mnemonic": "CPDR", "description": "Compare, decrement, repeat"},
    {"opcode": "0xBA", "mnemonic": "INDR", "description": "Input, decrement, repeat"},
    {"opcode": "0xBB", "mnemonic": "OTDR", "description": "Output, decrement, repeat"},
    {
        "opcode": "0xBC",
        "mnemonic": "stub: ED BC",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xBD",
        "mnemonic": "stub: ED BD",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xBE",
        "mnemonic": "stub: ED BE",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xBF",
        "mnemonic": "stub: ED BF",
        "description": "Placeholder for unimplemented ED opcode",
    },
    {
        "opcode": "0xED",
        "mnemonic": "ED prefix",
        "description": "Prefix for the extended instruction table",
    },
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0x40
# Mnemonic: IN B,(C)
# Description: Input a byte from port C into B


def _in_b_c(self):
    self.B.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x41
# Mnemonic: OUT (C),B
# Description: Output B to port C


def _out_c_b(self):
    self.port_out(self.BC.get(), self.B.get())
    return 12


# Opcode: 0x42
# Mnemonic: SBC HL,BC
# Description: Subtract BC from HL with carry


def _sbc_hl_bc(self):
    self.HL.set(self.sbc_hl_ss(self.BC.get()))
    return 15


# Opcode: 0x43
# Mnemonic: LD (nn),BC
# Description: Store BC at absolute address nn


def _ld_nn_bc(self):
    self.memory.write16(self.ingest_next_word(), self.BC.get())
    return 20


# Opcode: 0x44
# Mnemonic: NEG
# Description: Negate accumulator


def _neg(self):
    self.neg_acc()
    return 8


# Opcode: 0x45
# Mnemonic: RETN
# Description: Return from non-maskable interrupt


def _retn(self):
    self.PC.set(self.pop_word())
    self.IFF1 = self.IFF2
    return 14


# Opcode: 0x46
# Mnemonic: IM 0
# Description: Set interrupt mode 0


def _im_0(self):
    self.im_mode(0)
    return 8


# Opcode: 0x47
# Mnemonic: LD I,A
# Description: Load I with A


def _ld_i_a(self):
    self.load_reg_from_a("I")
    return 9


# Opcode: 0x48
# Mnemonic: IN C,(C)
# Description: Input a byte from port C into C


def _in_c_c(self):
    self.C.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x49
# Mnemonic: OUT (C),C
# Description: Output C to port C


def _out_c_c(self):
    self.port_out(self.BC.get(), self.C.get())
    return 12


# Opcode: 0x4A
# Mnemonic: ADC HL,BC
# Description: Add BC to HL with carry


def _adc_hl_bc(self):
    self.HL.set(self.adc_hl_ss(self.BC.get()))
    return 15


# Opcode: 0x4B
# Mnemonic: LD BC,(nn)
# Description: Load BC from absolute address nn


def _ld_bc_nn(self):
    self.BC.set(self.memory.read16(self.ingest_next_word()))
    return 20


# Opcode: 0x4D
# Mnemonic: RETI
# Description: Return from interrupt


def _reti(self):
    self.PC.set(self.pop_word())
    self.IFF1 = self.IFF2
    return 14


# Opcode: 0x4E
# Mnemonic: IM 0/1
# Description: Placeholder for interrupt mode selector


def _im_1(self):
    self.im_mode(1)
    return 8


# Opcode: 0x4F
# Mnemonic: LD R,A
# Description: Load R with A


def _ld_r_a(self):
    self.R.set(self.A.get())
    return 9


# Opcode: 0x50
# Mnemonic: IN D,(C)
# Description: Input a byte from port C into D


def _in_d_c(self):
    self.D.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x51
# Mnemonic: OUT (C),D
# Description: Output D to port C


def _out_c_d(self):
    self.port_out(self.BC.get(), self.D.get())
    return 12


# Opcode: 0x52
# Mnemonic: SBC HL,DE
# Description: Subtract DE from HL with carry


def _sbc_hl_de(self):
    self.HL.set(self.sbc_hl_ss(self.DE.get()))
    return 15


# Opcode: 0x53
# Mnemonic: LD (nn),DE
# Description: Store DE at absolute address nn


def _ld_nn_de(self):
    self.memory.write16(self.ingest_next_word(), self.DE.get())
    return 20


# Opcode: 0x56
# Mnemonic: IM 1
# Description: Set interrupt mode 1


def _im_2(self):
    self.im_mode(2)
    return 8


# Opcode: 0x57
# Mnemonic: LD A,I
# Description: Load A with I


def _ld_a_i(self):
    self.A.set(self.I.get())
    self.set_input_flags(self.A.get())
    return 9


# Opcode: 0x58
# Mnemonic: IN E,(C)
# Description: Input a byte from port C into E


def _in_e_c(self):
    self.E.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x59
# Mnemonic: OUT (C),E
# Description: Output E to port C


def _out_c_e(self):
    self.port_out(self.BC.get(), self.E.get())
    return 12


# Opcode: 0x5A
# Mnemonic: ADC HL,DE
# Description: Add DE to HL with carry


def _adc_hl_de(self):
    self.HL.set(self.adc_hl_ss(self.DE.get()))
    return 15


# Opcode: 0x5B
# Mnemonic: LD DE,(nn)
# Description: Load DE from absolute address nn


def _ld_de_nn(self):
    self.DE.set(self.memory.read16(self.ingest_next_word()))
    return 20


# Opcode: 0x5F
# Mnemonic: LD A,R
# Description: Load A with R


def _ld_a_r(self):
    self.A.set(self.R.get())
    self.set_input_flags(self.A.get())
    return 9


# Opcode: 0x60
# Mnemonic: IN H,(C)
# Description: Input a byte from port C into H


def _in_h_c(self):
    self.H.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x61
# Mnemonic: OUT (C),H
# Description: Output H to port C


def _out_c_h(self):
    self.port_out(self.BC.get(), self.H.get())
    return 12


# Opcode: 0x62
# Mnemonic: SBC HL,HL
# Description: Subtract HL from HL with carry


def _sbc_hl_hl(self):
    self.HL.set(self.sbc_hl_ss(self.HL.get()))
    return 15


# Opcode: 0x63
# Mnemonic: LD (nn),HL
# Description: Store HL at absolute address nn


def _ld_nn_hl(self):
    self.memory.write16(self.ingest_next_word(), self.HL.get())
    return 20


# Opcode: 0x67
# Mnemonic: RRD
# Description: Rotate right digit in A and memory


def _rrd(self):
    self.rrd()
    return 18


# Opcode: 0x68
# Mnemonic: IN L,(C)
# Description: Input a byte from port C into L


def _in_l_c(self):
    self.L.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x69
# Mnemonic: OUT (C),L
# Description: Output L to port C


def _out_c_l(self):
    self.port_out(self.BC.get(), self.L.get())
    return 12


# Opcode: 0x6A
# Mnemonic: ADC HL,HL
# Description: Add HL to HL with carry


def _adc_hl_hl(self):
    self.HL.set(self.adc_hl_ss(self.HL.get()))
    return 15


# Opcode: 0x6B
# Mnemonic: LD HL,(nn)
# Description: Load HL from absolute address nn


def _ld_hl_nn(self):
    self.HL.set(self.memory.read16(self.ingest_next_word()))
    return 20


# Opcode: 0x6F
# Mnemonic: RLD
# Description: Rotate left digit in A and memory


def _rld(self):
    self.rld()
    return 18


# Opcode: 0x70
# Mnemonic: IN F,(C)
# Description: Reserved input form


def _in_f_c(self):
    self.port_in(self.BC.get())
    return 12


# Opcode: 0x71
# Mnemonic: OUT (C),0
# Description: Reserved output form


def _out_c_zero(self):
    self.port_out(self.BC.get(), 0)
    return 12


# Opcode: 0x72
# Mnemonic: SBC HL,SP
# Description: Subtract SP from HL with carry


def _sbc_hl_sp(self):
    self.HL.set(self.sbc_hl_ss(self.SP.get()))
    return 15


# Opcode: 0x73
# Mnemonic: LD (nn),SP
# Description: Store SP at absolute address nn


def _ld_nn_sp(self):
    self.memory.write16(self.ingest_next_word(), self.SP.get())
    return 20


# Opcode: 0x78
# Mnemonic: IN A,(C)
# Description: Input a byte from port C into A


def _in_a_c(self):
    self.A.set(self.port_in(self.BC.get()))
    return 12


# Opcode: 0x79
# Mnemonic: OUT (C),A
# Description: Output A to port C


def _out_c_a(self):
    self.port_out(self.BC.get(), self.A.get())
    return 12


# Opcode: 0x7A
# Mnemonic: ADC HL,SP
# Description: Add SP to HL with carry


def _adc_hl_sp(self):
    self.HL.set(self.adc_hl_ss(self.SP.get()))
    return 15


# Opcode: 0x7B
# Mnemonic: LD SP,(nn)
# Description: Load SP from absolute address nn


def _ld_sp_nn(self):
    self.SP.set(self.memory.read16(self.ingest_next_word()))
    return 20


# Opcode: 0xA0
# Mnemonic: LDI
# Description: Load and increment


def _ldi(self):
    self.block_load(1)
    self.F.add_sub = False
    self.F.half_carry = False
    self.F.parity_overflow = False
    return 16


# Opcode: 0xA1
# Mnemonic: CPI
# Description: Compare and increment


def _cpi(self):
    self.block_compare(1)
    self.F.half_carry = False
    self.F.add_sub = True
    self.F.parity_overflow = self.BC.get() != 0
    return 16


# Opcode: 0xA2
# Mnemonic: INI
# Description: Input and increment


def _ini(self):
    self.block_input(1)
    return 16


# Opcode: 0xA3
# Mnemonic: OUTI
# Description: Output and increment


def _outi(self):
    self.block_output(1)
    return 16


# Opcode: 0xA8
# Mnemonic: LDD
# Description: Load and decrement


def _ldd(self):
    self.block_load(-1)
    self.F.add_sub = False
    self.F.half_carry = False
    self.F.parity_overflow = False
    return 16


# Opcode: 0xA9
# Mnemonic: CPD
# Description: Compare and decrement


def _cpd(self):
    self.block_compare(-1)
    self.F.half_carry = False
    self.F.add_sub = True
    self.F.parity_overflow = self.BC.get() != 0
    return 16


# Opcode: 0xAA
# Mnemonic: IND
# Description: Input and decrement


def _ind(self):
    self.block_input(-1)
    return 16


# Opcode: 0xAB
# Mnemonic: OUTD
# Description: Output and decrement


def _outd(self):
    self.block_output(-1)
    return 16


# Opcode: 0xB0
# Mnemonic: LDIR
# Description: Load, increment, repeat


def _ldir(self):
    self.block_load(1)
    if self.BC.get() != 0:
        self.PC.dec(2)
        self.F.parity_overflow = True
        return 21
    self.F.parity_overflow = False
    return 16


# Opcode: 0xB1
# Mnemonic: CPIR
# Description: Compare, increment, repeat


def _cpir(self):
    self.block_compare(1)
    if self.BC.get() != 0:
        self.PC.dec(2)
        self.F.parity_overflow = True
        return 21
    self.F.parity_overflow = False
    return 16


# Opcode: 0xB2
# Mnemonic: INIR
# Description: Input, increment, repeat


def _inir(self):
    self.block_input(1)
    if self.B.get() != 0:
        self.PC.dec(2)
        return 21
    return 16


# Opcode: 0xB3
# Mnemonic: OTIR
# Description: Output, increment, repeat


def _otir(self):
    self.block_output(1)
    if self.B.get() != 0:
        self.PC.dec(2)
        return 21
    return 16


# Opcode: 0xB8
# Mnemonic: LDDR
# Description: Load, decrement, repeat


def _lddr(self):
    self.block_load(-1)
    if self.BC.get() != 0:
        self.PC.dec(2)
        self.F.parity_overflow = True
        return 21
    self.F.parity_overflow = False
    return 16


# Opcode: 0xB9
# Mnemonic: CPDR
# Description: Compare, decrement, repeat


def _cpdr(self):
    self.block_compare(-1)
    if self.BC.get() != 0:
        self.PC.dec(2)
        self.F.parity_overflow = True
        return 21
    self.F.parity_overflow = False
    return 16


# Opcode: 0xBA
# Mnemonic: INDR
# Description: Input, decrement, repeat


def _indr(self):
    self.block_input(-1)
    if self.B.get() != 0:
        self.PC.dec(2)
        return 21
    return 16


# Opcode: 0xBB
# Mnemonic: OTDR
# Description: Output, decrement, repeat


def _otdr(self):
    self.block_output(-1)
    if self.B.get() != 0:
        self.PC.dec(2)
        return 21
    return 16


def execute(self, opcode):
    prefix = opcode
    opcode = self.ingest_next_byte()

    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0x40:
                return _in_b_c(self)
            if opcode == 0x41:
                return _out_c_b(self)
            if opcode == 0x42:
                return _sbc_hl_bc(self)
            if opcode == 0x43:
                return _ld_nn_bc(self)
            if opcode == 0x44:
                return _neg(self)
            if opcode == 0x45:
                return _retn(self)
            if opcode == 0x46:
                return _im_0(self)
            if opcode == 0x47:
                return _ld_i_a(self)
            if opcode == 0x48:
                return _in_c_c(self)
            if opcode == 0x49:
                return _out_c_c(self)
            if opcode == 0x4A:
                return _adc_hl_bc(self)
            if opcode == 0x4B:
                return _ld_bc_nn(self)
            if opcode == 0x4D:
                return _reti(self)
            if opcode == 0x4E:
                return _im_1(self)
            if opcode == 0x4F:
                return _ld_r_a(self)
            if opcode == 0x50:
                return _in_d_c(self)
            if opcode == 0x51:
                return _out_c_d(self)
            if opcode == 0x52:
                return _sbc_hl_de(self)
            if opcode == 0x53:
                return _ld_nn_de(self)
            if opcode == 0x56:
                return _im_2(self)
            if opcode == 0x57:
                return _ld_a_i(self)
            if opcode == 0x58:
                return _in_e_c(self)
            if opcode == 0x59:
                return _out_c_e(self)
            if opcode == 0x5A:
                return _adc_hl_de(self)
            if opcode == 0x5B:
                return _ld_de_nn(self)
            if opcode == 0x5F:
                return _ld_a_r(self)
            if opcode == 0x60:
                return _in_h_c(self)
            if opcode == 0x61:
                return _out_c_h(self)
            if opcode == 0x62:
                return _sbc_hl_hl(self)
            if opcode == 0x63:
                return _ld_nn_hl(self)
            if opcode == 0x67:
                return _rrd(self)
            if opcode == 0x68:
                return _in_l_c(self)
            if opcode == 0x69:
                return _out_c_l(self)
            if opcode == 0x6A:
                return _adc_hl_hl(self)
            if opcode == 0x6B:
                return _ld_hl_nn(self)
            if opcode == 0x6F:
                return _rld(self)
            if opcode == 0x70:
                return _in_f_c(self)
            if opcode == 0x71:
                return _out_c_zero(self)
            if opcode == 0x72:
                return _sbc_hl_sp(self)
            if opcode == 0x73:
                return _ld_nn_sp(self)
            if opcode == 0x78:
                return _in_a_c(self)
            if opcode == 0x79:
                return _out_c_a(self)
            if opcode == 0x7A:
                return _adc_hl_sp(self)
            if opcode == 0x7B:
                return _ld_sp_nn(self)
            if opcode == 0xA0:
                return _ldi(self)
            if opcode == 0xA1:
                return _cpi(self)
            if opcode == 0xA2:
                return _ini(self)
            if opcode == 0xA3:
                return _outi(self)
            if opcode == 0xA8:
                return _ldd(self)
            if opcode == 0xA9:
                return _cpd(self)
            if opcode == 0xAA:
                return _ind(self)
            if opcode == 0xAB:
                return _outd(self)
            if opcode == 0xB0:
                return _ldir(self)
            if opcode == 0xB1:
                return _cpir(self)
            if opcode == 0xB2:
                return _inir(self)
            if opcode == 0xB3:
                return _otir(self)
            if opcode == 0xB8:
                return _lddr(self)
            if opcode == 0xB9:
                return _cpdr(self)
            if opcode == 0xBA:
                return _indr(self)
            if opcode == 0xBB:
                return _otdr(self)

            raise NotImplementedError(
                f"{__name__}: {prefix:02X} {opcode:02X} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(
        f"{__name__}: opcode {prefix:02X} {opcode:02X} is not defined in the ED-prefixed instruction table"
    )
