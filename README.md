# tubessweeper
Minesweeper AI yang dibuat dengan Python dan CLIPS.

## User Manual

### Requirement
1. Python 3
2. PyQT5
3. clipspy

### Instalasi
...

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
...
