"""Display installed distribution inventory without exposing configuration."""
from importlib.metadata import distributions
from pathlib import Path
import csv

PURPOSE = {"pip": "Python package installer", "setuptools": "Python packaging tools", "wheel": "Build wheel distributions"}
def rows():
    return sorted((d.metadata.get("Name", "unknown"), d.version, PURPOSE.get(d.metadata.get("Name", "").lower(), "Installed environment package")) for d in distributions())
def main():
    result = rows()
    print("Package | Version | Purpose")
    for row in result: print(" | ".join(row))
    target = Path(__file__).resolve().parents[1] / "docs" / "dependency-inventory.csv"
    with target.open("w", newline="", encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["package","version","purpose"]); w.writerows(result)
    print(f"\nInventory saved to {target}")
if __name__ == "__main__": main()
