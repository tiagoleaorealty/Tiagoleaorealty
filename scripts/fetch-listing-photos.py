#!/usr/bin/env python3
"""Save the hero photo of each listing featured in the under-$500K blog post.

The photos are Tiago's own real estate photography, served through the MLS
media feed on the KRAIN listing pages. The feed's URLs carry signed tokens and
rotate, so the post cannot link to them directly — this copies each hero shot
into listing-photos/ at card size, and the post references the local files.

Run from the repo root:  python3 scripts/fetch-listing-photos.py
Re-running is safe; it overwrites what is already there.
"""
import os
import subprocess
import urllib.request

BASE = "https://api.cotality.com/trestle/Media/Property/PHOTO-jpeg/"
OUT_DIR = "listing-photos"
CARD_WIDTH = 720  # 2x the 240px card, enough for retina screens

PHOTOS = {
    # Tamarindo
    "casa-moana": "1189379321/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4ODM5NzQ0Mw/qByoPYOMjumKqc_nXMXykg4iKfc6TPyPaHornl3VNEs",
    "la-esquina-3": "1147273158/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4ODU3MDMxNw/8bgdCtAE0tvOl4f0MfmB3CdoAJgtToeyniJFpXkYq5I",
    "villa-verde-i-3": "1157631451/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4OTAwMjQwNw/oC4RgS3q02RIAPF7TWy13g30SNJlqcQibRIPeVEcQZk",
    "villa-verde-i": "1174660379/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NTI4NzQwMQ/OjEz32aRgl5dVsEgKBuHyteJHVy75S8GUrAYp7ttp_Y",
    "boca-raca-9": "1177634204/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NzM2MDQ1Nw/RD4voxYddeULDFZUdcE9Xue4LXEb3FPsf1_Y4ENEYTw",
    # Potrero / Flamingo
    "flamingo-marina-cove-619": "1169350666/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NzM2MDUyOA/M9jC05iRRJqmowY7I3J9592nJbHHngxTCLhVZMmR2RM",
    "casa-maravilla": "1137616258/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NjA2NTAzMg/8J9wz6e1bl0OVYi7qD05_lwM1r7yeySHZ36BPvvAk7g",
    # Playas del Coco
    "papagayo-3br-condo": "1120210688/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NjE1MTM3NA/UZCaYlf45GvjfDfABN9oENOmlrENGAvzCaVaSF3FPKA",
    "house-of-winds-3": "1107274228/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4OTE3NTAxOA/Q61xBbze5ane7SylUB9NjyeftSZfsrG2ouLfHerpDFA",
    "monte-seca-casa-luma": "1153543817/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4OTkyNDcxMQ/gyNThbEdV1xiLJgFcu4BASA-sbmefVfcQUc2TQGGJu4",
    "pacifico-c509": "1168447804/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NTk3ODQzMQ/M_6JpOnV0Ntkvr4cgc3o_CWoI349WIprPG6CQk3czQc",
    "coco-cliffs-vista-marina": "1114271883/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4NTk3ODkyNg/fZF2K3y-VXRxAuRAUN6pqkl0vZy0LzIyAu_7YKyXrH4",
    "vista-marina-bella-luna": "1168445655/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4OTkwMTg1Nw/Wn6NbbnGFJbQ0HPQZuMenqPOoRy10T_1JmYcUoGeElw",
    "la-finca-blanca": "1176273017/1/MzM2Ny8yMTY3LzE3/MTcvMTUyMTYvMTc4OTI2MTQyMw/NQMtu_2uqC-xHeYJBFmTpGrph6qIVHWMvEbZEjMvx3c",
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, path in sorted(PHOTOS.items()):
        out = os.path.join(OUT_DIR, name + ".jpg")
        tmp = out + ".full"
        req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
        with open(tmp, "wb") as f:
            f.write(raw)
        # sips ships with macOS; no Node or Pillow on this machine.
        subprocess.run(
            ["sips", "-Z", str(CARD_WIDTH), "-s", "format", "jpeg",
             "-s", "formatOptions", "60", tmp, "--out", out],
            capture_output=True, check=True,
        )
        os.remove(tmp)
        print(f"{name:26} {len(raw) // 1024:>4} KB  ->  {os.path.getsize(out) // 1024:>3} KB")


if __name__ == "__main__":
    main()
