import os.path
import subprocess

def make_preview(original_path):
    """add make_preview function"""
    filename = os.path.basename(original_path)
    preview_path = f"storage/previews/{filename}"
    subprocess.run(["ffmpeg", "-y", "-i", original_path, "-t", "30", "-c", "copy", preview_path])
    return preview_path