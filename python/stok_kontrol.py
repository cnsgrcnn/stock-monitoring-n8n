"""CLI demonstration of the decision rules in the n8n stock-monitoring project."""
from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "data" / "sample_inventory.csv"


def classify(material: dict[str, str]) -> str:
    code = material.get("malzeme_kodu", "").strip()
    try:
        stock = Decimal(material.get("mevcut_stok", ""))
        threshold = Decimal(material.get("kritik_seviye", ""))
    except (InvalidOperation, TypeError):
        return "HATALI VERI"
    if not code or not stock.is_finite() or not threshold.is_finite():
        return "HATALI VERI"
    if stock < 0 or threshold < 0:
        return "HATALI VERI"
    return "KRITIK STOK" if stock <= threshold else "NORMAL STOK"


def main() -> None:
    counts = {"KRITIK STOK": 0, "NORMAL STOK": 0, "HATALI VERI": 0}
    with SAMPLE_CSV.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    for material in rows:
        result = classify(material)
        counts[result] += 1
        print(f"{material['malzeme_kodu']}: {result}")

    print("\nSTOK OZET RAPORU")
    print(f"Toplam: {len(rows)}")
    print(f"Kritik: {counts['KRITIK STOK']}")
    print(f"Normal: {counts['NORMAL STOK']}")
    print(f"Hatali: {counts['HATALI VERI']}")


if __name__ == "__main__":
    main()
