# main.py
# -*- coding: utf-8 -*-

import argparse
from steamdata import SteamData, SteamDataError

def main():
    parser = argparse.ArgumentParser(description="Fase 1 – Fun Corp – Steam (Python puro)")
    parser.add_argument("--csv", required=True, help="Caminho para o CSV (completo ou amostra)")
    args = parser.parse_args()

    try:
        sd = SteamData(args.csv)
        sd.load()

        # P1
        print("== P1: Percentual de jogos gratuitos vs pagos ==")
        p1 = sd.percent_free_vs_paid()
        print(f"Total: {p1['total']} | Gratuitos: {p1['gratuitos_qtd']} ({p1['gratuitos_%']}%) "
              f"| Pagos: {p1['pagos_qtd']} ({p1['pagos_%']}%)\n")

        # P2
        print("== P2: Ano(s) com mais lançamentos ==")
        anos = sd.top_years_by_releases()
        if anos:
            print("Ano(s):", ", ".join(str(a) for a in anos))
            # opcional: mostrar top 5 anos
            hist = sd.year_histogram()[:5]
            print("Top 5 (ano: contagem):", ", ".join([f"{a}: {c}" for a, c in hist]))
        else:
            print("Não foi possível determinar o(s) ano(s).")
        print()

        # P3
        print("== P3: Sistema operacional mais compatível + resumo multi-OS ==")
        os_name, qty, pct = sd.most_compatible_os()
        print(f"Mais compatível: {os_name} ({qty} jogos; {pct}%)")
        mos = sd.multi_os_summary()
        print(f"Multi-OS: {mos['multi_qtd']} ({mos['multi_%']}%) "
              f"| Single-OS: {mos['single_qtd']} ({mos['single_%']}%) "
              f"| Zero-OS: {mos['zero_qtd']} ({mos['zero_%']}%)")

    except SteamDataError as e:
        print("[ERRO] SteamData:", e)
    except Exception as e:
        print("[ERRO] Geral:", e)

if __name__ == "__main__":
    main()
