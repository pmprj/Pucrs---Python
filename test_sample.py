# tests/test_sample.py
# -*- coding: utf-8 -*-

import os
from steamdata import SteamData

# Caminho para a amostra
SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "sample_20.csv")

# ======= PREENCHA com os valores da sua amostra (calculados manualmente) =======
EXPECTED_TOTAL = 20

# P1
EXPECTED_FREE_PERCENT = 10.00   # ex.: 10.00
EXPECTED_PAID_PERCENT = 90.00   # ex.: 90.00

# P2 (lista ordenada de anos com mais lançamentos; se um só, lista com um elemento)
EXPECTED_TOP_YEARS = [2022]

# P3 (SO mais compatível na amostra)
EXPECTED_MOST_OS = "Windows"
# ==============================================================================

def test_p1_percent_free_vs_paid():
    sd = SteamData(SAMPLE_CSV)
    sd.load()
    res = sd.percent_free_vs_paid()
    assert res["total"] == EXPECTED_TOTAL
    assert res["gratuitos_%"] == EXPECTED_FREE_PERCENT
    assert res["pagos_%"] == EXPECTED_PAID_PERCENT

def test_p2_top_years():
    sd = SteamData(SAMPLE_CSV)
    sd.load()
    anos = sd.top_years_by_releases()
    assert anos == EXPECTED_TOP_YEARS

def test_p3_most_compatible_os():
    sd = SteamData(SAMPLE_CSV)
    sd.load()
    os_name, qty, pct = sd.most_compatible_os()
    assert os_name == EXPECTED_MOST_OS
