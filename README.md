# Minecraft Deadmoon

Modpack Minecraft **1.21.1** / **NeoForge 21.1.257**, géré avec [packwiz](https://packwiz.infra.link/).
Thème : automatisation Create, cuisine & agriculture, exploration de structures. **45 mods.**

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
déjà réglées) et le bootstrap packwiz. **Les mods n'y sont pas** : ils se téléchargent au premier
lancement, ce qui garde la mise à jour automatique et ramène le fichier à 89 Ko au lieu de 215 Mo.

Côté joueur·euse : installer [Prism Launcher](https://prismlauncher.org/download/windows/) →
ajouter son compte Microsoft → glisser le zip sur la fenêtre → double-cliquer sur l'instance.
Aucune étape technique.

Ce zip n'a pas besoin d'être régénéré quand le pack change : il ne contient que la configuration,
jamais la liste des mods.

> ⚠️ L'import de ce zip n'a pas encore été testé sur une vraie installation Windows. Le format a été
> vérifié contre les métadonnées de Prism (`net.neoforged 21.1.257` exige bien `net.minecraft 1.21.1`),
> mais fais-le essayer par une personne avant diffusion générale.

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
servi par GitHub. GitHub n'héberge que la **liste** des mods — une centaine de Ko de `.toml`. Les
jars viennent de Modrinth et CurseForge, et seuls ceux dont l'empreinte a changé sont retéléchargés.

### Variante : launcher CurseForge

Le launcher CurseForge **ne sait pas lire un pack packwiz** : pas de commande pre-launch, donc pas de
mise à jour automatique. Il faut diffuser un zip, à refaire à chaque modification du pack.

1. Générer le zip : `cd pack && packwiz curseforge export`
   → `build/Minecraft-Deadmoon-1.0.0-curseforge.zip` (191 Mo)
2. CurseForge App → *Minecraft* → *Créer un profil personnalisé* → **Importer** → choisir le zip

Sur les 45 mods, seuls 2 sont référencés par identifiant CurseForge ; les 43 autres sont embarqués
comme jars dans le zip, d'où les 191 Mo. Chaque mise à jour = un transfert de 191 Mo et une
réinstallation manuelle pour tout le monde.

Le `.mrpack` (2 Mo) est un troisième recours, importable dans Prism ou l'app Modrinth — mais pas dans
le launcher CurseForge, et sans mise à jour automatique.

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
├── mods/              ← les 41 jars ici, en vrac
├── world/
├── eula.txt
└── server.properties  ← ce fichier identifie la racine
```

Dans l'ordre :

1. **Arrêter le serveur.** Un serveur allumé réécrit ses fichiers en s'arrêtant et écraserait l'upload.
2. **Supprimer `world/`** (ainsi que `world_nether/` et `world_the_end/` s'ils existent). Terralith
   remplace la génération du terrain : sur un monde déjà généré en vanilla, on obtient une zone de
   spawn vanilla, des biomes Terralith autour, et des murs de terrain à la frontière.
3. **Vider `mods/`**, puis envoyer les **41 jars** de `build/server-mods.zip` (216 Mo décompressés).
   Les jars vont **directement** dans `mods/`, sans sous-dossier : extraire le zip depuis la racine,
   pas depuis l'intérieur de `mods/`, sinon on obtient `mods/mods/` et le serveur démarre sans aucun
   mod — sans erreur visible, jusqu'à ce que tout le monde soit rejeté en « Outdated client ».
4. **Mémoire : 6 Go minimum** (8 Go confortable). Dans `server.properties` : `view-distance=8` et
   `simulation-distance=6`. Au-delà, le serveur s'écroule dès que trois personnes s'éloignent.
5. **Démarrer et surveiller la console** jusqu'à `Done (XXXs)! For help, type "help"`. Compter 3 à
   10 minutes au lieu de quelques secondes : cette lenteur est le signe que les mods se chargent.
   En cas de plantage, la console nomme le mod fautif.
6. **Tester soi-même** avant d'annoncer l'adresse à la guilde.

**41 jars côté serveur contre 45 côté client, c'est normal** : EMI, Jade et les deux Xaero's sont
purement client, `build-server.sh` les exclut (ils portent `side = "client"` dans leur `.pw.toml`).

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
git add -A && git commit -m "..." && git push   # publier → la guilde l'a au prochain lancement
```

- `add-mods.sh` : réinstalle toute la liste de zéro (idempotent).
- Un mod **client only** : ajouter `side = "client"` dans son `pack/mods/<mod>.pw.toml`, puis `packwiz refresh`.
- `packwiz update` peut se tromper quand un projet versionne mal ses sorties (vu sur Terralith, qui
  restait en 2.5.8 alors que la 2.6.2 existait). En cas de doute :
  `packwiz modrinth add --project-id <id> --version-id <id>`.

**Ordre d'une mise à jour**, à respecter : `./build-server.sh` → arrêter le serveur → sauvegarder le
monde → vider `mods/` → envoyer les nouveaux jars → redémarrer → prévenir la guilde. Les joueur·euses
sous Prism se mettent à jour seuls au lancement suivant, mais si le serveur n'est pas à jour **avant**
eux, ils se retrouvent bloqués dehors.

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
