# Captures d'écran du guide

Dépose ici les 7 images, avec **exactement ces noms**. Le script `../guide.py` les intègre
automatiquement à la régénération ; tant qu'une image manque, un emplacement pointillé la
remplace dans le PDF, à la même taille.

| Fichier | Ce qu'il faut capturer |
|---|---|
| `01-choix-du-jeu.png` | L'application CurseForge au premier lancement, sur la liste des jeux |
| `02-creer-profil.png` | L'onglet Minecraft, avec le bouton « Créer un profil personnalisé » |
| `03-importer.png` | La fenêtre de création de profil, bouton « Importer » visible en haut à droite |
| `04-installation.png` | Le profil « Minecraft Deadmoon » pendant son installation |
| `05-memoire.png` | Les paramètres du profil, curseur « Mémoire allouée » sur 6 Go |
| `06-ajouter-serveur.png` | Le formulaire « Ajouter un serveur » de Minecraft, rempli avec l'adresse |
| `07-serveur-en-ligne.png` | La liste des serveurs, avec la barre verte à droite du nom |

Conseils :

- **PNG**, au moins 1200 px de large. Les proportions sont conservées, l'image est centrée
  dans son cadre : inutile de recadrer au millimètre.
- Capture **la fenêtre seule**, pas tout l'écran (sous Windows : `Alt + Impr. écran`).
- Vérifie qu'aucune information personnelle ne traîne (adresse e-mail, autres serveurs,
  nom de compte si tu préfères).
- Les images des étapes 1 à 5 se prennent sur Windows dans le launcher CurseForge ;
  celles des étapes 6 et 7 dans Minecraft une fois le pack lancé.

Régénération du PDF ensuite :

```bash
.venv/bin/python docs/guide.py
```
