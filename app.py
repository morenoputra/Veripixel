"""
app.py
Aplikasi web VeriPixel: upload gambar -> prediksi EfficientNet-B0 -> visualisasi
Grad-CAM -> simpan & tampilkan riwayat deteksi (SQLite).
"""

import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

import db
import inference

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXT = {"jpg", "jpeg", "png"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB, samakan dengan teks di halaman upload

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "ganti-dengan-kunci-rahasia-anda")
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_DIR, exist_ok=True)
db.init_db()

BULAN_ID = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


@app.template_filter("format_date_id")
def format_date_id(value):
    """Filter Jinja: '2026-07-20T14:05:00' -> '20 Juli 2026, 14:05 WIB'."""
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return value
    return f"{dt.day} {BULAN_ID[dt.month - 1]} {dt.year}, {dt.strftime('%H:%M')} WIB"


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def _remove_detection_files(item):
    for fname in (item["original_filename"], item["gradcam_filename"]):
        fpath = os.path.join(UPLOAD_DIR, fname)
        if os.path.exists(fpath):
            os.remove(fpath)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None

    if request.method == "POST":
        file = request.files.get("file")

        if file is None or file.filename == "":
            error = "Silakan pilih file gambar terlebih dahulu."
        elif not _allowed_file(file.filename):
            error = "Format file tidak didukung. Gunakan JPG, JPEG, atau PNG."
        else:
            temp_path = os.path.join(UPLOAD_DIR, f"tmp_{uuid_suffix()}_{file.filename}")
            file.save(temp_path)
            try:
                result = inference.predict_and_gradcam(temp_path, UPLOAD_DIR)
                db.insert_detection(
                    original_filename=result["original_filename"],
                    gradcam_filename=result["gradcam_filename"],
                    label=result["label"],
                    confidence=result["confidence"],
                    created_at=datetime.now().isoformat(timespec="seconds"),
                )
            except FileNotFoundError as e:
                error = str(e)
            except Exception as e:  # noqa: BLE001 - ditampilkan apa adanya ke pengguna
                error = f"Terjadi kesalahan saat memproses gambar: {e}"
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    history = db.get_all_detections()

    return render_template(
        "index.html",
        error=error,
        label=result["label"] if result else None,
        confidence=result["confidence"] if result else None,
        original_img=result["original_filename"] if result else None,
        gradcam_img=result["gradcam_filename"] if result else None,
        history=history,
    )


@app.route("/history/clear", methods=["POST"])
def clear_history():
    for item in db.get_all_detections():
        _remove_detection_files(item)
    db.clear_all_detections()
    return redirect(url_for("index") + "#history")


@app.route("/history/<int:detection_id>/delete", methods=["POST"])
def delete_history_item(detection_id):
    item = db.get_detection(detection_id)
    if item:
        _remove_detection_files(item)
        db.delete_detection(detection_id)
    return redirect(url_for("index") + "#history")


def uuid_suffix():
    import uuid

    return uuid.uuid4().hex[:8]


if __name__ == "__main__":
    app.run(debug=True)
