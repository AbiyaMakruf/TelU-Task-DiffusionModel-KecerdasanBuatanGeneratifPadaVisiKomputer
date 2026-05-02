#!/usr/bin/env python3
"""
Script untuk menyisakan gambar dalam folder images/ sebanyak yang ditentukan.
Gambar yang dihapus dipilih secara acak.
"""

import os
import random
import sys
from pathlib import Path
from typing import List


def get_image_files(folder_path: str) -> List[Path]:
    """
    Mendapatkan semua file gambar dalam folder.
    Mendukung format: jpg, jpeg, png, gif, bmp, webp, tiff
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder '{folder_path}' tidak ditemukan.")
    
    image_files = [
        file for file in folder.rglob('*')
        if file.is_file() and file.suffix.lower() in image_extensions
    ]
    
    return image_files


def keep_images(folder_path: str, count: int, dry_run: bool = False) -> None:
    """
    Menyisakan N gambar, sisanya dihapus secara acak.
    
    Args:
        folder_path: Path ke folder yang berisi gambar
        count: Jumlah gambar yang ingin disimpan
        dry_run: Jika True, tampilkan apa yang akan dihapus tanpa benar-benar menghapus
    """
    image_files = get_image_files(folder_path)
    
    if len(image_files) == 0:
        print("❌ Tidak ada gambar yang ditemukan dalam folder.")
        return
    
    if count >= len(image_files):
        print(f"✅ Folder sudah memiliki {len(image_files)} gambar.")
        print(f"   Jumlah yang ingin disimpan: {count}")
        print(f"   Tidak ada gambar yang perlu dihapus.")
        return
    
    # Pilih gambar secara acak untuk dihapus
    files_to_delete = random.sample(image_files, len(image_files) - count)
    
    print(f"📊 Total gambar: {len(image_files)}")
    print(f"📌 Gambar yang akan disimpan: {count}")
    print(f"🗑️  Gambar yang akan dihapus: {len(files_to_delete)}")
    print()
    
    if dry_run:
        print("🔍 Mode DRY RUN - Tidak ada file yang dihapus")
        print("Gambar yang akan dihapus:")
        for i, file in enumerate(files_to_delete, 1):
            print(f"  {i}. {file.relative_to(folder_path)}")
    else:
        print("🗑️  Menghapus gambar...")
        for i, file in enumerate(files_to_delete, 1):
            try:
                file.unlink()  # Hapus file
                print(f"  ✓ [{i}/{len(files_to_delete)}] Dihapus: {file.name}")
            except Exception as e:
                print(f"  ✗ Gagal menghapus {file.name}: {e}")
        
        print(f"\n✅ Selesai! {len(files_to_delete)} gambar telah dihapus.")
        print(f"   Gambar tersisa: {count}")


def main():
    """Main function"""
    # Gunakan folder images di directory saat ini
    default_folder = Path(__file__).parent / "images"
    
    # Tanyakan ke user
    print("=" * 60)
    print("🖼️  SCRIPT PENYISAAN GAMBAR")
    print("=" * 60)
    print()
    
    # Input folder
    folder_input = input(f"Masukkan path folder [default: {default_folder}]: ").strip()
    folder_path = folder_input if folder_input else str(default_folder)
    
    # Validasi folder
    try:
        image_files = get_image_files(folder_path)
        print(f"✅ Ditemukan {len(image_files)} gambar\n")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Input jumlah gambar yang ingin disimpan
    while True:
        try:
            keep_count = int(input(f"Berapa banyak gambar yang ingin disimpan? (1-{len(image_files)}): "))
            if 1 <= keep_count <= len(image_files):
                break
            else:
                print(f"❌ Masukkan angka antara 1 dan {len(image_files)}")
        except ValueError:
            print("❌ Masukkan angka yang valid")
    
    print()
    
    # Tanyakan dry run
    dry_run_input = input("Lakukan dry run terlebih dahulu? (y/n) [default: y]: ").strip().lower()
    dry_run = dry_run_input != 'n'
    
    print()
    keep_images(folder_path, keep_count, dry_run=dry_run)
    
    # Jika dry run, tanyakan apakah lanjut dengan penghapusan sebenarnya
    if dry_run:
        print()
        confirm = input("\nLanjutkan dengan penghapusan sebenarnya? (y/n): ").strip().lower()
        if confirm == 'y':
            print()
            keep_images(folder_path, keep_count, dry_run=False)


if __name__ == "__main__":
    main()
