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
rules_fc = {
    "P01": ["G01", "G02", "G03", "G04", "G06", "G20"],
    "P02": ["G01", "G02", "G03", "G05", "G06", "G15", "G18", "G19", "G20"],
    "P03": ["G03", "G05", "G11", "G12", "G13", "G14", "G18"],
    "P04": ["G02", "G04", "G06", "G07", "G08", "G09", "G10",
            "G11", "G13", "G14", "G16", "G17"]
}

rules_cf = {
    "P01": {
        "G01": 0.5, "G02": 0.6, "G03": 0.7,
        "G04": 0.85, "G06": 0.6, "G20": 0.7
    },
    "P02": {
        "G01": 0.4, "G02": 0.4, "G03": 0.5,
        "G05": 0.9, "G06": 0.4, "G15": 0.85,
        "G18": 0.8, "G19": 0.85, "G20": 0.9
    },
    "P03": {
        "G03": 0.6, "G05": 0.6, "G11": 0.6,
        "G12": 0.5, "G13": 0.7, "G14": 0.6,
        "G18": 0.5
    },
    "P04": {
        "G02": 0.6, "G04": 0.5, "G06": 0.5,
        "G07": 0.7, "G08": 0.6, "G09": 0.9,
        "G10": 0.6, "G11": 0.5, "G13": 0.6,
        "G14": 0.8, "G16": 0.9, "G17": 0.7
    }
}

def forward_chaining(selected_gejala):
    kandidat = []
    for p, daftar_gejala in rules_fc.items():
        if set(selected_gejala) & set(daftar_gejala):
            kandidat.append(p)
    return kandidat

def certainty_factor(kandidat, selected_gejala):
    hasil = {}

    for p in kandidat:
        cf_combine = 0
        first = True

        for g in selected_gejala:
            if g in rules_cf[p]:
                cf = rules_cf[p][g]
                if first:
                    cf_combine = cf
                    first = False
                else:
                    cf_combine = cf_combine + cf * (1 - cf_combine)

        if cf_combine > 0:
            hasil[p] = cf_combine

    return hasil


