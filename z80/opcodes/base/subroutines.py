OPCODES = [
    {"opcode": "0xC0", "mnemonic": "RET NZ", "description": "Return if Z is reset"},
    {"opcode": "0xC4", "mnemonic": "CALL NZ,nn", "description": "Call nn if Z is reset"},
    {"opcode": "0xC7", "mnemonic": "RST 00H", "description": "Call fixed address 0000H"},
    {"opcode": "0xC8", "mnemonic": "RET Z", "description": "Return if Z is set"},
    {"opcode": "0xC9", "mnemonic": "RET", "description": "Return from subroutine"},
    {"opcode": "0xCC", "mnemonic": "CALL Z,nn", "description": "Call nn if Z is set"},
    {"opcode": "0xCD", "mnemonic": "CALL nn", "description": "Call subroutine at absolute address nn"},
    {"opcode": "0xCF", "mnemonic": "RST 08H", "description": "Call fixed address 0008H"},
    {"opcode": "0xD0", "mnemonic": "RET NC", "description": "Return if C is reset"},
    {"opcode": "0xD4", "mnemonic": "CALL NC,nn", "description": "Call nn if C is reset"},
    {"opcode": "0xD7", "mnemonic": "RST 10H", "description": "Call fixed address 0010H"},
    {"opcode": "0xD8", "mnemonic": "RET C", "description": "Return if C is set"},
    {"opcode": "0xDC", "mnemonic": "CALL C,nn", "description": "Call nn if C is set"},
    {"opcode": "0xDF", "mnemonic": "RST 18H", "description": "Call fixed address 0018H"},
    {"opcode": "0xE0", "mnemonic": "RET PO", "description": "Return if parity is odd"},
    {"opcode": "0xE4", "mnemonic": "CALL PO,nn", "description": "Call nn if parity is odd"},
    {"opcode": "0xE7", "mnemonic": "RST 20H", "description": "Call fixed address 0020H"},
    {"opcode": "0xE8", "mnemonic": "RET PE", "description": "Return if parity is even"},
    {"opcode": "0xEC", "mnemonic": "CALL PE,nn", "description": "Call nn if parity is even"},
    {"opcode": "0xEF", "mnemonic": "RST 28H", "description": "Call fixed address 0028H"},
    {"opcode": "0xF0", "mnemonic": "RET P", "description": "Return if sign is positive"},
    {"opcode": "0xF4", "mnemonic": "CALL P,nn", "description": "Call nn if sign is positive"},
    {"opcode": "0xF7", "mnemonic": "RST 30H", "description": "Call fixed address 0030H"},
    {"opcode": "0xF8", "mnemonic": "RET M", "description": "Return if sign is negative"},
    {"opcode": "0xFC", "mnemonic": "CALL M,nn", "description": "Call nn if sign is negative"},
    {"opcode": "0xFF", "mnemonic": "RST 38H", "description": "Call fixed address 0038H"},
]


def _matches_opcode(opcode, entry):
    value = entry["opcode"]
    if "-" in value:
        start, end = value.split("-", 1)
        return int(start, 16) <= opcode <= int(end, 16)
    return opcode == int(value, 16)


# Opcode: 0xC0
# Mnemonic: RET NZ
# Description: Return if Z is reset

def _ret_nz(self):
    return None


# Opcode: 0xC4
# Mnemonic: CALL NZ,nn
# Description: Call nn if Z is reset

def _call_nz_nn(self):
    return None


# Opcode: 0xC7
# Mnemonic: RST 00H
# Description: Call fixed address 0000H

def _rst_00(self):
    return None


# Opcode: 0xC8
# Mnemonic: RET Z
# Description: Return if Z is set

def _ret_z(self):
    return None


# Opcode: 0xC9
# Mnemonic: RET
# Description: Return from subroutine

def _ret(self):
    return None


# Opcode: 0xCC
# Mnemonic: CALL Z,nn
# Description: Call nn if Z is set

def _call_z_nn(self):
    return None


# Opcode: 0xCD
# Mnemonic: CALL nn
# Description: Call subroutine at absolute address nn

def _call_nn(self):
    return None


# Opcode: 0xCF
# Mnemonic: RST 08H
# Description: Call fixed address 0008H

def _rst_08(self):
    return None


# Opcode: 0xD0
# Mnemonic: RET NC
# Description: Return if C is reset

def _ret_nc(self):
    return None


# Opcode: 0xD4
# Mnemonic: CALL NC,nn
# Description: Call nn if C is reset

def _call_nc_nn(self):
    return None


# Opcode: 0xD7
# Mnemonic: RST 10H
# Description: Call fixed address 0010H

def _rst_10(self):
    return None


# Opcode: 0xD8
# Mnemonic: RET C
# Description: Return if C is set

def _ret_c(self):
    return None


# Opcode: 0xDC
# Mnemonic: CALL C,nn
# Description: Call nn if C is set

def _call_c_nn(self):
    return None


# Opcode: 0xDF
# Mnemonic: RST 18H
# Description: Call fixed address 0018H

def _rst_18(self):
    return None


# Opcode: 0xE0
# Mnemonic: RET PO
# Description: Return if parity is odd

def _ret_po(self):
    return None


# Opcode: 0xE4
# Mnemonic: CALL PO,nn
# Description: Call nn if parity is odd

def _call_po_nn(self):
    return None


# Opcode: 0xE7
# Mnemonic: RST 20H
# Description: Call fixed address 0020H

def _rst_20(self):
    return None


# Opcode: 0xE8
# Mnemonic: RET PE
# Description: Return if parity is even

def _ret_pe(self):
    return None


# Opcode: 0xEC
# Mnemonic: CALL PE,nn
# Description: Call nn if parity is even

def _call_pe_nn(self):
    return None


# Opcode: 0xEF
# Mnemonic: RST 28H
# Description: Call fixed address 0028H

def _rst_28(self):
    return None


# Opcode: 0xF0
# Mnemonic: RET P
# Description: Return if sign is positive

def _ret_p(self):
    return None


# Opcode: 0xF4
# Mnemonic: CALL P,nn
# Description: Call nn if sign is positive

def _call_p_nn(self):
    return None


# Opcode: 0xF7
# Mnemonic: RST 30H
# Description: Call fixed address 0030H

def _rst_30(self):
    return None


# Opcode: 0xF8
# Mnemonic: RET M
# Description: Return if sign is negative

def _ret_m(self):
    return None


# Opcode: 0xFC
# Mnemonic: CALL M,nn
# Description: Call nn if sign is negative

def _call_m_nn(self):
    return None


# Opcode: 0xFF
# Mnemonic: RST 38H
# Description: Call fixed address 0038H

def _rst_38(self):
    return None


def execute(self, opcode):
    for entry in OPCODES:
        if _matches_opcode(opcode, entry):
            if opcode == 0xC0:
                return _ret_nz(self)
            if opcode == 0xC4:
                return _call_nz_nn(self)
            if opcode == 0xC7:
                return _rst_00(self)
            if opcode == 0xC8:
                return _ret_z(self)
            if opcode == 0xC9:
                return _ret(self)
            if opcode == 0xCC:
                return _call_z_nn(self)
            if opcode == 0xCD:
                return _call_nn(self)
            if opcode == 0xCF:
                return _rst_08(self)
            if opcode == 0xD0:
                return _ret_nc(self)
            if opcode == 0xD4:
                return _call_nc_nn(self)
            if opcode == 0xD7:
                return _rst_10(self)
            if opcode == 0xD8:
                return _ret_c(self)
            if opcode == 0xDC:
                return _call_c_nn(self)
            if opcode == 0xDF:
                return _rst_18(self)
            if opcode == 0xE0:
                return _ret_po(self)
            if opcode == 0xE4:
                return _call_po_nn(self)
            if opcode == 0xE7:
                return _rst_20(self)
            if opcode == 0xE8:
                return _ret_pe(self)
            if opcode == 0xEC:
                return _call_pe_nn(self)
            if opcode == 0xEF:
                return _rst_28(self)
            if opcode == 0xF0:
                return _ret_p(self)
            if opcode == 0xF4:
                return _call_p_nn(self)
            if opcode == 0xF7:
                return _rst_30(self)
            if opcode == 0xF8:
                return _ret_m(self)
            if opcode == 0xFC:
                return _call_m_nn(self)
            if opcode == 0xFF:
                return _rst_38(self)

            raise NotImplementedError(
                f"{__name__}: {entry['opcode']} {entry['mnemonic']} ({entry['description']}) is not implemented"
            )

    raise NotImplementedError(f"{__name__}: opcode 0x{opcode:02X} is not defined in the subroutine table")
