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

LINK = "#B5651D"

def A(url, label=None):
    """Lien cliquable dans un Paragraph : coloré et souligné."""
    return f'<a href="{url}"><font color="{LINK}"><u>{label or url}</u></font></a>'

def link_area(c, url, x, y, w, h):
    """Rend une zone déjà dessinée cliquable (texte tracé au canvas)."""
    c.linkURL(url, (x, y, x + w, y + h), relative=0, thickness=0)

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
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v4.0")
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

def mono_box(c, text, x, y, w, size=9.4, pad=3.4 * mm, url=None):
    # wordWrap CJK : coupe n'importe où, seul moyen de replier une URL sans espaces
    style = ParagraphStyle("m", fontName="Mono", fontSize=size, leading=size * 1.5,
                           textColor=INK, wordWrap="CJK")
    p = Paragraph(text, style)
    _, th = p.wrapOn(c, w - 2 * pad, H)
    bh = th + 2 * pad
    c.setFillColor(HexColor("#EDEAE1")); c.setStrokeColor(RULE); c.setLineWidth(0.8)
    c.roundRect(x, y - bh, w, bh, 1.8 * mm, stroke=1, fill=1)
    c.setStrokeColor(COPPER); c.setLineWidth(2.2)
    c.line(x + 0.9, y - bh + 2.2 * mm, x + 0.9, y - 2.2 * mm)
    p.drawOn(c, x + pad, y - bh + pad)
    if url:
        link_area(c, url, x, y - bh, w, bh)
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
URL_PRISM = "https://prismlauncher.org/download/windows/"
URL_ZIP = "https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/dist/Minecraft-Deadmoon-Prism.zip"
URL_DEPOT = "https://github.com/ForestSound/MC_Deadmoon"

def page_1(c):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    y = H - 24 * mm
    tracked(c, "GUIDE D’INSTALLATION · WINDOWS", M, y, "Fira-Med", 8.2, COPPER, tracking=2.8)
    y -= 15 * mm
    c.setFont("Fira-Black", 32); c.setFillColor(INK)
    c.drawString(M - 1, y, "Minecraft Deadmoon")
    y -= 8 * mm
    para(c, "Quatre étapes pour installer le pack et nous rejoindre",
         st("Fira-Light", 12.5, 17, MUTED), M, y, COL)
    y -= 13 * mm
    c.setStrokeColor(RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)
    c.setFont("Fira", 7.6); c.setFillColor(MUTED)
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v4.0")
    c.drawRightString(W - M, 12 * mm, "1")
    y -= 10 * mm

    y = para(c, "Le pack ajoute <b>45 mods</b> à Minecraft. On l’installe avec <b>Prism Launcher</b>, "
                "un lanceur gratuit qui remplace celui de Minecraft — pas besoin de l’avoir déjà. "
                "Tout est préparé dans un fichier à importer : rien à régler, rien à copier à la main. "
                "Compte un quart d’heure, surtout de l’attente.",
             st("Fira", 10.4, 15.6), M, y, COL)
    y -= 5 * mm
    y = para(c, "Ensuite, <b>le pack se met à jour tout seul</b> à chaque lancement. Tu n’auras plus "
                "jamais à refaire ces étapes.", st("Fira", 10.4, 15.6), M, y, COL)
    y -= 8 * mm
    y = note_box(c, "CE QU’IL TE FAUT", [
        "Un compte <b>Minecraft Java Edition</b> — les versions Bedrock, Switch, PlayStation, Xbox et "
        "téléphone ne peuvent pas rejoindre le serveur.",
        "Un PC sous <b>Windows 10 ou 11</b>, environ <b>3 Go</b> de place libre.",
        "Tes identifiants <b>Microsoft</b>. Java, lui, s’installe tout seul avec Prism.",
    ], M, y, COL)

    y -= 9 * mm
    y = step(c, 1, "Installe Prism Launcher",
             "Sur " + A(URL_PRISM, "prismlauncher.org/download") + ", section <b>Windows</b>, prends le "
             "fichier <b>Installer (.exe)</b> et lance-le : installation classique, tout suivant. Si "
             "Windows affiche « Windows a protégé votre ordinateur », clique sur <b>Informations "
             "complémentaires</b> puis <b>Exécuter quand même</b>.", M, y, COL)
    y -= 6 * mm
    y = step(c, 2, "Ajoute ton compte Microsoft",
             "Prism demande d’abord la langue, puis propose de <b>télécharger Java</b> : accepte. "
             "Ensuite, en haut à droite : <b>Comptes → Gérer les comptes → Ajouter un compte "
             "Microsoft</b>, et connecte-toi avec le compte qui possède Minecraft.", M, y, COL)
    y -= 6 * mm
    y = step(c, 3, "Télécharge le pack et glisse-le dans Prism",
             "Clique sur le lien ci-dessous : il télécharge un petit fichier de 90 Ko. "
             "<b>Glisse-le directement sur la fenêtre de Prism</b>, et confirme. "
             "(Au clavier, ça marche aussi par <b>Ajouter une instance → Importer depuis un zip</b>.)",
             M, y, COL)
    y -= 3.5 * mm
    mono_box(c, A(URL_ZIP, "github.com/ForestSound/MC_Deadmoon → dist/Minecraft-Deadmoon-Prism.zip"),
             M, y, COL, size=8.6, url=URL_ZIP)
    c.showPage()

def page_2(c):
    y = page_frame(c, "SUITE ET FIN", "Lancer et nous rejoindre", 2)
    y = step(c, 4, "Double-clique sur l’instance « Minecraft Deadmoon »",
             "Prism installe Minecraft, le moteur de mods NeoForge, puis les 45 mods. "
             "Le premier lancement prend <b>5 à 10 minutes</b> et affiche beaucoup de lignes de texte : "
             "c’est normal, laisse faire. Les fois suivantes seront rapides.", M, y, COL)

    y -= 8 * mm
    bh = 26 * mm
    c.setFillColor(NIGHT); c.roundRect(M, y - bh, COL, bh, 2.4 * mm, stroke=0, fill=1)
    tracked(c, "ADRESSE DU SERVEUR", M + 8 * mm, y - 9 * mm, "Fira-Med", 7.6, COPPER, tracking=2.2)
    c.setFont("Mono-Bold", 15.5); c.setFillColor(MOON)
    c.drawString(M + 8 * mm, y - 19 * mm, "mcdeadmoon.omgserv.net:10023")
    y -= bh + 9 * mm

    y = step(c, 5, "Dans le jeu : Multijoueur → Ajouter un serveur",
             "<b>Nom</b> : ce que tu veux. <b>Adresse</b> : recopie celle ci-dessus en entier — le "
             "<font name='Mono' size='9'>:10023</font> en fait partie, sans lui ça ne marche pas. "
             "Valide, puis double-clique sur le serveur dans la liste : une barre verte signifie "
             "qu’il est allumé.", M, y, COL)

    y -= 10 * mm
    y = note_box(c, "SI ÇA COINCE", [
        "<b>L’import du fichier échoue</b> — demande à Gordorak le fichier <font name='Mono' "
        "size='8.6'>.mrpack</font>, qui s’importe de la même façon.",
        "<b>« Outdated server » ou « Outdated client »</b> — relance le jeu : la mise à jour des mods "
        "se fait au démarrage.",
        "<b>« Connection refused »</b> — le serveur redémarre, réessaie dans deux minutes.",
        "<b>Plantage au chargement</b> — clic droit sur l’instance → <b>Modifier → Paramètres → "
        "Java</b>, et monte la mémoire maximale à 8192 Mo.",
        "<b>Ça rame</b> — baisse la distance d’affichage à 8 ou 10 chunks dans les options vidéo.",
        "<b>Rien ne marche</b> — envoie à Gordorak le fichier <font name='Mono' size='8.6'>"
        ".minecraft/logs/latest.log</font> (clic droit sur l’instance → Dossier).",
    ], M, y, COL, accent=CRIMSON)

    y -= 8 * mm
    tracked(c, "DANS LE PACK", M, y, "Fira-Semi", 8.2, COPPER, tracking=1.8)
    y -= 6.5 * mm
    y = para(c, "<b>Create et ses extensions</b> (convoyeurs, trains, machines à vapeur, cuisine "
                "automatisée) · <b>cuisine et agriculture</b> (des centaines de cultures et de "
                "recettes, du vin, de la bière) · <b>un monde refait</b> (paysages, donjons, mines et "
                "temples repensés de fond en comble) · <b>créatures</b> (des boss sérieux, n’y va pas "
                "en armure de cuir) · <b>confort</b> (balises de téléportation, boussoles, carte, "
                "livre de recettes).", st("Fira", 9.6, 14), M, y, COL)

    y -= 5 * mm
    para(c, "Des questions ? Demande à Gordorak. Le pack et ce guide vivent sur "
            + A(URL_DEPOT, "github.com/ForestSound/MC_Deadmoon") + ".",
         st("Fira-It", 9.2, 13, MUTED), M, y, COL)
    c.showPage()

def build(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Minecraft Deadmoon — guide d’installation (Windows / Prism Launcher)")
    c.setAuthor("Gordorak"); c.setSubject("Importer l’instance Prism et rejoindre le serveur")
    page_1(c); page_2(c)
    c.save()
    print(f"{path} ({os.path.getsize(path)/1024:.0f} Ko, 2 pages)")

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Guide-Minecraft-Deadmoon.pdf"))
