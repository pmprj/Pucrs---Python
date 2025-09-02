# make_sample.py
# -*- coding: utf-8 -*-
"""
Gera uma amostra aleatória de 20 jogos (não os 20 primeiros).
Salva em sample_20.csv mantendo o cabeçalho original.
"""

import csv
import random
import sys

def make_sample(src_csv: str, dst_csv: str = "sample_20.csv", seed: int = 42):
    random.seed(seed)
    with open(src_csv, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        if len(rows) < 40:
            raise ValueError("Dataset muito pequeno para amostrar 20 jogos não sequenciais.")

        shuffled = rows[:]  # cópia
        random.shuffle(shuffled)
        sample = shuffled[:20]

        fieldnames = list(rows[0].keys())
        with open(dst_csv, "w", encoding="utf-8", newline="") as out:
            w = csv.DictWriter(out, fieldnames=fieldnames)
            w.writeheader()
            for row in sample:
                w.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python make_sample.py /caminho/steam_games.csv")
        sys.exit(1)
    make_sample(sys.argv[1])
    print("Amostra salva em sample_20.csv")
