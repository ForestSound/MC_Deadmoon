#!/bin/bash
# Construit le dossier mods/ à envoyer sur l'hébergement (OMGServ) + un zip prêt à uploader.
# Exclut les mods marqués side = "client" (EMI, Jade, Xaero's).
set -u
cd "$(dirname "$0")" || exit 1
OUT="build/server/mods"
rm -rf "$OUT" && mkdir -p "$OUT"
n=0; fail=0
for f in pack/mods/*.pw.toml; do
  side=$(grep -m1 '^side' "$f" | cut -d'"' -f2)
  [ "$side" = "client" ] && continue
  jar=$(grep -m1 '^filename' "$f" | cut -d'"' -f2)
  url=$(grep -m1 '^url' "$f" | cut -d'"' -f2)
  if [ -z "$url" ]; then
    # Mod CurseForge (métadonnées seules) : URL reconstruite depuis le file-id
    fid=$(grep -m1 'file-id' "$f" | tr -dc '0-9')
    url="https://mediafilez.forgecdn.net/files/${fid:0:4}/${fid:4}/$jar"
  fi
  if curl -fsSL -o "$OUT/$jar" "$url"; then n=$((n+1)); else echo "ÉCHEC: $jar"; fail=$((fail+1)); fi
done
echo "$n jars téléchargés, $fail échec(s)"
du -sh "$OUT"
rm -f build/server-mods.zip
if command -v zip >/dev/null; then
  ( cd build/server && zip -qr ../server-mods.zip mods )
else
  python3 -m zipfile -c build/server-mods.zip build/server/mods   # pas de zip(1) sur la machine
fi
echo "Zip prêt : $(pwd)/build/server-mods.zip ($(du -h build/server-mods.zip | cut -f1))"
[ $fail -eq 0 ]
