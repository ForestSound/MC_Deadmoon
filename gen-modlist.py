#!/usr/bin/env python3
"""Genere MODS.md depuis les metadonnees packwiz du dossier pack/.

Usage : python3 gen-modlist.py
Les numeros de version viennent de l'API Modrinth ; pour les mods CurseForge,
ils sont lus dans le nom du jar (packwiz ne stocke pas le numero).
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACK = ROOT / "pack"
UA = {"User-Agent": "MC_Deadmoon-modlist/1.0 (github.com/ForestSound/MC_Deadmoon)"}


def api(path):
    req = urllib.request.Request("https://api.modrinth.com/v2" + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def read_entry(path):
    """Extrait d'un .pw.toml ce dont on a besoin, sans dependance TOML externe."""
    txt = path.read_text(encoding="utf-8")

    def one(key):
        m = re.search(r'^%s\s*=\s*"([^"]*)"' % key, txt, re.M)
        return m.group(1) if m else None

    def num(key):
        m = re.search(r"^%s\s*=\s*(\d+)" % key, txt, re.M)
        return m.group(1) if m else None

    return {
        "slug": path.stem,
        "name": one("name") or path.stem,
        "filename": one("filename") or "",
        "side": one("side") or "both",
        "mr_project": one("mod-id"),
        "mr_version": one("version"),
        "cf_project": num("project-id"),
        "cf_file": num("file-id"),
    }


def version_from_filename(fn):
    """Derniere sequence qui ressemble a un numero de version dans le nom du jar."""
    stem = re.sub(r"\.(jar|zip)$", "", fn)
    cands = re.findall(r"\d+(?:\.\d+)+(?:[-+][A-Za-z0-9.]+)?", stem)
    cands = [c for c in cands if c not in ("1.21.1", "1.21", "1.20.1")] or cands
    if not cands:
        return "—"
    # "1.21.1-4.2.4" -> "4.2.4" : on jette le prefixe de version Minecraft
    return re.sub(r"^1\.2[01](?:\.\d+)?[-+]", "", cands[-1])


def enrich_modrinth(entries):
    """Complete version_number et url pour toutes les entrees Modrinth, en deux appels."""
    vids = sorted({e["mr_version"] for e in entries if e["mr_version"]})
    pids = sorted({e["mr_project"] for e in entries if e["mr_project"]})
    versions, projects = {}, {}
    for chunk in (vids[i:i + 100] for i in range(0, len(vids), 100)):
        q = urllib.parse.quote(json.dumps(chunk))
        for v in api("/versions?ids=" + q):
            versions[v["id"]] = v["version_number"]
    for chunk in (pids[i:i + 100] for i in range(0, len(pids), 100)):
        q = urllib.parse.quote(json.dumps(chunk))
        for p in api("/projects?ids=" + q):
            projects[p["id"]] = p["slug"]
    for e in entries:
        if not e["mr_project"]:
            continue
        e["version"] = versions.get(e["mr_version"]) or version_from_filename(e["filename"])
        slug = projects.get(e["mr_project"])
        e["url"] = f"https://modrinth.com/project/{slug}" if slug else None
        e["source"] = "Modrinth"


def collect(folder):
    entries = [read_entry(p) for p in sorted((PACK / folder).glob("*.pw.toml"))]
    for e in entries:
        if e["cf_project"]:
            e["version"] = version_from_filename(e["filename"])
            e["url"] = f"https://www.curseforge.com/projects/{e['cf_project']}"
            e["source"] = "CurseForge"
    enrich_modrinth(entries)
    entries.sort(key=lambda e: e["name"].lstrip("[").lower())
    return entries


def table(entries, with_side=True):
    head = "| Mod | Version | Côté | Source |" if with_side else "| Shaderpack | Version | Source |"
    rule = "|---|---|---|---|" if with_side else "|---|---|---|"
    out = [head, rule]
    for e in entries:
        name = f"[{e['name']}]({e['url']})" if e.get("url") else e["name"]
        src = f"{e['source']}"
        side = {"both": "client + serveur", "client": "**client seul**", "server": "serveur seul"}
        if with_side:
            out.append(f"| {name} | `{e['version']}` | {side[e['side']]} | {src} |")
        else:
            out.append(f"| {name} | `{e['version']}` | {src} |")
    return "\n".join(out)


def main():
    pack_toml = (PACK / "pack.toml").read_text(encoding="utf-8")
    pv = re.search(r'^version\s*=\s*"([^"]+)"', pack_toml, re.M).group(1)
    mc = re.search(r'^minecraft\s*=\s*"([^"]+)"', pack_toml, re.M).group(1)
    neo = re.search(r'^neoforge\s*=\s*"([^"]+)"', pack_toml, re.M).group(1)

    mods = collect("mods")
    shaders = collect("shaderpacks")
    client_only = sum(1 for e in mods if e["side"] == "client")

    md = f"""# Liste des mods — Minecraft Deadmoon

Pack **{pv}** · Minecraft **{mc}** · NeoForge **{neo}** · généré le {date.today().isoformat()}.

**{len(mods)} mods** et **{len(shaders)} shaderpacks**. {client_only} mods sont purement client :
le serveur en reçoit **{len(mods) - client_only}**.

Ce fichier est généré par `gen-modlist.py` à partir des métadonnées packwiz de `pack/`.
Ne pas l'éditer à la main : relancer `python3 gen-modlist.py` après chaque modification du pack.

Retour au [README](README.md).

## Mods

{table(mods)}

## Shaderpacks

Livrés désactivés, à activer dans *Options… → Video Settings → Shader Packs*.

{table(shaders, with_side=False)}
"""
    (ROOT / "MODS.md").write_text(md, encoding="utf-8")
    print(f"MODS.md écrit : {len(mods)} mods, {len(shaders)} shaderpacks, "
          f"{len(mods) - client_only} jars côté serveur")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as e:
        sys.exit(f"API Modrinth injoignable : {e}")
