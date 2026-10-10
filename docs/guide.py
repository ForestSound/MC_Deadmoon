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
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v3.0")
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


# ---------------------------------------------------------------- contenu
URL_PACK = "https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/pack/pack.toml"

def first_header(c):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 24 * mm
    tracked(c, "GUIDE D’INSTALLATION · WINDOWS", M, y, "Fira-Med", 8.2, COPPER, tracking=2.8)
    y -= 15 * mm
    c.setFont("Fira-Black", 32); c.setFillColor(INK)
    c.drawString(M - 1, y, "Minecraft Deadmoon")
    y -= 8 * mm
    para(c, "Installer le pack avec Prism Launcher, et nous rejoindre sur le serveur",
         st("Fira-Light", 12.5, 17, MUTED), M, y, COL)
    y -= 13 * mm
    c.setStrokeColor(RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)
    c.setFont("Fira", 7.6); c.setFillColor(MUTED)
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v3.0")
    c.drawRightString(W - M, 12 * mm, "1")
    return y - 10 * mm

def page_1(c):
    y = first_header(c)
    y = para(c, "On installe les <b>45 mods</b> du pack avec <b>Prism Launcher</b>, un lanceur gratuit "
                "qui remplace celui de Minecraft. Pas besoin de l’avoir déjà : on part de zéro. "
                "Une fois réglé, <b>le pack se met à jour tout seul</b> à chaque lancement — tu n’auras "
                "plus jamais à y toucher. Compte 30 minutes.",
             st("Fira", 10.4, 15.6), M, y, COL)
    y -= 8 * mm
    y = note_box(c, "CE QU’IL TE FAUT", [
        "Un compte <b>Minecraft Java Edition</b> — les versions Bedrock, Switch, PlayStation, Xbox et "
        "téléphone ne peuvent pas rejoindre le serveur.",
        "Un PC sous <b>Windows 10 ou 11</b>, environ <b>3 Go</b> de place libre.",
        "Tes identifiants <b>Microsoft</b>. Java, lui, s’installe tout seul avec Prism.",
    ], M, y, COL)

    y -= 9 * mm
    y = step(c, 1, "Installe Prism Launcher",
             "Sur <font name='Mono' size='9'>prismlauncher.org/download</font>, section <b>Windows</b>, "
             "prends le fichier <b>Installer (.exe)</b> et lance-le : installation classique, tout "
             "suivant. Si Windows affiche « Windows a protégé votre ordinateur », clique sur "
             "<b>Informations complémentaires</b> puis <b>Exécuter quand même</b>.", M, y, COL)
    y -= 6 * mm
    y = step(c, 2, "Premier démarrage",
             "Prism demande la langue, puis propose de <b>télécharger Java</b> : accepte. "
             "Ensuite, en haut à droite : <b>Comptes → Gérer les comptes → Ajouter un compte "
             "Microsoft</b>, et connecte-toi. Ton pseudo s’affiche en haut à droite.", M, y, COL)
    y -= 6 * mm
    y = step(c, 3, "Crée l’instance",
             "<b>Ajouter une instance</b> (en haut à gauche). Nom : <b>Deadmoon</b>. Version : "
             "<b>1.21.1</b> — attention à ne pas prendre 1.21 ni 1.21.4. Puis, dans la colonne de "
             "gauche, <b>NeoForge</b> en version <b>21.1.257</b>. Valide avec <b>OK</b>.", M, y, COL)
    c.showPage()

def page_2(c):
    y = page_frame(c, "LA PARTIE TECHNIQUE", "Brancher les mises à jour", 2)
    y = para(c, "Ces trois étapes disent à Prism d’aller chercher les mods à jour avant chaque "
                "lancement. Elles ne se font qu’une fois.", st("Fira", 10.2, 15), M, y, COL)
    y -= 8 * mm

    y = step(c, 4, "Dépose le fichier de mise à jour",
             "Télécharge <font name='Mono' size='8.8'>packwiz-installer-bootstrap.jar</font> "
             "(Gordorak t’envoie le lien). Dans Prism : <b>clic droit sur l’instance → Dossier</b>, "
             "entre dans le sous-dossier <font name='Mono' size='8.8'>.minecraft</font>, et colle le "
             "fichier dedans.", M, y, COL)
    y -= 6 * mm
    y = step(c, 5, "Colle la commande",
             "Clic droit sur l’instance → <b>Modifier → Paramètres</b> → coche <b>Commandes "
             "personnalisées</b>. Dans <b>Pre-launch command</b>, colle la ligne ci-dessous. "
             "<b>Copie-la depuis le message de Gordorak</b> : une faute de frappe et rien ne marche.",
             M, y, COL)
    y -= 3.5 * mm
    y = mono_box(c, '"$INST_JAVA" -jar packwiz-installer-bootstrap.jar<br/>' + URL_PACK, M, y, COL, size=8.4)

    y -= 7 * mm
    y = step(c, 6, "Règle la mémoire",
             "Toujours dans <b>Paramètres</b>, onglet <b>Java</b> : coche <b>Allocation mémoire</b> et "
             "mets la mémoire maximale à <b>6144 Mo</b> (8192 si ton PC a 16 Go). Sans ça, le jeu "
             "plante au chargement — c’est l’oubli le plus fréquent.", M, y, COL)
    y -= 6 * mm
    y = step(c, 7, "Lance le jeu",
             "Double-clique sur l’instance. Les 45 mods se téléchargent, puis Minecraft démarre. "
             "Le premier lancement prend 3 à 5 minutes, les suivants sont rapides.", M, y, COL)

    y -= 9 * mm
    note_box(c, "LES PROCHAINES FOIS", [
        "Double-clic sur l’instance, et c’est tout : les mods ajoutés ou mis à jour par Gordorak "
        "se téléchargent automatiquement avant le lancement.",
    ], M, y, COL)
    c.showPage()

def page_3(c):
    y = page_frame(c, "DERNIÈRE ÉTAPE", "Nous rejoindre", 3)

    bh = 26 * mm
    c.setFillColor(NIGHT); c.roundRect(M, y - bh, COL, bh, 2.4 * mm, stroke=0, fill=1)
    tracked(c, "ADRESSE DU SERVEUR", M + 8 * mm, y - 9 * mm, "Fira-Med", 7.6, COPPER, tracking=2.2)
    c.setFont("Mono-Bold", 15.5); c.setFillColor(MOON)
    c.drawString(M + 8 * mm, y - 19 * mm, "mcdeadmoon.omgserv.net:10023")
    y -= bh + 9 * mm

    y = step(c, 8, "Multijoueur → Ajouter un serveur",
             "Depuis l’écran d’accueil de Minecraft, une fois le jeu lancé.", M, y, COL)
    y -= 5 * mm
    y = step(c, 9, "Remplis les deux cases",
             "<b>Nom</b> : ce que tu veux. <b>Adresse</b> : recopie celle ci-dessus en entier — le "
             "<font name='Mono' size='9'>:10023</font> en fait partie, sans lui ça ne marche pas. "
             "Valide, puis double-clique sur le serveur : une barre verte signifie qu’il est allumé.",
             M, y, COL)

    y -= 10 * mm
    y = note_box(c, "SI ÇA COINCE", [
        "<b>Les mods ne se téléchargent pas</b> — vérifie que le fichier <font name='Mono' "
        "size='8.6'>.jar</font> est bien dans <font name='Mono' size='8.6'>.minecraft</font> et que la "
        "commande a été collée en entier, guillemets compris.",
        "<b>« Outdated server » ou « Outdated client »</b> — relance le jeu, la mise à jour se fait au "
        "démarrage.",
        "<b>« Connection refused »</b> — le serveur redémarre, réessaie dans deux minutes.",
        "<b>Plantage au chargement</b> — monte la mémoire à 8192 Mo (étape 6).",
        "<b>Ça rame</b> — baisse la distance d’affichage à 8 ou 10 chunks dans les options vidéo.",
        "<b>Rien ne marche</b> — envoie à Gordorak le fichier <font name='Mono' size='8.6'>"
        ".minecraft/logs/latest.log</font> (clic droit sur l’instance → Dossier).",
    ], M, y, COL, accent=CRIMSON)

    y -= 10 * mm
    tracked(c, "DANS LE PACK", M, y, "Fira-Semi", 8.2, COPPER, tracking=1.8)
    y -= 6.5 * mm
    for titre, desc in [
        ("Create et ses extensions", "Convoyeurs, trains, machines à vapeur, cuisine automatisée."),
        ("Cuisine et agriculture", "Des centaines de cultures et de recettes, du vin, de la bière."),
        ("Un monde refait", "Paysages, donjons, mines et temples repensés de fond en comble."),
        ("Créatures", "Des boss sérieux. N’y va pas en armure de cuir."),
        ("Confort", "Balises de téléportation, boussoles, carte, livre de recettes."),
    ]:
        y = para(c, f"<b>{titre}</b> — {desc}", st("Fira", 9.6, 13.6), M, y, COL)
        y -= 2.8 * mm

    c.setFont("Fira", 8.4); c.setFillColor(MUTED)
    c.drawCentredString(W / 2, 20 * mm, "Des questions ? Demande à Gordorak.  ·  github.com/ForestSound/MC_Deadmoon")
    c.showPage()

def build(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Minecraft Deadmoon — guide d’installation (Windows / Prism Launcher)")
    c.setAuthor("Gordorak"); c.setSubject("Installer le modpack avec Prism Launcher et rejoindre le serveur")
    for page in (page_1, page_2, page_3):
        page(c)
    c.save()
    print(f"{path} ({os.path.getsize(path)/1024:.0f} Ko, 3 pages)")

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Guide-Minecraft-Deadmoon.pdf"))
