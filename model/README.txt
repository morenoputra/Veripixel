Letakkan file bobot hasil training di sini, misalnya:

    model_efficientnet_b0.pth

File ini adalah output dari CONFIG["final_model_path"] pada notebook training
(Skripsi_Training_EfficientNet_*.ipynb) — biasanya dihasilkan dari sel terakhir
("10. Simpan & Unduh Model Final") lalu diunduh dari Google Colab.

Jika nama file atau lokasinya berbeda, set environment variable MODEL_PATH,
contoh (Linux/Mac):

    export MODEL_PATH=/path/ke/model_anda.pth
    python app.py

atau (Windows PowerShell):

    $env:MODEL_PATH = "C:\path\ke\model_anda.pth"
    python app.py
