from utility import read
from ex import decrypt


MAGIC = b"!<arch>\n"


def ObjectFiles(file, json_data, py_data):
    header = decrypt(file, json_data["ArchiveMemberHeader"], py_data)

    machine = read(file, "*u2")
    file.seek(file.tell() - 2)
    res = {
        "ArchiveMemberHeader": header,
        "#ArchiveMemberHeader": file.tell()
    }
    tell = file.tell()
    if machine != 0:
        res.update(decrypt(file, json_data["_LongFormat"], py_data))

        for section in res['SectionHeaders']:
            file.seek(tell + section['PointerToRawData'])
            section['RawData'] = file.read(section['SizeOfRawData'])

            if section['NumberOfRelocations'] > 0:
                file.seek(tell + section['PointerToRelocations'])
                section['Relocations'] = [decrypt(file, "header/relocation.json", py_data) for i in range(section['NumberOfRelocations'])]

    else:
        res.update(decrypt(file, json_data["_ShortFormat"], py_data))

    file.seek(tell + res['ArchiveMemberHeader']['Size'])

    while file.read(1) == b'\n':
        pass
    file.seek(file.tell() - 1)

    # print(hex(file.tell()))

    return res


def SectionHeaders(file, json_data, py_data):
    pass
