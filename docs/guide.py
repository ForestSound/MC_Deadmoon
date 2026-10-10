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

# ---------------------------------------------------------------- page 1 : couverture
# dégradé du ciel : du presque noir en haut au bleu nuit en bas
SKY_TOP = (0.035, 0.043, 0.066)
SKY_BOT = (0.082, 0.098, 0.145)

def sky_rgb(y):
    """Couleur du ciel à l'ordonnée y (sert à découper le croissant sans raccord visible)."""
    t = max(0.0, min(1.0, 1 - y / H))
    return tuple(a + (b - a) * t for a, b in zip(SKY_TOP, SKY_BOT))

def cover(c):
    # dégradé en fines bandes (240 = raccords invisibles à l'impression comme à l'écran)
    n = 240
    for i in range(n):
        yb = H * (1 - (i + 1) / n)
        c.setFillColorRGB(*sky_rgb(yb + H / (2 * n)))
        c.rect(0, yb, W, H / n + 1, stroke=0, fill=1)

    # étoiles (graine fixe = rendu reproductible)
    rnd = random.Random(7)
    for _ in range(210):
        sx, sy = rnd.uniform(0, W), rnd.uniform(H * 0.28, H)
        c.setFillColor(MOON, alpha=rnd.uniform(0.12, 0.8))
        c.circle(sx, sy, rnd.choice([0.25, 0.35, 0.45, 0.6]), stroke=0, fill=1)
    c.setFillColor(MOON, alpha=1)

    # lune morte : halo cramoisi (du plus large au plus serré, très faible opacité) puis croissant
    mx, my, mr = W - 46 * mm, H - 62 * mm, 21 * mm
    for i in range(18, 0, -1):
        c.setFillColor(CRIMSON, alpha=0.022)
        c.circle(mx, my, mr + i * 1.9 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#E8E4D8")); c.circle(mx, my, mr, stroke=0, fill=1)
    # on creuse le croissant avec un disque exactement de la couleur du ciel à cette hauteur
    c.setFillColorRGB(*sky_rgb(my))
    c.circle(mx + 8.2 * mm, my + 3.4 * mm, mr * 0.95, stroke=0, fill=1)
    # cratères sur la faucille visible
    c.setFillColor(HexColor("#CDC7B6"), alpha=0.5)
    for dx, dy, dr in [(-13.5, 2.5, 2.1), (-10, -8.5, 1.4), (-15, -4.5, 0.9), (-9.5, 10, 1.1)]:
        c.circle(mx + dx * mm, my + dy * mm, dr * mm, stroke=0, fill=1)
    c.setFillColor(MOON, alpha=1)

    # titre
    y = H - 122 * mm
    tracked(c, "MODPACK MINECRAFT", M, y, "Fira-Med", 9.5, COPPER, tracking=3.4)
    y -= 26 * mm
    c.setFont("Fira-Black", 62); c.setFillColor(MOON)
    c.drawString(M - 1.5, y, "DEADMOON")
    y -= 9 * mm
    c.setStrokeColor(COPPER); c.setLineWidth(1.6)
    c.line(M, y, M + 46 * mm, y)
    y -= 13 * mm
    para(c, "Guide d\u2019installation et de connexion au serveur",
         st("Fira-Light", 15.5, 21, SILVER), M, y, COL * 0.8)

    # bandeau du bas : pastilles en haut, adresse en dessous (aucun chevauchement)
    bh = 58 * mm
    c.setFillColor(NIGHT_2); c.rect(0, 0, W, bh, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#2A3245")); c.setLineWidth(0.7); c.line(0, bh, W, bh)

    chips = [("MINECRAFT", "1.21.1"), ("LOADER", "NeoForge"), ("MODS", "45")]
    cw, ch, gap = 32 * mm, 16 * mm, 4 * mm
    cx = W - M - (cw * 3 + gap * 2)
    cy = bh - 11 * mm - ch
    for label, value in chips:
        c.setFillColor(HexColor("#1D2436")); c.setStrokeColor(HexColor("#2E3850"))
        c.setLineWidth(0.7); c.roundRect(cx, cy, cw, ch, 2.4 * mm, stroke=1, fill=1)
        tracked(c, label, cx + cw / 2, cy + ch - 6 * mm, "Fira-Med", 6.6, SILVER, 1.5, center=True)
        c.setFont("Fira-Semi", 12.5); c.setFillColor(MOON)
        c.drawCentredString(cx + cw / 2, cy + 4.4 * mm, value)
        cx += cw + gap

    ay = cy - 13 * mm
    tracked(c, "ADRESSE DU SERVEUR", M, ay, "Fira-Med", 8, SILVER, tracking=2.2)
    c.setFont("Mono-Bold", 16); c.setFillColor(MOON)
    c.drawString(M, ay - 10 * mm, "mcdeadmoon.omgserv.net:10023")
    c.showPage()

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
    c.drawString(M, 12 * mm, "Minecraft Deadmoon · guide v1.0")
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

# ---------------------------------------------------------------- page 2 : installation
def page_install(c):
    y = page_frame(c, "ÉTAPE 1 SUR 2", "Installer le modpack", 2)

    y = para(c, "Minecraft Deadmoon réunit <b>45 mods</b> : les machines de Create, une cuisine "
                "complète, des structures entièrement repensées et quelques créatures "
                "nettement moins accueillantes. Tout s’installe en une fois, depuis un seul fichier.",
             st("Fira", 10.6, 16), M, y, COL * 0.95)

    y -= 9 * mm
    y = note_box(c, "AVANT DE COMMENCER", [
        "Un compte <b>Minecraft Java Edition</b> (les versions Bedrock, Switch ou mobile ne peuvent pas rejoindre le serveur)",
        "Le launcher <b>CurseForge</b>, gratuit — <font name='Mono' size='8.6'>curseforge.com/download</font>",
        "Environ <b>3 Go</b> d’espace disque libre et <b>8 Go</b> de mémoire vive recommandés",
    ], M, y, COL)

    y -= 11 * mm
    y = step(c, 1, "Récupère le fichier du pack",
             "David t’envoie <font name='Mono' size='8.8'>Minecraft-Deadmoon-1.0.0-curseforge.zip</font> "
             "(191 Mo). Ne le décompresse pas : le launcher s’en occupe.", M, y, COL)
    y -= 5.4 * mm
    y = step(c, 2, "Installe le launcher CurseForge",
             "Télécharge-le sur curseforge.com/download, installe-le, puis ouvre l’onglet "
             "<b>Minecraft</b> dans la colonne de gauche.", M, y, COL)
    y -= 5.4 * mm
    y = step(c, 3, "Importe le pack",
             "Clique sur <b>Créer un profil personnalisé</b>, puis sur le bouton <b>Importer</b> "
             "en haut à droite de la fenêtre, et choisis le fichier zip. Le launcher installe "
             "NeoForge 1.21.1 et les 45 mods tout seul — compte 5 à 10 minutes.", M, y, COL)
    y -= 5.4 * mm
    y = step(c, 4, "Donne-lui de la mémoire",
             "Survole le profil, clique sur la roue crantée, puis <b>Paramètres → Mémoire allouée</b> : "
             "règle sur <b>6 Go</b> minimum (8 Go si ta machine le permet). Sans ça, le jeu plantera "
             "au chargement du monde.", M, y, COL)
    y -= 5.4 * mm
    y = step(c, 5, "Lance le jeu",
             "Bouton <b>Jouer</b>. Le tout premier démarrage prend 3 à 5 minutes : c’est normal, "
             "le jeu assemble les recettes et les textures de tous les mods. Les suivants seront rapides.",
             M, y, COL)

    y -= 7 * mm
    note_box(c, "ET ENSUITE ?", [
        "Le pack est installé : la page suivante explique comment rejoindre tout le monde sur le serveur <b>Deadmoon</b>.",
        "Garde le fichier zip, il resservira en cas de réinstallation.",
    ], M, y, COL)
    c.showPage()

# ---------------------------------------------------------------- page 3 : le serveur
def page_server(c):
    y = page_frame(c, "ÉTAPE 2 SUR 2", "Rejoindre le serveur", 3)

    # carte d'adresse
    bh = 28 * mm
    c.setFillColor(NIGHT); c.roundRect(M, y - bh, COL, bh, 2.4 * mm, stroke=0, fill=1)
    rnd = random.Random(3)
    for _ in range(45):
        c.setFillColor(MOON, alpha=rnd.uniform(0.1, 0.55))
        c.circle(rnd.uniform(M + 2, M + COL - 2), rnd.uniform(y - bh + 2, y - 2), rnd.choice([0.25, 0.4]), stroke=0, fill=1)
    c.setFillColor(MOON, alpha=1)
    tracked(c, "ADRESSE À COPIER", M + 8 * mm, y - 9.5 * mm, "Fira-Med", 7.6, COPPER, tracking=2.2)
    c.setFont("Mono-Bold", 15.5); c.setFillColor(MOON)
    c.drawString(M + 8 * mm, y - 20 * mm, "mcdeadmoon.omgserv.net:10023")
    y -= bh + 10 * mm

    y = step(c, 1, "Ouvre le menu Multijoueur",
             "Depuis l’écran titre de Minecraft, une fois le pack lancé.", M, y, COL)
    y -= 5.5 * mm
    y = step(c, 2, "Clique sur « Ajouter un serveur »", "", M, y, COL)
    y -= 5.5 * mm
    y = step(c, 3, "Nom du serveur",
             "Mets ce que tu veux, par exemple <b>Deadmoon</b>. Ce champ ne sert qu’à toi.", M, y, COL)
    y -= 5.5 * mm
    y = step(c, 4, "Adresse du serveur",
             "Recopie l’adresse ci-dessus <b>en entier</b>. Le <font name='Mono' size='9'>:10023</font> "
             "à la fin est indispensable : sans lui, la connexion échouera.", M, y, COL)
    y -= 5.5 * mm
    y = step(c, 5, "Terminé, puis double-clique sur le serveur",
             "Il apparaît dans ta liste. Une barre verte à droite du nom signifie qu’il est en ligne : "
             "double-clique, et tu arrives au milieu des autres.",
             M, y, COL)

    y -= 11 * mm
    note_box(c, "SI ÇA COINCE", [
        "<b>« Outdated server » ou « Outdated client »</b> — tes mods ne correspondent pas à ceux du serveur. "
        "Réimporte le zip envoyé par David, sans ajouter ni retirer de mod.",
        "<b>Barre rouge, « Connection refused »</b> — le serveur est éteint ou redémarre. Réessaie dans deux minutes.",
        "<b>Le jeu plante au chargement</b> — monte la mémoire allouée à 8 Go (étape 4 page précédente).",
        "<b>Tu ne reconnais plus rien</b> — c’est voulu : le monde est entièrement régénéré. "
        "Fabrique une boussole d’exploration pour retrouver les structures.",
        "<b>Rien n’y fait</b> — envoie à David le fichier <font name='Mono' size='8.6'>latest.log</font>, "
        "dans le dossier <font name='Mono' size='8.6'>logs</font> du profil.",
    ], M, y, COL, accent=CRIMSON)
    c.showPage()

# ---------------------------------------------------------------- page 4 : contenu
def page_content(c):
    y = page_frame(c, "POUR ALLER PLUS LOIN", "Ce qu’il y a dedans", 4)

    blocks = [
        ("CREATE ET SES EXTENSIONS",
         "Create · Central Kitchen · Crafts & Additions · Steam ’n’ Rails · Confectionery",
         "Convoyeurs, trains, machines à vapeur, et de quoi automatiser la cuisine."),
        ("CUISINE ET AGRICULTURE",
         "Farmer’s Delight · Expanded Delight · Ube’s Delight · Brewin’ and Chewin’ · Croptopia · "
         "Let’s Do : Farm & Charm, Vinery, Bakery, Brewery, Candlelight",
         "Des centaines de cultures et de recettes, du vin, de la bière, des dîners aux chandelles."),
        ("UN MONDE REMANIÉ",
         "Terralith · les 10 mods YUNG’s Better · When Dungeons Arise · Dungeons and Taverns",
         "Nouveaux biomes, donjons, mines, temples et forteresses repensés de fond en comble."),
        ("CRÉATURES",
         "Mowzie’s Mobs · L_Ender’s Cataclysm",
         "Des boss sérieux. Ne pars pas les chercher en armure de cuir."),
        ("CONFORT",
         "Waystones · Explorer’s Compass · Nature’s Compass · EMI · Jade · Xaero’s Minimap & World Map",
         "Téléportation entre balises, recherche de structures et de biomes, recettes et carte."),
    ]
    for kicker, mods, desc in blocks:
        tracked(c, kicker, M, y, "Fira-Semi", 8, COPPER, tracking=1.8)
        y -= 6.2 * mm
        y = para(c, mods, st("Fira-Med", 9.8, 14.2, INK), M, y, COL)
        y = para(c, desc, st("Fira", 9.3, 13.4, MUTED), M, y - 1.2 * mm, COL)
        y -= 7 * mm

    y -= 2 * mm
    c.setStrokeColor(RULE); c.setLineWidth(0.8); c.line(M, y, W - M, y)
    y -= 7 * mm

    tracked(c, "VARIANTE : PRISM LAUNCHER, MISES À JOUR AUTOMATIQUES", M, y, "Fira-Semi", 8, INK, tracking=1.8)
    y -= 7 * mm
    y = para(c, "Avec <b>Prism Launcher</b> (gratuit), le pack se met à jour tout seul à chaque lancement : "
                "plus besoin qu’on te renvoie un zip de 191 Mo. Crée une instance <b>Minecraft 1.21.1 + "
                "NeoForge 21.1.257</b>, dépose <font name='Mono' size='8.6'>packwiz-installer-bootstrap.jar</font> "
                "dans son dossier, puis colle cette commande dans <i>Paramètres → Commandes personnalisées → "
                "Pre-launch</i> :",
             st("Fira", 9.8, 14.4), M, y, COL)
    y -= 4 * mm
    y = mono_box(c, '"$INST_JAVA" -jar packwiz-installer-bootstrap.jar<br/>'
                    'https://raw.githubusercontent.com/ForestSound/MC_Deadmoon/main/pack/pack.toml',
                 M, y, COL, size=8.6)

    c.setFont("Fira", 8.4); c.setFillColor(MUTED)
    c.drawCentredString(W / 2, 20 * mm, "Pack maintenu par David  ·  github.com/ForestSound/MC_Deadmoon  ·  octobre 2026")
    c.showPage()

# ---------------------------------------------------------------- assemblage
def build(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle("Minecraft Deadmoon — guide d’installation")
    c.setAuthor("David"); c.setSubject("Installation du modpack et connexion au serveur")
    cover(c); page_install(c); page_server(c); page_content(c)
    c.save()
    print(f"{path} ({os.path.getsize(path)/1024:.0f} Ko)")

if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Guide-Minecraft-Deadmoon.pdf"))
