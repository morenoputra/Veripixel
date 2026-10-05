"""
inference.py
Memuat model EfficientNet-B0 hasil training (lihat notebook skripsi) dan menjalankan
prediksi real-vs-AI beserta visualisasi Grad-CAM untuk satu gambar input.

Letakkan file bobot hasil training (mis. model_efficientnet_b0.pth) di folder model/,
atau set environment variable MODEL_PATH ke lokasi file tersebut.
"""

import os
import uuid

import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMG_SIZE = 224
# Index 0/1 mengikuti torchvision ImageFolder (urutan alfabetis): FAKE=0, REAL=1
CLASS_NAMES = ["AI-Generated", "Real Image"]

MODEL_PATH = os.environ.get(
    "MODEL_PATH", os.path.join(BASE_DIR, "model", "model_efficientnet_b0.pth")
)

_transform = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

# State global: model di-load sekali saja (lazy-loaded saat request pertama masuk)
_model = None
_activations = {}
_gradients = {}


def _build_architecture():
    """Struktur model harus identik dengan yang dipakai saat training di notebook."""
    model = models.efficientnet_b0(weights=None)
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, 1)
    return model


def load_model():
    """Memuat bobot model + memasang hook Grad-CAM pada layer konvolusi terakhir."""
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"File bobot model tidak ditemukan di '{MODEL_PATH}'. "
            "Salin file .pth hasil training dari notebook skripsi ke folder model/."
        )

    model = _build_architecture()
    state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(state_dict)
    model.to(DEVICE)
    model.eval()

    # Layer target Grad-CAM: blok konvolusi terakhir sebelum global pooling
    target_layer = model.features[-1]

    def forward_hook(module, inp, out):
        _activations["value"] = out

    def backward_hook(module, grad_in, grad_out):
        _gradients["value"] = grad_out[0]

    target_layer.register_forward_hook(forward_hook)
    target_layer.register_full_backward_hook(backward_hook)

    _model = model
    return _model


def _compute_gradcam(logit):
    """Menghitung heatmap Grad-CAM (0-1) dari aktivasi & gradien layer target."""
    _model.zero_grad(set_to_none=True)
    logit.backward(retain_graph=True)

    gradients = _gradients["value"][0]     # (C, H, W)
    activations = _activations["value"][0]  # (C, H, W)

    weights = gradients.mean(dim=(1, 2))    # rata-rata gradien per channel -> (C,)
    cam = torch.relu((weights[:, None, None] * activations).sum(dim=0))
    cam = cam.detach().cpu().numpy()

    cam -= cam.min()
    if cam.max() > 1e-8:
        cam /= cam.max()
    cam = cv2.resize(cam, (IMG_SIZE, IMG_SIZE))
    return cam


def _overlay_heatmap(original_rgb, cam, alpha=0.45):
    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    overlay = (alpha * heatmap + (1 - alpha) * original_rgb).astype(np.uint8)
    return overlay


def predict_and_gradcam(image_path, upload_dir):
    """
    Menjalankan pipeline lengkap: load gambar -> prediksi -> Grad-CAM -> simpan hasil.
    Mengembalikan dict berisi label, confidence (%), dan nama file gambar asli & heatmap
    (keduanya sudah disimpan di upload_dir).
    """
    model = load_model()

    image = Image.open(image_path).convert("RGB")
    image_resized = image.resize((IMG_SIZE, IMG_SIZE))
    original_np = np.array(image_resized)

    input_tensor = _transform(image).unsqueeze(0).to(DEVICE)
    input_tensor.requires_grad_(True)

    logit = model(input_tensor)
    prob_real = torch.sigmoid(logit).item()

    if prob_real >= 0.5:
        label = CLASS_NAMES[1]
        confidence = prob_real * 100
    else:
        label = CLASS_NAMES[0]
        confidence = (1 - prob_real) * 100

    cam = _compute_gradcam(logit[0])
    overlay = _overlay_heatmap(original_np, cam)

    unique_id = uuid.uuid4().hex[:10]
    original_filename = f"{unique_id}_original.jpg"
    gradcam_filename = f"{unique_id}_gradcam.jpg"

    Image.fromarray(original_np).save(os.path.join(upload_dir, original_filename), quality=92)
    Image.fromarray(overlay).save(os.path.join(upload_dir, gradcam_filename), quality=92)

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "original_filename": original_filename,
        "gradcam_filename": gradcam_filename,
    }
