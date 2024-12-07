import asyncio
import os
import shutil
from pathlib import Path
import logging
import argparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def copy_file(file_path: Path, target_folder: Path):
    """Копіює файл до цільової папки на основі розширення."""
    try:
        extension = file_path.suffix.lower().strip('.')
        target_dir = target_folder / extension

        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / file_path.name
        shutil.copy2(file_path, target_path)
        logging.info(f"Файл {file_path} скопійовано до {target_path}")
    except Exception as e:
        logging.error(f"Помилка копіювання файлу {file_path}: {e}")

async def read_folder(source_folder: Path, target_folder: Path):
    """Рекурсивно читає файли з вихідної папки та копіює їх."""
    tasks = []

    for root, _, files in os.walk(source_folder):
        for file_name in files:
            file_path = Path(root) / file_name
            tasks.append(copy_file(file_path, target_folder))
    
    await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням")
    parser.add_argument("source", type=str, help="Вихідна папка")
    parser.add_argument("target", type=str, help="Цільова папка")
    args = parser.parse_args()

    source_folder = Path(args.source)
    target_folder = Path(args.target)

    if not source_folder.is_dir():
        logging.error("Вихідна папка не існує або не є директорією")
        return

    if not target_folder.exists():
        target_folder.mkdir(parents=True)

    asyncio.run(read_folder(source_folder, target_folder))

if __name__ == "__main__":
    main()
