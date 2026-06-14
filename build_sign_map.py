import os, json

PROJECT_ROOT = os.path.dirname(__file__)
WLASL_DIR = os.path.join(PROJECT_ROOT, "wlasl")
VIDEOS_DIR = os.path.join(WLASL_DIR, "videos")  # check this folder has mp4s
ANNOT_PATH = os.path.join(WLASL_DIR, "WLASL_v0.3.json")
OUTPUT_JSON = os.path.join(PROJECT_ROOT, "sign_map.json")

# 1) Index local videos
id_to_relpath = {}
for root, _, files in os.walk(VIDEOS_DIR):
    for f in files:
        if f.lower().endswith(".mp4"):
            vid = os.path.splitext(f)[0]
            full = os.path.join(root, f)
            rel = os.path.relpath(full, PROJECT_ROOT).replace("\\","/")
            id_to_relpath[vid] = rel

print("Indexed", len(id_to_relpath), "local mp4 files")

# 2) Map gloss -> first available mp4
with open(ANNOT_PATH, "r", encoding="utf-8") as fh:
    data = json.load(fh)

word_to_path = {}
missing = 0
for entry in data:
    gloss = entry.get("gloss", "").strip().lower()
    found = None
    for inst in entry.get("instances", []):
        vid = str(inst.get("video_id"))
        if vid in id_to_relpath:
            found = id_to_relpath[vid]
            break
    if found:
        word_to_path[gloss] = found
    else:
        missing += 1

with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
    json.dump(word_to_path, out, ensure_ascii=False, indent=2)

print("Wrote", len(word_to_path), "mappings to", OUTPUT_JSON, "Missing:", missing)
