# Final Project Pemrograman Jaringan

## Informasi Game Kewan War 
Judul: Kewan War
Tipe FP: Multiplayer Game
Deskripsi: Kewan War adalah game multiplayer yang dapat dimainkan di terminal oleh banyak player di room berbeda selama player terkoneksi pada jaringan yang sama dengan server.
Player harus memiliki source code [client.py](./client.py).

## Cara Bermain sebagai Player

Untuk bermain sebagai Player, kita bisa menjalankan **server.py** terlebih dahulu. Setelah itu siapkan minimal 2 user atau pemain dan kelipatannya agar dapat bermain di room yang berbeda. Contoh penerapannya seperti berikut.

<p align="center">
  <img src="img/cara_main.png">
</p>

Pada gambar tersebut kita telah membuat 2 user atau player bermain di dalam satu ruangan yang sama, sebelum memilih **Kewan**, player diharuskan untuk menginput username terlebih dahulu seperti gambar berikut.

<p align="center">
  <img src="img/username.png">
</p>

Setelah semua player telah memiliki usernamenya masing-masing, player tersebut dapat memilih kewan yang tersedia. Untuk memilih kewan tersebut, player diharuskan untuk menginput **Nama** dari **Kewan** itu sendiri seperti gambar berikut ini

<p align="center">
  <img src="img/kewan.png">
</p>

Setiap kewan memiliki kekuatan yang berbeda-beda, di mana terdapat 2 tipe serangan untuk setiap kewan, yaitu **Basic Attack** dan **Random Skill**. Player I akan memperoleh giliran pertama dalam permainan dan Player II akan memperoleh giliran setelahnya. 

<p align="center">
  <img src="img/giliran.png">
</p>

Selamat Bermain

## Cara Hosting sebagai Server

Untuk Hosting sebagai Server, hubungkan satu laptop ke jaringan internet yang tidak memiliki banyak pengakses, contohnya seperti hotspot hp. 

<p align="center">
  <img src="img/hotspot.png">
</p>

Setelah itu, atur konfigurasi IP pada server melalui **server.conf**, kita bisa mendapatkan IP dengan menggunakan command *ipconfig*.

<p align="center">
  <img src="img/ipconfig.png">
</p>

<p align="center">
  <img src="img/serverconf.jpg">
</p>

Setelah server telah ter set-up, kita siapkan 2 laptop berbeda agar menjadi client atau player pada permainan. Kita harus menyamakan IP pada client sama dengan IP pada server agar dapat bermain di dalam satu room. Setelah semua client terset-up, kita bisa memainkan game tersebut di laptop masing-masing. Selamat Bermain!!

