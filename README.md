# TubesSweeper
Minesweeper AI yang dibuat dengan Python dan CLIPS.

## User Manual

### Requirement
1. Python 3
2. PyQT5
3. clipspy

### Instalasi
1. Install Python 3 dengan mengikuti petunjuk di [halaman download Python 3.](https://www.python.org/downloads/)
2. Install PyQT5 dengan mengikuti petunjuk di [halaman pypi untuk PyQT5.](https://pypi.org/project/PyQt5/)
3. Install clipspy dengen menjalankan perintah berikut:
   ```
   pip install clipspy
   ```
4. Download kode yang ada di github ini lalu letakkan kode di suatu direktori.
5. Buka direktori kode, lalu jalankan perintah penggunaan.

### Penggunaan
Aplikasi dapat dimulai dalam 3 mode penerimaan masukan pengaturan awal:
1. Input dari GUI
   
    Perintah:
    ```
    python main.py
    ```
2. Input dari *Console*

    Perintah:
    ```
    python main.py --no-gui
    ```
3. Input dari File

    Perintah:
    ```
    python main.py -f /path/to/file.txt
    ```
    Contoh isi dari `file.txt`:
    ```
    4
    2
    1,1
    2,2
    ```
Setelah aplikasi dimulai, gunakan tombol `Run Satu Iterasi` untuk menjalankan satu *rule* pada CLIPS atau tombol `Run Hingga Selesai` untuk menjalankan CLIPS hingga tidak ada *rule* yang bisa diaktivasi.

Tombol `Restart` dapat digunakan untuk mengulang aplikasi ke keadaan awal.

## Dokumentasi
Struktur file aplikasi ini adalah sebagai berikut.
```
1.  /clips/tubessweeper.clp
2.  /gui/input_dialog.py
    /gui/input_dialog.ui
3.  /gui/main_window.py
    /gui/main_window.ui
4.  /src/ai.py
5.  /src/input.py
6.  /main.py
```
Berikut penjelasan kode yang ada pada tiap file.
1.  `/clips/tubessweeper.clp`
    
    File ini berisi kode CLIPS yang digunakan sebagai kerangka bagian KBS aplikasi.

2.  `/gui/input_dialog.py` dan `/gui/input_dialog.ui`
    
    Dua file ini berisi *layout* tampilan yang digunakan untuk menerima masukan aplikasi beserta kode yang menyambungkan Python dengan tampilan.

3.  `/gui/main_window.py` dan `/gui/main_window.ui`
    
    Dua file ini berisi *layout* tampilan utama aplikasi beserta kode yang menyambungkan Python dengan tampilan.

4.  `/src/ai.py`
    
    File ini berisi kode yang menghubungkan aplikasi Python dengan bagian kode CLIPS.

5.  `/src/input.py`
    
    File ini berisi kode yang bertanggung jawab membaca masukan pengguna.

6.  `/main.py`
    
    File ini berisi kode alur utama penjalanan aplikasi
  
  
## Kelompok 8 - TubesSweeper
1. 13518112 - M Fauzan Al-G
2. 13518130 - Ryan Daniel
3. 13518136 - Reyvan Rizky I
4. 13518148 - M Rizky Ismail F
