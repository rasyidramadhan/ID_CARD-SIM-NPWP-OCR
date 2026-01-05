from rapidfuzz import fuzz


def ktp(texts):
    FIELDS = [
        'NIK', 'NAMA',
        'TEMPAT/TGL LAHIR', 'JENIS KELAMIN',
        'GOL DARAH', 'GOL. DARAH',
        'ALAMAT', 'RT/RW', 'KEL/DESA',
        'KECAMATAN', 'AGAMA',
        'STATUS PERKAWINAN',
        'PEKERJAAN', 'KEWARGANEGARAAN',
        'BERLAKU HINGGA'
    ]

    clean_data = []

    for text in texts:
        if not text:
            continue

        text = text.replace('N1K', 'NIK')

        t = text.replace(':', '').strip()
        t_upper = t.upper()

        is_field = False
        for f in FIELDS:
            if fuzz.partial_ratio(f, t_upper) > 80:
                is_field = True
                break

        if not is_field and t:
            clean_data.append(t)

    return clean_data


def sim(texts):
    clean_data = []

    for text in texts:
        if not text:
            continue

        t = text
        for i in range(1, 7):
            t = t.replace(f"{i}.", "")

        t = t.strip()

        if t:
            clean_data.append(t)

    return clean_data

def npwp(texts):
    FIELDS = [
        'NPVP',
        'DIREKTORAT JENDERAL PAJAK',
        'DIREKTORAT',
        'JENDERAL',
        'PAJAK',
        'WWW.PAJAK.GO.ID',
        'ODJP'
    ]

    clean_data = []

    for text in texts:
        if not text:
            continue

        t = text.strip()
        t_upper = t.upper()

        is_header = False
        for f in FIELDS:
            if fuzz.partial_ratio(f, t_upper) > 80:
                is_header = True
                break

        if not is_header and t:
            clean_data.append(t)

    return clean_data
