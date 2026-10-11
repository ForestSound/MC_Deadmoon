# Minecraft Deadmoon

Modpack Minecraft **1.21.1** / **NeoForge 21.1.257**, géré avec [packwiz](https://packwiz.infra.link/).
Thème : automatisation Create, cuisine & agriculture, décoration, exploration de structures.
**89 mods + 3 shaderpacks.** Version du pack : **1.1.0**.
Liste exhaustive avec les numéros de version : **[MODS.md](MODS.md)**.

**Serveur** : `mcdeadmoon.omgserv.net:10023`
**URL du pack** (lue par l'installeur packwiz) :
`https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/pack/pack.toml`

Ce dépôt sert à toute la guilde : chaque personne y trouve de quoi installer le pack et rejoindre
le serveur, et Gordorak y maintient la liste des mods.

## À distribuer à la guilde

Deux fichiers, et c'est tout :

| Fichier | Taille | Lien direct |
|---|---|---|
| Le guide | 2 pages | `https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/docs/Guide-Minecraft-Deadmoon.pdf` |
| L'instance Prism | 89 Ko | `https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/dist/Minecraft-Deadmoon-Prism.zip` |

Le guide (`docs/Guide-Minecraft-Deadmoon.pdf`) couvre l'installation sous **Windows avec Prism
Launcher** en 5 étapes, la connexion au serveur et le dépannage. Liens cliquables, texte seul.
Régénération : `.venv/bin/python docs/guide.py` (nécessite reportlab).

## Installer le pack — chemin recommandé

`dist/Minecraft-Deadmoon-Prism.zip` s'importe dans Prism par simple glisser-déposer. Il contient
`mmc-pack.json` (1.21.1 + NeoForge 21.1.257), `instance.cfg` (mémoire 6 Go et commande pre-lancement
déjà réglées), le bootstrap packwiz et `config/iris.properties`. **Les mods n'y sont pas** : ils se
téléchargent au premier lancement, ce qui garde la mise à jour automatique et ramène le fichier à
89 Ko au lieu de 300 Mo.

Côté joueur·euse : installer [Prism Launcher](https://prismlauncher.org/download/windows/) →
ajouter son compte Microsoft → glisser le zip sur la fenêtre → double-cliquer sur l'instance.
Aucune étape technique. *Import validé sous Windows (octobre 2026).*

Ce zip n'a besoin d'être régénéré que si la **configuration** change (mémoire, version de NeoForge,
shader présélectionné). Ajouter ou retirer un mod ne le concerne pas.

### Variante : configuration manuelle dans Prism

Si l'import échoue, la même chose à la main :

1. Installer [Prism Launcher](https://prismlauncher.org/) (gratuit, Windows/Mac/Linux).
2. *Ajouter une instance* → **Minecraft 1.21.1** → **NeoForge 21.1.257**.
3. Télécharger [packwiz-installer-bootstrap.jar](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest/download/packwiz-installer-bootstrap.jar)
   et le déposer dans le sous-dossier `.minecraft` de l'instance (clic droit sur l'instance → *Dossier*).
4. Clic droit → *Modifier* → *Paramètres* → cocher **Commandes personnalisées**, puis dans
   **Pre-launch command** coller :

   ```
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/pack/pack.toml
   ```

5. *Paramètres → Java* : mémoire maximale à **6144 Mo** (8192 si la machine a 16 Go).

**Ce que fait ce `.jar`** : il se dépose une fois et ne change jamais. À chaque lancement, il
télécharge (et met à jour tout seul) `packwiz-installer.jar` à côté de lui, puis lit le `pack.toml`
servi par GitHub. GitHub n'héberge que la **liste** des mods — quelques centaines de Ko de `.toml`.
Les jars viennent de Modrinth et CurseForge, et seuls ceux dont l'empreinte a changé sont
retéléchargés.

### Variante : launcher CurseForge

Le launcher CurseForge **ne sait pas lire un pack packwiz** : pas de commande pre-launch, donc pas de
mise à jour automatique. Il faut diffuser un zip, à refaire à chaque modification du pack.

1. Générer le zip : `cd pack && packwiz curseforge export`
2. CurseForge App → *Minecraft* → *Créer un profil personnalisé* → **Importer** → choisir le zip

Chaque mise à jour = un transfert de ~300 Mo et une réinstallation manuelle pour tout le monde.

Le `.mrpack` (`build/Minecraft-Deadmoon-1.1.0.mrpack`, 2,5 Mo) est un troisième recours, importable
dans Prism ou l'app Modrinth — mais pas dans le launcher CurseForge, et sans mise à jour automatique.

## Shaders

Le pack embarque **Iris** (le moteur de shaders) et **Sodium** (dont Iris dépend), plus trois
shaderpacks qui arrivent automatiquement dans `shaderpacks/` chez tout le monde, exactement comme les
mods :

| Shaderpack | Version | Pour qui |
|---|---|---|
| Complementary Reimagined | r5.9.3 | présélectionné — rendu proche du vanilla, le mieux optimisé |
| Complementary Unbound | r5.9.3 | plus poussé visuellement, plus gourmand |
| BSL | v10.1.8 | style très marqué, le plus gourmand des trois |

**Les shaders sont livrés désactivés.** Ils coûtent cher en images par seconde et toute la guilde
n'a pas la même machine : chacun·e les allume quand il ou elle veut, via *Options… → Video Settings →
Shader Packs* → cocher **Shader Pack Enabled**.

Complementary Reimagined est déjà sélectionné pour les nouvelles installations (c'est le rôle de
`config/iris.properties` dans le zip Prism). Les personnes déjà installées avant la 1.1.0 n'auront pas
cette présélection : la liste des trois shaderpacks sera bien là, il n'y aura juste rien de coché.

Les trois `.pw.toml` de `pack/shaderpacks/` portent `side = "client"` : le serveur ne les reçoit pas.

## Rejoindre le serveur

Dans le jeu : *Multijoueur* → *Ajouter un serveur* → adresse `mcdeadmoon.omgserv.net:10023`.
Le `:10023` fait partie de l'adresse, sans lui la connexion échoue.

Tout le monde doit avoir **exactement la même version du pack** que le serveur, sinon Minecraft
refuse avec « Outdated client » ou « Outdated server ».

## Déployer le serveur (OMGServ)

Le serveur tourne en **NeoForge 21.1.257 / Minecraft 1.21.1** — même build que le client, c'est
impératif. Vérifiable dans la console au démarrage : `--fml.neoForgeVersion, 21.1.257`.

Le FTP se crée depuis le panel, section **« Serveur FTP »** (identifiant + mot de passe à définir,
l'hôte s'affiche ensuite), puis connexion avec FileZilla.

Le `mods/` va à la **racine du serveur** : le dossier qui contient `server.properties`. NeoForge l'y
crée vide à son premier démarrage.

```
racine du serveur
├── libraries/
├── logs/
├── mods/              ← les 81 jars ici, en vrac
├── world/
├── eula.txt
└── server.properties  ← ce fichier identifie la racine
```

Dans l'ordre :

1. **Arrêter le serveur.** Un serveur allumé réécrit ses fichiers en s'arrêtant et écraserait l'upload.
2. **Supprimer `world/`** (ainsi que `world_nether/` et `world_the_end/` s'ils existent). Terralith
   remplace la génération du terrain : sur un monde déjà généré en vanilla, on obtient une zone de
   spawn vanilla, des biomes Terralith autour, et des murs de terrain à la frontière.
3. **Vider `mods/`**, puis envoyer les **81 jars** de `build/server-mods.zip` (287 Mo décompressés).
   Les jars vont **directement** dans `mods/`, sans sous-dossier : extraire le zip depuis la racine,
   pas depuis l'intérieur de `mods/`, sinon on obtient `mods/mods/` et le serveur démarre sans aucun
   mod — sans erreur visible, jusqu'à ce que tout le monde soit rejeté en « Outdated client ».
4. **Mémoire : 6 Go minimum** (8 Go confortable à 89 mods). Dans `server.properties` :
   `view-distance=8` et `simulation-distance=6`. Au-delà, le serveur s'écroule dès que trois
   personnes s'éloignent.
5. **Démarrer et surveiller la console** jusqu'à `Done (XXXs)! For help, type "help"`. Compter 3 à
   10 minutes au lieu de quelques secondes : cette lenteur est le signe que les mods se chargent.
   En cas de plantage, la console nomme le mod fautif.
6. **Tester soi-même** avant d'annoncer l'adresse à la guilde.

**81 jars côté serveur contre 89 côté client, c'est normal** : EMI, Jade, Iris, Sodium, Athena,
Nemo's Inventory Sorting et les deux Xaero's sont purement client, `build-server.sh` les exclut (ils
portent `side = "client"` dans leur `.pw.toml`). Les shaderpacks sont exclus pour la même raison.

## Mettre à jour le serveur après une modification du pack

Le client se met à jour tout seul, le serveur **non**. Et c'est le serveur qui doit partir devant :
une personne sous Prism aura les nouveaux mods au lancement suivant, et se fera rejeter si le serveur
est resté en arrière.

```bash
export PATH="$HOME/.local/bin:$PATH"
cd ~/dev/minecraft-modpack

# 1. modifier le pack (ajout, retrait, mise à jour), puis :
cd pack && packwiz refresh && cd ..

# 2. reconstruire le dossier mods/ du serveur
./build-server.sh          # → build/server/mods/ + build/server-mods.zip

# 3. publier la nouvelle liste pour la guilde
git add -A && git commit -m "..." && git push
```

Ensuite, sur le panel OMGServ :

1. **Prévenir la guilde** et demander à tout le monde de quitter le serveur.
2. **Arrêter le serveur** depuis le panel, et attendre que le statut passe réellement à l'arrêt.
3. **Sauvegarder `world/`** (téléchargement FTP, ou snapshot si le panel en propose). À faire même
   quand la mise à jour paraît anodine : un mod retiré emporte ses blocs du monde.
4. **Vider `mods/` entièrement**, puis y envoyer les jars de `build/server-mods.zip`. Ne pas se
   contenter d'ajouter les nouveaux : les anciennes versions resteraient à côté des nouvelles et
   NeoForge refuserait de démarrer sur un doublon de modid.
5. **Redémarrer** et attendre `Done (XXXs)!` dans la console.
6. **Se connecter soi-même** pour vérifier, puis annoncer que c'est ouvert.

Si quelqu'un se fait rejeter en « Outdated server » après ça, c'est que le serveur n'a pas la même
liste : vérifier que `mods/` contient bien le même nombre de jars que `build/server/mods/`.

Pour un **retrait** de mod, prévoir l'étape de plus : supprimer un mod qui a posé des blocs laisse
des erreurs de chargement de chunks. `world/` sauvegardé à l'étape 3, c'est le filet.

## Maintenance du pack

`packwiz` est dans `~/.local/bin/packwiz` (compilé en conteneur, rien installé en système).

```bash
export PATH="$HOME/.local/bin:$PATH"
cd pack
packwiz modrinth add <slug>     # ajouter un mod Modrinth
packwiz curseforge add <slug>   # ajouter un mod CurseForge
packwiz remove <nom>            # retirer un mod
packwiz update --all            # mettre tout à jour
packwiz refresh                 # reconstruire l'index (après édition manuelle)
cd .. && ./build-server.sh      # regénérer le zip serveur
python3 gen-modlist.py          # regénérer MODS.md
```

- **Après toute modification du pack** : `packwiz refresh`, `./build-server.sh`,
  `python3 gen-modlist.py`, puis commit. MODS.md est généré, ne jamais l'éditer à la main.
- `add-mods.sh` : réinstalle la liste d'origine de zéro (idempotent).
  `add-mods-v2.sh` : la deuxième vague (décoration, Farmer's Delight addons, Iris/Sodium).
- Un mod **client only** : ajouter `side = "client"` dans son `pack/mods/<mod>.pw.toml`, puis
  `packwiz refresh`.
- `packwiz update` peut se tromper quand un projet versionne mal ses sorties (vu sur Terralith, qui
  restait en 2.5.8 alors que la 2.6.2 existait, et sur TreeTimber). En cas de doute :
  `packwiz modrinth add --project-id <id> --version-id <id>`.
- **Vérifier chaque ajout CurseForge** : `packwiz curseforge add` ne garantit pas le bon couple
  loader/version. Christmas Delight est ainsi arrivé en jar 1.20.1 et a dû être retiré.
- **Un mod CurseForge dont l'auteur a coupé la distribution tierce est inutilisable ici** : packwiz
  ne peut pas le télécharger pour la guilde. Le symptôme apparaît à l'export
  (`Found N manual downloads`). Rice Delight est dans ce cas, d'où son absence.

## Contenu

Vue d'ensemble par thème. Pour la liste complète, avec le numéro de version de chaque mod, son côté
(client seul ou client + serveur) et un lien vers sa page : **[MODS.md](MODS.md)**.

### Create & addons
Create 6.0.10 · Create: Dragons Plus *(dépendance de Create)* · Create: Central Kitchen ·
Create Crafts & Additions · Steam 'n' Rails *(port NeoForge non officiel — seul dispo en 1.21.1)* ·
Create Confectionery

### Cuisine & agriculture
Farmer's Delight · Expanded Delight · ExtraDelight · Ube's Delight · Brewin' and Chewin' ·
Croptopia *(CurseForge)* · Aquaculture 2 + Aquaculture Delight ·
[Let's Do] Farm & Charm *(socle requis en 1.21.1)* · Vinery · Bakery · Brewery · Candlelight

### Farmer's Delight — addons de cuisine du monde
Kazakh Delight · Ribbe Delight · Roll Delight · Veggies Delight ·
Ramadan Delight · Fungi Delight · New Year's Delight

### Décoration & construction
Les 7 **Macaw's** (Doors, Furniture, Fences and Walls, Bridges, Stairs, Paintings, Lights and Lamps) ·
Chipped · Amendments · Diagonal Fences · Diagonal Walls · Diagonal Windows · Simple Hats

### Structures & monde
Terralith **2.6.2** *(version NeoForge dédiée)* · les 10 **YUNG's Better**
(Dungeons, Mineshafts, Strongholds, Desert Temples, Witch Huts, Ocean Monuments, Nether Fortresses,
End Island, Jungle Temples) + YUNG's API · When Dungeons Arise · Dungeons and Taverns · Explorify ·
Aures - Farmers Structures · Realm RPG: Treasure Balloons

### Magie & progression
Ars Nouveau · Relics

### Exploration & confort
Explorer's Compass · Nature's Compass · Waystones · Sophisticated Backpacks · Comforts · Corpse ·
TrashSlot · TreeTimber · Xaero's Minimap & World Map *(client)* ·
Nemo's Inventory Sorting *(client)*

### Créatures
Mowzie's Mobs · L_Ender's Cataclysm

### Rendu & utilitaires
Iris Shaders *(client)* · Sodium *(client)* · EMI *(client)* · Jade *(client)*

### Écartés volontairement
**JEI** — EMI remplit le même rôle, et les deux ensemble donnent deux interfaces de recettes
superposées. **Gobber** et **Teyvat's Delight** — retirés à la demande de Gordorak.
**Biomes O' Plenty** — Terralith est seul maître de la génération du monde ; faire
cohabiter deux générateurs de biomes donne des frontières nettes et des structures mal placées.
Retirer BoP a aussi retiré ses deux dépendances, TerraBlender et GlitchCore, dont rien d'autre
n'avait besoin dans ce pack.

### Dépendances tirées automatiquement
Architectury API · Balm · Curios API · Accessories · Athena *(client)* · EpheroLib · Geckolib ·
Lionfish-API · Lithostitched *(Terralith 2.6.2)* · Moonlight Lib · owo-lib · Puzzles Lib ·
Resourceful Lib · ShatterLib/OctoLib *(Relics)* · Sophisticated Core
