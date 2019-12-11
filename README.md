Untuk menjalankan, name server harus dinyalakan dulu pada dua port
pyro4-ns -n <IP address> -p 7777 dan pyro4-ns -n <IP address> -p 7778
gunakan URI untuk referensi name server yang akan digunakan

----

![Arsitektur app](https://github.com/mailsyarief/fp_sister_19/blob/master/arsitektur.png)

PLAYER 1
Untuk menjalankan program sebagai player 1, nyalakan dulu server dan manager pada folder manager/server/s1 (untuk server 1)
python server.py
python manager.py

client:
jalankan pada folder manager/clients/c1
python client.py

PLAYER 2
Untuk menjalankan program sebagai player 2, nyalakan dulu server dan manager pada folder manager/server/s2 (untuk server 2)
python server.py
python manager.py

client:
jalankan pada folder manager/clients/c2
python client.py

SPECTATOR
Untuk menjalankan program sebagai spectator, nyalakan dulu server dan manager pada folder manager/server/s3 (untuk server 3)
python server.py
python manager.py

client:
jalankan pada folder manager/clients/c3
python client.py
---

TESTCASE
1. c1 mati, c1 masuk, permainan masih berlanjut
2. c2 mati, c2 masuk, permainan masih berlanjut
3. c3 mati, c3 masuk, permainan masih berlanjut

4. s1 mati, semua player masih bisa bermain
5. s2 mati, semua player masih bisa bermain
6. s3 mati, semua player masih bisa bermain

7. c1 quit, c3 bermain