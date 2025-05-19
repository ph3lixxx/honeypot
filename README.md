![BLUE Banner](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNm9meTN4c2Fjb290M3k0YmRreHQ4Y3IzOHZydWlkMncxdG91cjNhZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FjfeL5TcB1y70dkT4p/giphy.gif)
# Web Honeypot Clone

Honeypot ini dibuat untuk menangkap aktivitas penyerang yang mencoba mengakses halaman clone dari situs asli. Semua request dicatat lengkap.

## Menjalankan
```bash
pip install -r requirements.txt
python run.py

## Clone the Website
'''bash
sudo apt install httrack
httrack "https://target.com" -O /home/felix/clone-target target.com -v  
