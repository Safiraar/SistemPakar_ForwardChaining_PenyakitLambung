# =============================
# FILE: rules.py
# =============================
# Basis pengetahuan Sistem Pakar Penyakit Lambung

penyakit = {
    "P01": "Maag",
    "P02": "GERD",
    "P03": "Dyspepsia",
    "P04": "Tukak Lambung"
}

gejala = {
    "G01": "Mual dan Muntah",
    "G02": "Nafsu Makan Berkurang",
    "G03": "Perut Sakit",
    "G04": "Perut Kembung",
    "G05": "Nyeri Ulu Hati",
    "G06": "Sendawa",
    "G07": "Berat Badan Turun",
    "G08": "Lemah Letih Lesuh",
    "G09": "Sakit Pada Tukak Lambung",
    "G10": "Sesak Napas",
    "G11": "Sembelit",
    "G12": "Perubahan Suhu Tubuh dan Keringat Dingin",
    "G13": "Perasaan Kenyang Berlebih",
    "G14": "BAB Hitam",
    "G15": "Sering Cegukan",
    "G16": "BAB Berdarah",
    "G17": "Anemia",
    "G18": "Sulit Tidur",
    "G19": "Sakit Tenggorokan",
    "G20": "Asam dan Pahit Pada Mulut"
}

# Rules berbasis Forward Chaining
rules = {
    "P01": ["G01", "G02", "G03", "G04", "G06", "G15", "G20"],
    "P02": ["G01", "G02", "G03", "G05", "G06", "G11", "G13", "G18", "G19", "G20"],
    "P03": ["G03", "G04", "G06", "G11", "G13", "G18"],
    "P04": ["G02", "G07", "G08", "G09", "G10", "G12", "G14", "G16", "G17"]
}


def forward_chaining(selected_gejala):
    hasil = {}
    for kode_penyakit, daftar_gejala in rules.items():
        cocok = set(selected_gejala).intersection(set(daftar_gejala))
        if cocok:
            hasil[kode_penyakit] = len(cocok) / len(daftar_gejala)
    return hasil

