#!/bin/bash
# Ajoute tous les mods du pack. Idempotent : relançable sans risque.
# Usage : ./add-mods.sh
set -u
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/pack" || exit 1
LOG="${TMPDIR:-/tmp}/packwiz-add.log"
: > "$LOG"

MODRINTH=(
  # --- Create & addons ---
  create                                  # Create 6.0.10
  create-central-kitchen                  # Create: Central Kitchen
  createaddition                          # Create Crafts & Additions
  create-steam-n-rails-1.21.1             # Steam 'n' Rails (port NeoForge)
  create-confectionery                    # Create Confectionery
  # --- Cuisine & agriculture ---
  farmers-delight                         # Farmer's Delight
  expanded-delight                        # Expanded Delight
  ubes-delight                            # Ube's Delight
  brewin-and-chewin                       # Brewin' and Chewin'
  lets-do-farm-charm                      # [Let's Do] Farm & Charm (socle 1.21.1)
  lets-do-vinery                          # [Let's Do] Vinery
  lets-do-bakery-farmcharm-compat         # [Let's Do] Bakery
  lets-do-brewery-farmcharm-compat        # [Let's Do] Brewery
  lets-do-candlelight-farmcharm-compat    # [Let's Do] Candlelight
  # --- Structures & monde ---
  yungs-api
  yungs-better-dungeons
  yungs-better-mineshafts
  yungs-better-strongholds
  yungs-better-desert-temples
  yungs-better-witch-huts
  yungs-better-ocean-monuments
  yungs-better-nether-fortresses
  yungs-better-end-island
  yungs-better-jungle-temples
  when-dungeons-arise
  dungeons-and-taverns
  terralith
  # --- Exploration & confort ---
  explorers-compass
  natures-compass
  waystones
  # --- Créatures ---
  mowzies-mobs
  l_enders-cataclysm
  # --- Utilitaires (choix Gordorak) ---
  jei
  jade
  xaeros-minimap
  xaeros-world-map
)

CURSEFORGE=(
  croptopia                               # absent de Modrinth
)

fail=()
for m in "${MODRINTH[@]}"; do
  [ -f "mods/$m.pw.toml" ] && { echo "= $m (déjà présent)"; continue; }
  echo "+ $m"
  packwiz modrinth add "$m" -y >>"$LOG" 2>&1 || fail+=("modrinth:$m")
done
for m in "${CURSEFORGE[@]}"; do
  echo "+ $m (curseforge)"
  packwiz curseforge add "$m" -y >>"$LOG" 2>&1 || fail+=("curseforge:$m")
done

packwiz refresh
echo
echo "Mods installés : $(ls mods/*.pw.toml 2>/dev/null | wc -l)"
echo "Journal détaillé : $LOG"
if [ ${#fail[@]} -gt 0 ]; then printf 'ÉCHECS : %s\n' "${fail[*]}"; exit 1; fi
