# Minecraft Deadmoon

Modpack Minecraft **1.21.1** / **NeoForge 21.1.257**, géré avec [packwiz](https://packwiz.infra.link/).
Thème : automatisation Create, cuisine & agriculture, exploration de structures.

**Serveur** : `mcdeadmoon.omgserv.net:10023`
**URL du pack** (pour l'installeur packwiz) :
`https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/pack/pack.toml`

Ce dépôt sert à toute la guilde : chaque personne y trouve de quoi installer le pack et rejoindre
le serveur, et Gordorak y maintient la liste des mods.

## Guide à distribuer

`docs/Guide-Minecraft-Deadmoon.pdf` — 2 pages, prêt à envoyer à la guilde : installation **sous
Windows avec Prism Launcher** en 5 étapes, puis connexion au serveur et dépannage. Liens cliquables,
texte seul.
Régénération : `.venv/bin/python docs/guide.py` (nécessite reportlab).

### Instance Prism préconfigurée

`dist/Minecraft-Deadmoon-Prism.zip` (89 Ko) — à importer dans Prism par simple glisser-déposer.
Contient `mmc-pack.json` (1.21.1 + NeoForge 21.1.257), `instance.cfg` (mémoire 6 Go et commande
pre-lancement déjà réglées) et le bootstrap packwiz. **Les mods ne sont pas dedans** : ils se
téléchargent au premier lancement, ce qui préserve la mise à jour automatique.

Lien direct :
`https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/dist/Minecraft-Deadmoon-Prism.zip`

Après toute modification du pack, ce zip n'a pas besoin d'être régénéré — il ne contient que la
configuration, jamais la liste des mods.

Lien direct :
`https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/docs/Guide-Minecraft-Deadmoon.pdf`

## Installer le pack (côté joueur·euse)

Avec **Prism Launcher**, le pack s'installe **et se met à jour tout seul** à chaque lancement.
Une seule configuration à faire, puis plus personne n'a à y penser :

1. Installer [Prism Launcher](https://prismlauncher.org/) (gratuit, Windows/Mac/Linux).
2. *Ajouter une instance* → **Minecraft 1.21.1** → onglet *Mod Loader* → **NeoForge 21.1.257**.
3. Télécharger [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar)
   et le déposer dans le dossier de l'instance (clic droit sur l'instance → *Dossier* → sous-dossier `.minecraft`).
4. Clic droit sur l'instance → *Modifier* → *Paramètres* → cocher **Commandes personnalisées**, puis dans
   **Pre-launch command** coller :

   ```
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/pack/pack.toml
   ```

5. Lancer. Les 45 mods se téléchargent ; aux lancements suivants, seuls les changements sont récupérés.

**Ce que fait ce fichier `.jar`** : il se dépose une seule fois et ne change jamais. À chaque lancement,
il télécharge (et met à jour tout seul) `packwiz-installer.jar` à côté de lui, puis lit le `pack.toml`
servi par GitHub. GitHub n'héberge que la **liste** des mods — une centaine de Ko de fichiers `.toml`.
Les jars des mods, eux, viennent de Modrinth et CurseForge, et seuls ceux dont l'empreinte a changé
sont retéléchargés.

Mémoire conseillée : **6 Go minimum, 8 Go confortable**.

### Variante : launcher CurseForge (Windows)

Le launcher CurseForge **ne sait pas lire un pack packwiz** : il n'a pas de commande pre-launch, donc
pas de mise à jour automatique. Il faut alors diffuser un zip, à refaire à chaque modification du pack.

1. Côté maintenance, générer le zip : `cd pack && packwiz curseforge export`
   → `build/Minecraft-Deadmoon-1.0.0-curseforge.zip` (191 Mo)
2. Côté guilde, chaque personne l'installe : CurseForge App → *Minecraft* →
   *Créer un profil personnalisé* → **Importer** → choisir le zip

Sur les 45 mods, seuls 2 sont référencés par identifiant CurseForge ; les 43 autres sont **embarqués
comme jars** dans le zip (d'où les 191 Mo). C'est fonctionnel, mais chaque mise à jour représente un
transfert de 191 Mo et une réinstallation manuelle pour tout le monde.

Autre variante : le fichier `.mrpack` (2 Mo), importable dans Prism ou l'app Modrinth — mais pas dans
le launcher CurseForge.

## Rejoindre le serveur

Adresse à ajouter dans *Multijoueur* → *Ajouter un serveur* :

```
mcdeadmoon.omgserv.net:10023
```

Le `:10023` fait partie de l'adresse : sans lui, la connexion échoue. Tout le monde doit utiliser
**exactement la même version du pack** que le serveur, sinon Minecraft refuse la connexion avec un
message « Outdated client » ou « Outdated server ».

## Déployer le serveur (OMGServ)

1. Panel OMGServ → type de serveur **NeoForge**, version **1.21.1** (build **21.1.257**).
2. FTP : vider le dossier `mods/` existant, puis envoyer **`build/server-mods.zip`**
   (il se décompresse en `mods/` à la racine du serveur) — 41 jars, 216 Mo décompressés.
   Les 4 mods purement client (EMI, Jade, Xaero's Minimap & World Map) en sont exclus : inutiles côté serveur.
3. RAM conseillée : **6 Go minimum, 8 Go confortable** (Create + Terralith + 10 mods de structures).
4. Premier démarrage long (génération des registres). Si le panel propose `--add-modules` ou des flags
   Java, laisser les réglages par défaut d'OMGServ.

⚠️ Client et serveur doivent porter **exactement les mêmes versions** de mods : regénérer le zip
(`./build-server.sh`) à chaque mise à jour du pack, et prévenir la guilde.

## Maintenance du pack

`packwiz` est dans `~/.local/bin/packwiz` (compilé en conteneur, rien installé en système).

```bash
cd pack
packwiz modrinth add <slug>     # ajouter un mod Modrinth
packwiz curseforge add <slug>   # ajouter un mod CurseForge
packwiz remove <nom>            # retirer un mod
packwiz update --all            # mettre tout à jour
packwiz refresh                 # reconstruire l'index (après édition manuelle)
cd .. && ./build-server.sh      # regénérer le zip serveur
git add -A && git commit -m "..." && git push   # publier → la guilde l'a au prochain lancement
```

- `add-mods.sh` : réinstalle toute la liste de zéro (idempotent).
- Un mod **client only** : ajouter `side = "client"` dans son `pack/mods/<mod>.pw.toml`, puis `packwiz refresh`.
- Après chaque changement : régénérer le zip serveur, l'envoyer sur OMGServ, et prévenir les personnes
  qui jouent via le launcher CurseForge (elles ne reçoivent rien automatiquement).

## Contenu

### Create & addons
Create 6.0.10 · Create: Dragons Plus *(dépendance de Create)* · Create: Central Kitchen ·
Create Crafts & Additions · Steam 'n' Rails *(port NeoForge non officiel — seul dispo en 1.21.1)* ·
Create Confectionery

### Cuisine & agriculture
Farmer's Delight · Expanded Delight · Ube's Delight · Brewin' and Chewin' · Croptopia *(CurseForge)* ·
[Let's Do] Farm & Charm *(socle requis en 1.21.1)* · Vinery · Bakery · Brewery · Candlelight

### Structures & monde
Terralith **2.6.2** *(version NeoForge dédiée)* · les 10 **YUNG's Better** (Dungeons, Mineshafts, Strongholds, Desert Temples, Witch Huts, Ocean Monuments,
Nether Fortresses, End Island, Jungle Temples) + YUNG's API · When Dungeons Arise · Dungeons and Taverns

### Exploration & confort
Explorer's Compass · Nature's Compass · Waystones · Xaero's Minimap & World Map *(client)*

### Créatures
Mowzie's Mobs · L_Ender's Cataclysm

### Utilitaires
EMI *(client)* · Jade *(client)*

### Dépendances tirées automatiquement
Architectury API · Balm · Curios API · EpheroLib · Geckolib · Lionfish-API · Lithostitched *(Terralith 2.6.2)*
