// main.js — interaksi ringan untuk form upload VeriPixel

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file");
    const fileNameEl = document.getElementById("fileName");
    const dropzone = document.getElementById("dropzone");
    const form = document.getElementById("uploadForm");
    const submitBtn = document.getElementById("submitBtn");

    if (!fileInput || !dropzone) return;

    fileInput.addEventListener("change", function () {
        if (fileInput.files && fileInput.files.length > 0) {
            fileNameEl.textContent = fileInput.files[0].name;
        } else {
            fileNameEl.textContent = "Belum ada file dipilih";
        }
    });

    ["dragenter", "dragover"].forEach((evt) => {
        dropzone.addEventListener(evt, function (e) {
            e.preventDefault();
            dropzone.classList.add("vp-dropzone-active");
        });
    });

    ["dragleave", "drop"].forEach((evt) => {
        dropzone.addEventListener(evt, function (e) {
            e.preventDefault();
            dropzone.classList.remove("vp-dropzone-active");
        });
    });

    dropzone.addEventListener("drop", function (e) {
        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            fileInput.files = files;
            fileNameEl.textContent = files[0].name;
        }
    });

    if (form && submitBtn) {
        form.addEventListener("submit", function () {
            submitBtn.disabled = true;
            submitBtn.textContent = "Menganalisis...";
        });
    }
});
