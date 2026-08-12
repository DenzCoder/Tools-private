# VIP Tools — Termux Admin Upgrade

Versi ini tidak memakai `tkinter`, jadi bisa dijalankan di Termux/Android.

## Jalankan

```bash
cd /sdcard/tools
pip install -r requirements.txt
python app.py
```

Login menggunakan akun admin dari API Vercel.

## Admin Panel

Setelah login admin, pilih menu `99`.

Fitur:
- Dashboard / statistik
- List customer
- Create customer
- Extend license
- Reset device
- Suspend / activate
- Delete customer
- Activity log

Tidak ada fitur customer untuk mengganti password, reset device, suspend, atau mengelola akun sendiri. Semua pengelolaan dilakukan admin.

## API

Default:
`https://api-endpoint-denz.vercel.app/api`

Bisa diganti:

```bash
export API_BASE_URL="https://api-endpoint-denz.vercel.app/api"
```

`VIP_API_URL` juga dapat dipakai oleh modul UI jika dibutuhkan.
