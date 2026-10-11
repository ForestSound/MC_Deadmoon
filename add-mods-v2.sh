#!/usr/bin/env bash
# Vague 2 : mods issus de modlist.html (Gordorak) + Iris/Sodium.
# Les shaderpacks s'ajoutent a part : packwiz modrinth add <slug>, puis side = "client".
# Idempotent : un mod deja present est saute.
set -uo pipefail
cd "$(dirname "$0")/pack" || exit 1
LOG="../build/add-mods-v2.log"
mkdir -p ../build
: > "$LOG"

MODRINTH=(
  diagonal-windows diagonal-fences diagonal-walls
  macaws-doors macaws-furniture macaws-fences-and-walls macaws-bridges
  macaws-stairs macaws-paintings macaws-lights-and-lamps
  extradelight teyvats-delight kazakh-delight ribbe_delight
  roll-delight veggies-delight aquaculture-delight ramadan-delight fungi-delight
  "new-years-delight-(a-farmers-delight-add-on)"
  aures-farmers-structures realm-rpg-treasure-balloons explorify
  trashslot amendments simple-hats corpse comforts
  nemos-inventory-sorting chipped
  sophisticated-core sophisticated-backpacks
  aquaculture ars-nouveau
  resourceful-lib puzzles-lib moonlight athena-ctm owo-lib accessories
  sodium iris treetimber-treecapitator
)
# rice-delight : distribution tierce coupee par l'auteur, packwiz ne peut pas le servir.
# christmas-delight : aucun build 1.21.1 NeoForge (le jar CurseForge est en 1.20.1).
# treetimber : repris depuis Modrinth, URL stable.
CURSEFORGE=( gobber )

ok=0; skip=0; fail=0
for m in "${MODRINTH[@]}"; do
  if compgen -G "mods/*.pw.toml" > /dev/null && grep -qrl "/$m/" mods/ 2>/dev/null; then :; fi
  if [[ -f "mods/$m.pw.toml" ]]; then
    echo "SKIP  $m (deja present)" | tee -a "$LOG"; skip=$((skip+1)); continue
  fi
  echo "ADD   modrinth: $m" | tee -a "$LOG"
  if packwiz modrinth add "$m" -y >> "$LOG" 2>&1; then ok=$((ok+1));
  else echo "ECHEC modrinth: $m" | tee -a "$LOG"; fail=$((fail+1)); fi
done

for m in "${CURSEFORGE[@]}"; do
  if [[ -f "mods/$m.pw.toml" ]]; then
    echo "SKIP  $m (deja present)" | tee -a "$LOG"; skip=$((skip+1)); continue
  fi
  echo "ADD   curseforge: $m" | tee -a "$LOG"
  if packwiz curseforge add "https://www.curseforge.com/minecraft/mc-mods/$m" -y >> "$LOG" 2>&1; then ok=$((ok+1));
  else echo "ECHEC curseforge: $m" | tee -a "$LOG"; fail=$((fail+1)); fi
done

echo "--- ajoutes=$ok  sautes=$skip  echecs=$fail  ---" | tee -a "$LOG"
