from pathlib import Path
import shutil


def main():
    target = Path("./data/processed/chroma")
    if target.exists():
        shutil.rmtree(target)
        print(f"Removed {target}")
    else:
        print(f"Nothing to remove at {target}")


if __name__ == "__main__":
    main()
