#!/usr/bin/env python3
"""Génère le guide PDF d'installation de Minecraft Deadmoon.

Usage : ../../.venv/bin/python guide.py   (nécessite reportlab)
Sortie : Guide-Minecraft-Deadmoon.pdf
"""
import os, random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

W, H = A4
M = 20 * mm                      # marge latérale
COL = W - 2 * M                  # largeur de colonne

# ---------------------------------------------------------------- palette
NIGHT   = HexColor("#0A0C12")
NIGHT_2 = HexColor("#161B29")
MOON    = HexColor("#F2EFE7")
SILVER  = HexColor("#98A1B6")
COPPER  = HexColor("#D08A4A")
CRIMSON = HexColor("#9E3B33")
PAPER   = HexColor("#F7F5F0")
INK     = HexColor("#16181F")
MUTED   = HexColor("#5C6274")
RULE    = HexColor("#DED8CB")

# ---------------------------------------------------------------- fontes
F = "/usr/share/fonts/TTF"
for name, path in [
    ("Fira",      f"{F}/FiraSans-Regular.ttf"),
    ("Fira-Med",  f"{F}/FiraSans-Medium.ttf"),
    ("Fira-Semi", f"{F}/FiraSans-SemiBold.ttf"),
    ("Fira-Bold", f"{F}/FiraSans-Bold.ttf"),
    ("Fira-Black",f"{F}/FiraSans-Heavy.ttf"),
    ("Fira-Light",f"{F}/FiraSans-Light.ttf"),
    ("Fira-It",   f"{F}/FiraSans-Italic.ttf"),
    ("Fira-BoldIt", f"{F}/FiraSans-BoldItalic.ttf"),
    ("Mono",      f"{F}/DejaVuSansMono.ttf"),
    ("Mono-Bold", f"{F}/DejaVuSansMono-Bold.ttf"),
]:
    pdfmetrics.registerFont(TTFont(name, path))

# sans ces familles, les balises <b>/<i> des Paragraph resteraient en romain
for base in ("Fira", "Fira-Med", "Fira-Semi", "Fira-Light"):
    pdfmetrics.registerFontFamily(base, normal=base, bold="Fira-Bold",
                                  italic="Fira-It", boldItalic="Fira-BoldIt")
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                              italic="Mono", boldItalic="Mono-Bold")

def st(font="Fira", size=10, leading=None, color=INK, space=0, align=TA_LEFT):
    return ParagraphStyle("s", fontName=font, fontSize=size,
                          leading=leading or size * 1.45, textColor=color,
                          spaceAfter=space, alignment=align)

def para(c, text, style, x, y, w):
    """Dessine un paragraphe dont y est le haut. Renvoie le y du bas."""
    p = Paragraph(text, style)
    _, h = p.wrapOn(c, w, H)
    p.drawOn(c, x, y - h)
    return y - h

def tracked(c, text, x, y, font, size, color, tracking=1.0, center=False):
    """Texte avec interlettrage (reportlab n'a pas de letter-spacing)."""
    c.setFont(font, size); c.setFillColor(color)
    total = sum(pdfmetrics.stringWidth(ch, font, size) + tracking for ch in text) - tracking
    cx = x - total / 2 if center else x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + tracking
    return total

# ------------------------------------------------- gabarit des pages intérieures
def page_frame(c, kicker, title, num):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 24 * mm
    tracked(c, kicker, M, y, "Fira-Med", 8.2, COPPER, tracking=2.8)
    y -= 12 * mm
    c.setFont("Fira-Black", 27); c.setFillColor(INK)
    c.drawString(M - 1, y, title)
    y -= 6.5 * mm
    c.setStrokeColor(RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)
    # pied de page
    c.setFont("Fira", 7.6); c.setFillColor(MUTED)
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v2.0")
    c.drawRightString(W - M, 12 * mm, str(num))
    return y - 11 * mm

def step(c, n, title, body, x, y, w):
    """Étape numérotée dans une pastille. Renvoie le y du bas."""
    d = 7.2 * mm
    c.setFillColor(INK); c.circle(x + d / 2, y - d / 2 + 0.6 * mm, d / 2, stroke=0, fill=1)
    c.setFont("Fira-Bold", 10.5); c.setFillColor(PAPER)
    c.drawCentredString(x + d / 2, y - d / 2 - 2.6 * mm + 0.6 * mm, str(n))
    tx = x + d + 4.5 * mm
    yb = para(c, title, st("Fira-Semi", 11.6, 15), tx, y, w - (d + 4.5 * mm))
    if body:
        yb = para(c, body, st("Fira", 9.6, 14.2, MUTED), tx, yb - 2.2 * mm, w - (d + 4.5 * mm))
    return yb

def mono_box(c, text, x, y, w, size=9.4, pad=3.4 * mm):
    p = Paragraph(text, st("Mono", size, size * 1.5, INK))
    _, th = p.wrapOn(c, w - 2 * pad, H)
    bh = th + 2 * pad
    c.setFillColor(HexColor("#EDEAE1")); c.setStrokeColor(RULE); c.setLineWidth(0.8)
    c.roundRect(x, y - bh, w, bh, 1.8 * mm, stroke=1, fill=1)
    c.setStrokeColor(COPPER); c.setLineWidth(2.2)
    c.line(x + 0.9, y - bh + 2.2 * mm, x + 0.9, y - 2.2 * mm)
    p.drawOn(c, x + pad, y - bh + pad)
    return y - bh

def note_box(c, title, lines, x, y, w, accent=COPPER):
    inner = w - 13 * mm
    gap = 2.6 * mm
    style = ParagraphStyle("b", fontName="Fira", fontSize=9.5, leading=13.8,
                           textColor=INK, leftIndent=4 * mm, bulletIndent=0,
                           bulletFontName="Fira", bulletFontSize=9.5)
    paras = [Paragraph(l, style, bulletText="\u2022") for l in lines]
    heights = [p.wrapOn(c, inner, H)[1] for p in paras]
    th = sum(heights) + gap * (len(paras) - 1)
    bh = th + 13.5 * mm
    c.setFillColor(HexColor("#FFFFFF")); c.setStrokeColor(RULE); c.setLineWidth(0.8)
    c.roundRect(x, y - bh, w, bh, 2 * mm, stroke=1, fill=1)
    c.setFillColor(accent); c.rect(x, y - bh, 1.6 * mm, bh, stroke=0, fill=1)
    tracked(c, title, x + 7 * mm, y - 6.4 * mm, "Fira-Semi", 8.4, accent, tracking=1.6)
    cy = y - 10.8 * mm
    for pg, h in zip(paras, heights):
        pg.drawOn(c, x + 7 * mm, cy - h)
        cy -= h + gap
    return y - bh


# ---------------------------------------------------------------- captures d'écran
CAPTURES = "captures"   # dossier des images, à côté de ce script

def shot(c, filename, caption, x, y, w, h):
    """Place une capture d'écran. Si l'image manque, dessine un emplacement légendé
    de la même taille : le gabarit reste identique avant et après ajout des images."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), CAPTURES, filename)
    if os.path.exists(path):
        from reportlab.lib.utils import ImageReader
        img = ImageReader(path)
        iw, ih = img.getSize()
        scale = min(w / iw, h / ih)            # on garde les proportions, jamais d'étirement
        dw, dh = iw * scale, ih * scale
        dx = x + (w - dw) / 2
        c.drawImage(img, dx, y - h + (h - dh) / 2, dw, dh, mask="auto")
        c.setStrokeColor(RULE); c.setLineWidth(0.8)
        c.rect(dx, y - h + (h - dh) / 2, dw, dh, stroke=1, fill=0)
    else:
        c.setFillColor(HexColor("#EFECE4")); c.setStrokeColor(HexColor("#C9C2B2"))
        c.setLineWidth(0.9); c.setDash(3, 3)
        c.roundRect(x, y - h, w, h, 1.6 * mm, stroke=1, fill=1)
        c.setDash()
        tracked(c, "CAPTURE À AJOUTER", x + w / 2, y - h / 2 + 2.5 * mm,
                "Fira-Semi", 7.4, HexColor("#A79D88"), 1.6, center=True)
        p = Paragraph(f"<i>{caption}</i>", st("Fira", 8.2, 11.4, HexColor("#8D8577"), align=1))
        _, th = p.wrapOn(c, w - 16 * mm, H)
        p.drawOn(c, x + 8 * mm, y - h / 2 - th + 0.5 * mm)
    c.setFillColor(MUTED); c.setFont("Fira-It", 8.2)
    c.drawString(x, y - h - 4.6 * mm, caption if os.path.exists(path) else "")
    return y - h - (7 * mm if os.path.exists(path) else 3 * mm)

# ---------------------------------------------------------------- page 1
def first_header(c):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 24 * mm
    tracked(c, "GUIDE D’INSTALLATION", M, y, "Fira-Med", 8.2, COPPER, tracking=2.8)
    y -= 15 * mm
    c.setFont("Fira-Black", 32); c.setFillColor(INK)
    c.drawString(M - 1, y, "Minecraft Deadmoon")
    y -= 8 * mm
    para(c, "Comment installer le pack de mods et nous rejoindre sur le serveur",
         st("Fira-Light", 12.5, 17, MUTED), M, y, COL)
    y -= 13 * mm
    c.setStrokeColor(RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)
    c.setFont("Fira", 7.6); c.setFillColor(MUTED)
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v2.0")
    c.drawRightString(W - M, 12 * mm, "1")
    return y - 10 * mm

def page_1(c):
    y = first_header(c)
    y = para(c, "Minecraft Deadmoon ajoute <b>45 mods</b> à Minecraft : des machines, de la cuisine, "
                "de nouveaux monstres et un monde entièrement refait. Pour jouer avec nous, il faut "
                "installer ces mods chez toi. Tout se fait en une fois, en suivant les pages qui suivent. "
                "Compte une vingtaine de minutes, dont beaucoup d’attente.",
             st("Fira", 10.4, 15.6), M, y, COL)
    y -= 8 * mm
    y = note_box(c, "CE QU’IL TE FAUT", [
        "Un compte <b>Minecraft Java Edition</b>. Les versions Bedrock, Switch, PlayStation, Xbox "
        "et téléphone <b>ne peuvent pas</b> rejoindre le serveur : ce n’est pas le même jeu.",
        "Un ordinateur Windows, Mac ou Linux, avec environ <b>3 Go</b> de place libre.",
        "Le fichier <font name='Mono' size='8.6'>Minecraft-Deadmoon-1.0.0-curseforge.zip</font> "
        "que David t’a envoyé. <b>Ne l’ouvre pas et ne le décompresse pas</b> : laisse-le tel quel.",
    ], M, y, COL)

    y -= 9 * mm
    y = step(c, 1, "Installe l’application CurseForge",
             "Va sur <font name='Mono' size='9'>curseforge.com/download</font>, télécharge "
             "l’application, puis installe-la comme n’importe quel logiciel. À la première ouverture, "
             "elle demande quel jeu tu veux gérer : choisis <b>Minecraft</b>.", M, y, COL)
    y -= 3 * mm
    y = shot(c, "01-choix-du-jeu.png",
             "L’application CurseForge au premier lancement : la liste des jeux, où il faut cliquer sur Minecraft.",
             M, y, COL, 38 * mm)

    y -= 4 * mm
    y = step(c, 2, "Ouvre l’onglet Minecraft",
             "Dans la colonne de gauche de l’application, clique sur <b>Minecraft</b>. Tu arrives sur la "
             "page de tes profils de jeu : elle est vide pour l’instant.", M, y, COL)
    y -= 3 * mm
    shot(c, "02-creer-profil.png",
         "L’onglet Minecraft, avec le bouton « Créer un profil personnalisé ».", M, y, COL, 38 * mm)
    c.showPage()

# ---------------------------------------------------------------- page 2
def page_2(c):
    y = page_frame(c, "INSTALLATION", "Importer le pack", 2)
    y = step(c, 3, "Importe le fichier zip",
             "Clique sur <b>Créer un profil personnalisé</b>, puis, dans la fenêtre qui s’ouvre, sur "
             "<b>Importer</b> (en haut à droite). Choisis le fichier zip que David t’a envoyé, et valide. "
             "Rien d’autre à régler : tout est déjà dedans.", M, y, COL)
    y -= 3 * mm
    y = shot(c, "03-importer.png",
             "La fenêtre de création de profil : le bouton « Importer » se trouve en haut à droite.",
             M, y, COL, 50 * mm)

    y -= 6 * mm
    y = step(c, 4, "Laisse l’installation se faire",
             "L’application télécharge Minecraft, le moteur de mods NeoForge, puis les 45 mods. "
             "Cela prend <b>5 à 10 minutes</b> selon ta connexion. Tu peux faire autre chose pendant "
             "ce temps, mais ne ferme pas la fenêtre.", M, y, COL)
    y -= 3 * mm
    shot(c, "04-installation.png",
         "Le profil « Minecraft Deadmoon » en cours d’installation.", M, y, COL, 50 * mm)
    c.showPage()

# ---------------------------------------------------------------- page 3
def page_3(c):
    y = page_frame(c, "INSTALLATION", "Régler et lancer", 3)
    y = step(c, 5, "Donne-lui assez de mémoire",
             "C’est l’étape que tout le monde oublie, et sans elle le jeu plante. Passe la souris sur le "
             "profil, clique sur la <b>roue crantée</b>, puis <b>Paramètres → Mémoire allouée</b>, et règle "
             "sur <b>6 Go</b> au minimum (8 Go si ton ordinateur en a 16).", M, y, COL)
    y -= 3 * mm
    y = shot(c, "05-memoire.png",
             "Les paramètres du profil : le curseur « Mémoire allouée » réglé sur 6 Go.", M, y, COL, 52 * mm)

    y -= 6 * mm
    y = step(c, 6, "Lance le jeu",
             "Clique sur <b>Jouer</b>. Le premier démarrage prend 3 à 5 minutes : c’est normal, le jeu "
             "assemble tous les mods. Les fois suivantes seront bien plus rapides.", M, y, COL)

    y -= 9 * mm
    note_box(c, "ÇA Y EST, LE PACK EST INSTALLÉ", [
        "Tu peux déjà jouer en solo, mais le plus intéressant est sur le serveur : la page suivante "
        "explique comment nous y retrouver.",
        "Garde le fichier zip quelque part, il resservira si tu dois réinstaller.",
    ], M, y, COL)
    c.showPage()

# ---------------------------------------------------------------- page 4
def page_4(c):
    y = page_frame(c, "DERNIÈRE ÉTAPE", "Nous rejoindre sur le serveur", 4)

    bh = 26 * mm
    c.setFillColor(NIGHT); c.roundRect(M, y - bh, COL, bh, 2.4 * mm, stroke=0, fill=1)
    tracked(c, "ADRESSE DU SERVEUR", M + 8 * mm, y - 9 * mm, "Fira-Med", 7.6, COPPER, tracking=2.2)
    c.setFont("Mono-Bold", 15.5); c.setFillColor(MOON)
    c.drawString(M + 8 * mm, y - 19 * mm, "mcdeadmoon.omgserv.net:10023")
    y -= bh + 9 * mm

    y = step(c, 7, "Ouvre « Multijoueur », puis « Ajouter un serveur »",
             "Depuis l’écran d’accueil de Minecraft, une fois le jeu lancé.", M, y, COL)
    y -= 4 * mm
    y = step(c, 8, "Remplis les deux cases",
             "<b>Nom du serveur</b> : ce que tu veux, par exemple Deadmoon. "
             "<b>Adresse du serveur</b> : recopie l’adresse ci-dessus en entier. "
             "Le <font name='Mono' size='9'>:10023</font> à la fin fait partie de l’adresse, "
             "sans lui ça ne marchera pas.", M, y, COL)
    y -= 3 * mm
    y = shot(c, "06-ajouter-serveur.png",
             "Le formulaire « Ajouter un serveur », rempli avec l’adresse complète.", M, y, COL, 44 * mm)

    y -= 5 * mm
    y = step(c, 9, "Valide, puis double-clique sur le serveur",
             "Il apparaît dans ta liste. Une barre verte à droite du nom veut dire qu’il est allumé : "
             "double-clique dessus, et tu arrives au milieu des autres.", M, y, COL)
    y -= 3 * mm
    shot(c, "07-serveur-en-ligne.png",
         "Le serveur dans la liste, avec la barre verte qui indique qu’il est en ligne.", M, y, COL, 38 * mm)
    c.showPage()

# ---------------------------------------------------------------- page 5
def page_5(c):
    y = page_frame(c, "EN CAS DE PROBLÈME", "Si ça coince", 5)
    y = note_box(c, "LES CAS LES PLUS COURANTS", [
        "<b>« Outdated server » ou « Outdated client »</b> — tes mods ne sont pas les mêmes que ceux du "
        "serveur. Réimporte le zip envoyé par David, sans rien ajouter ni retirer.",
        "<b>Barre rouge, « Connection refused »</b> — le serveur est éteint ou en train de redémarrer. "
        "Réessaie dans deux minutes.",
        "<b>Le jeu plante pendant le chargement</b> — la mémoire est trop basse. Reprends l’étape 5 et "
        "monte à 8 Go.",
        "<b>Le jeu rame beaucoup</b> — baisse la distance d’affichage à 8 ou 10 chunks dans les options "
        "vidéo. Avec 45 mods, ça change tout.",
        "<b>Tu ne reconnais plus rien dans le monde</b> — c’est voulu : les paysages et les donjons sont "
        "entièrement refaits.",
        "<b>Rien ne marche</b> — envoie à David le fichier <font name='Mono' size='8.6'>latest.log</font>, "
        "qui se trouve dans le dossier <font name='Mono' size='8.6'>logs</font> du profil "
        "(clic droit sur le profil → Ouvrir le dossier).",
    ], M, y, COL, accent=CRIMSON)

    y -= 11 * mm
    tracked(c, "CE QU’IL Y A DANS LE PACK", M, y, "Fira-Semi", 8.2, COPPER, tracking=1.8)
    y -= 7 * mm
    for titre, desc in [
        ("Create et ses extensions",
         "Convoyeurs, trains, machines à vapeur, et de quoi automatiser la cuisine."),
        ("Cuisine et agriculture",
         "Des centaines de cultures et de recettes, du vin, de la bière, des dîners aux chandelles."),
        ("Un monde refait",
         "Nouveaux paysages, donjons, mines, temples et forteresses repensés de fond en comble."),
        ("Créatures",
         "Des boss sérieux. N’y va pas en armure de cuir."),
        ("Confort",
         "Téléportation entre balises, recherche de structures et de biomes, carte, livre de recettes."),
    ]:
        y = para(c, f"<b>{titre}</b> — {desc}", st("Fira", 9.8, 14), M, y, COL)
        y -= 3.4 * mm

    c.setFont("Fira", 8.4); c.setFillColor(MUTED)
    c.drawCentredString(W / 2, 20 * mm, "Des questions ? Demande à David.  ·  github.com/ForestSound/MC_Deadmoon")
    c.showPage()

# ---------------------------------------------------------------- assemblage
def build(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Minecraft Deadmoon — guide d’installation")
    c.setAuthor("David"); c.setSubject("Installer le modpack et rejoindre le serveur")
    page_1(c); page_2(c); page_3(c); page_4(c); page_5(c)
    c.save()
    manquantes = [f for f in sorted(os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), CAPTURES)))] \
        if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), CAPTURES)) else []
    print(f"{path} ({os.path.getsize(path)/1024:.0f} Ko) — captures présentes : {len(manquantes)}/7")

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Guide-Minecraft-Deadmoon.pdf"))
