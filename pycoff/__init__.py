#!/usr/bin/python

from pe import PE
from elf import ELF
from ar import AR
from coff import COFF
from obj import OBJ
from defs import MAGIC, COFF_TYPE
from tk import show

import sys


def check_pe(file):
    file.seek(0x3c)
    sign_offset = int.from_bytes(file.read(4), byteorder=sys.byteorder)
    if sign_offset <= 0:
        return False

    file.seek(sign_offset)
    magic = file.read(len(MAGIC.PE))
    return magic == MAGIC.PE


def check_magic(file):
    # ELF
    magic = file.read(len(MAGIC.ELF))
    if magic == MAGIC.ELF:
        return COFF_TYPE.ELF

    # PE / MZ
    file.seek(0)
    magic = file.read(len(MAGIC.MZ))
    if magic == MAGIC.MZ:
        return COFF_TYPE.PE if check_pe(file) else COFF_TYPE.MZ

    # AR
    file.seek(0)
    magic = file.read(len(MAGIC.AR))
    if magic == MAGIC.AR:
        return COFF_TYPE.AR

    file.seek(0)
    magic = file.read(len(MAGIC.COFF))
    if magic == MAGIC.COFF:
        return COFF_TYPE.COFF

    file.seek(0)

    return COFF_TYPE.OBJ


def parser(file_path):
    file = open(file_path, 'rb')
    coff_type = check_magic(file)

    if coff_type == COFF_TYPE.COFF:
        return COFF(file, file_path)
    elif coff_type == COFF_TYPE.PE:
        return PE(file, file_path)
    elif coff_type == COFF_TYPE.ELF:
        return ELF(file, file_path)
    elif coff_type == COFF_TYPE.AR:
        return AR(file, file_path)
    elif coff_type == COFF_TYPE.OBJ:
        return OBJ(file, file_path)


def gui(file_path):
    obj = parser(file_path)
    show(obj)


# parse('E:\\L3D11Engine\\x64\\Debug\\LLoaderD.lib')
print(parser('E:\\L3D11Engine\\x64\\Debug\\LEngineD.lib').tojson())

# gui('E:\\L3D11Engine\\x64\\Debug\\LLoaderD.lib')
