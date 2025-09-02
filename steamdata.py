# steamdata.py
# -*- coding: utf-8 -*-
"""
Fase 1 – Programação para Dados (SEM pandas/numpy/matplotlib)

Este módulo implementa a classe SteamData com:
- Carga do CSV (csv.DictReader)
- P1: Percentual de jogos gratuitos e pagos
- P2: Ano(s) com maior número de lançamentos (empate -> lista)
- P3: Compatibilidade por sistema (Windows/Mac/Linux) + proporção multi-OS

Obs.: P3 foi definida como "Qual o sistema operacional mais compatível?",
mas o método também retorna percentuais e resumo multi-OS.
"""

import csv
import os
import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


# ---------------- Exceções específicas ----------------

class SteamDataError(Exception):
    """Exceção base do módulo SteamData."""
    pass


class FileNotFoundErrorSD(SteamDataError):
    """Arquivo CSV não encontrado."""
    pass


class InvalidCSVError(SteamDataError):
    """CSV inválido ou sem colunas obrigatórias."""
    pass


# ---------------- Classe principal ----------------

class SteamData:
    """
    Encapsula a carga e consultas do dataset da Steam usando Python puro.

    Atributos:
        csv_path (str): caminho do arquivo CSV
        data (List[Dict[str, str]]): linhas do CSV como dicionários
    """

    REQUIRED_MIN = {"Release date", "Price", "Windows", "Mac", "Linux"}

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data: List[Dict[str, str]] = []

    # ---------- utilidades internas ----------

    @staticmethod
    def _to_float(x: Optional[str]) -> float:
        """Converte str de preço para float. Vazios/ruído -> 0.0."""
        if x is None:
            return 0.0
        s = x.strip()
        if not s:
            return 0.0
        for token in ("R$", "$"):
            s = s.replace(token, "")
        s = s.replace(",", ".")
        try:
            return float(s)
        except Exception:
            return 0.0

    @staticmethod
    def _to_bool(x: Optional[str]) -> bool:
        if x is None:
            return False
        s = x.strip().lower()
        return s in {"true", "1", "yes", "y"}

    @staticmethod
    def _extract_year(date_str: Optional[str]) -> Optional[int]:
        """Extrai um ano (1970–2100) de uma string de data diversa."""
        if not date_str:
            return None
        years = re.findall(r"(19\d{2}|20\d{2})", date_str)
        year = None
        for y in years:
            y = int(y)
            if 1970 <= y <= 2100:
                year = y
        return year

    # ---------- carga ----------

    def load(self) -> List[Dict[str, str]]:
        """Carrega o CSV em self.data usando csv.DictReader."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundErrorSD(f"Arquivo não encontrado: {self.csv_path}")

        with open(self.csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise InvalidCSVError("CSV sem cabeçalho.")

            cols = set(reader.fieldnames)
            missing = self.REQUIRED_MIN - cols
            if missing:
                raise InvalidCSVError(f"CSV sem colunas mínimas requeridas: {missing}")

            self.data = [row for row in reader]

        if not self.data:
            raise InvalidCSVError("CSV carregado, mas sem linhas.")
        return self.data

    # ---------- P1: % gratuitos vs pagos ----------

    def percent_free_vs_paid(self) -> Dict[str, float]:
        """
        Retorna:
            {
              "total": int,
              "gratuitos_%": float (0-100, 2 casas),
              "pagos_%": float (0-100, 2 casas),
              "gratuitos_qtd": int,
              "pagos_qtd": int
            }
        """
        total = len(self.data)
        if total == 0:
            return {"total": 0, "gratuitos_%": 0.0, "pagos_%": 0.0,
                    "gratuitos_qtd": 0, "pagos_qtd": 0}

        free = 0
        for row in self.data:
            price = self._to_float(row.get("Price"))
            if price <= 0.0:
                free += 1
        paid = total - free

        return {
            "total": total,
            "gratuitos_%": round((free / total) * 100, 2),
            "pagos_%": round((paid / total) * 100, 2),
            "gratuitos_qtd": free,
            "pagos_qtd": paid
        }

    # ---------- P2: ano(s) com mais lançamentos ----------

    def top_years_by_releases(self) -> List[int]:
        """
        Retorna lista com o(s) ano(s) que tiveram maior número de lançamentos.
        Em caso de empate, retorna todos (ordenados).
        """
        counts: Dict[int, int] = defaultdict(int)
        for row in self.data:
            y = self._extract_year(row.get("Release date"))
            if y is not None:
                counts[y] += 1

        if not counts:
            return []

        max_val = max(counts.values())
        winners = [y for (y, c) in counts.items() if c == max_val]
        winners.sort()
        return winners

    def year_histogram(self) -> List[Tuple[int, int]]:
        """Retorna [(ano, contagem)] ordenado por contagem desc, ano asc (útil p/ explicar P2)."""
        counts: Dict[int, int] = defaultdict(int)
        for row in self.data:
            y = self._extract_year(row.get("Release date"))
            if y is not None:
                counts[y] += 1
        return sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    # ---------- P3: compatibilidade por SO ----------

    def os_compatibility(self) -> Dict[str, Tuple[int, float]]:
        """
        Retorna a contagem e percentual por sistema:
            {
              "Windows": (qtd, pct),
              "Mac": (qtd, pct),
              "Linux": (qtd, pct),
              "total": int
            }
        """
        total = len(self.data)
        w = m = l = 0
        for row in self.data:
            if self._to_bool(row.get("Windows")): w += 1
            if self._to_bool(row.get("Mac")):     m += 1
            if self._to_bool(row.get("Linux")):   l += 1

        def pct(x): return round((x / total) * 100, 2) if total else 0.0

        return {
            "total": total,
            "Windows": (w, pct(w)),
            "Mac": (m, pct(m)),
            "Linux": (l, pct(l))
        }

    def multi_os_summary(self) -> Dict[str, float]:
        """
        Retorna resumo multi-OS:
            {
              "total": int,
              "multi_qtd": int, "multi_%": float,
              "single_qtd": int, "single_%": float,
              "zero_qtd": int, "zero_%": float
            }
        """
        total = len(self.data)
        multi = single = zero = 0
        for row in self.data:
            s = int(self._to_bool(row.get("Windows"))) \
                + int(self._to_bool(row.get("Mac"))) \
                + int(self._to_bool(row.get("Linux")))
            if s >= 2:
                multi += 1
            elif s == 1:
                single += 1
            else:
                zero += 1

        def pct(x): return round((x / total) * 100, 2) if total else 0.0

        return {
            "total": total,
            "multi_qtd": multi, "multi_%": pct(multi),
            "single_qtd": single, "single_%": pct(single),
            "zero_qtd": zero, "zero_%": pct(zero)
        }

    def most_compatible_os(self) -> Tuple[str, int, float]:
        """
        Retorna (nome_do_sistema, qtd, percent) do sistema mais compatível.
        """
        dist = self.os_compatibility()
        winners = []
        for os_name in ("Windows", "Mac", "Linux"):
            qty, pct = dist[os_name]
            winners.append((os_name, qty, pct))
        winners.sort(key=lambda t: (-t[1], -t[2], t[0]))
        return winners[0]
