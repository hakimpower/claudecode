---
version: alpha
name: Power Recharge — Frame
description: >
  Charte graphique de POWER RECHARGE (SARL, SIREN 947 650 958, Juziers 78), installateur de
  bornes de recharge pour véhicules électriques (IRVE) à domicile, partout en France.
  Fond vert-noir profond, dégradé signature turquoise → jaune électrique, display géométrique
  « techno » (Rigelstar) + sans-serif géométrique (Berlin). Source : brand/charte-graphique.jpg.
unit: the frame — 1920×1080 primary; 9:16 and 1:1 allowed
principle: atoms are sacred · composition is free · numbers come from the script
tagline: "Le pouvoir de recharger !"

colors:
  night: "#102203"          # fond principal — RGB 16,34,3 · CMYK 52,0,91,86
  teal: "#01998E"           # départ du dégradé
  volt: "#F6FE67"           # fin du dégradé (jaune électrique)
  white: "#FFFFFF"
  mist: "#F7F7F7"           # fond clair secondaire (pages de la charte)
  ink: "#0B0F2E"            # titres sur fond clair
  icon-grey: "#A6A6A6"      # icône monochrome
  gradient: "linear-gradient(90deg, #01998E 0%, #F6FE67 100%)"

typography:
  # — display (Rigelstar) : géométrique, futuriste, MAJUSCULES —
  display:   { fontFamily: "Rigelstar", fallback: "Orbitron, Michroma, sans-serif", cqw: 9.0, weight: 400, lineHeight: 0.95, tracking: "0.04em", upper: true }
  headline:  { fontFamily: "Rigelstar", fallback: "Orbitron, Michroma, sans-serif", cqw: 5.0, weight: 400, lineHeight: 1.0, tracking: "0.04em", upper: true }
  # — texte (Berlin) : sans-serif géométrique, net et moderne —
  subtitle:  { fontFamily: "Berlin", fallback: "Urbanist, Poppins, sans-serif", cqw: 2.2, weight: 700, lineHeight: 1.15 }
  body:      { fontFamily: "Berlin", fallback: "Urbanist, Poppins, sans-serif", cqw: 1.1, weight: 400, lineHeight: 1.5 }
  label:     { fontFamily: "Berlin", fallback: "Urbanist, Poppins, sans-serif", px: 16, weight: 500, tracking: "0.18em", upper: true }

spacing:
  pad: "5cqw"
  gap-md: "2cqw"

components:
  logo-badge:
    description: >
      Logo officiel : voiture-prise (contour + deux roues + câble et fiche) au-dessus de
      « POWER RECHARGE », le tout dans un cercle fin, rempli du dégradé teal → volt, sur fond night.
      Ne jamais recolorer ni déformer.
  icon:
    description: >
      Pictogramme seul (voiture dont le câble se termine par une fiche). Version dégradé sur fond
      sombre, version monochrome {colors.icon-grey} ou blanche sur fond clair.
  gradient-text:
    backgroundColor: "{colors.gradient}"
    description: "Mots-clés et chiffres forts : texte rempli du dégradé (background-clip:text) sur fond night."
---

## Overview

Power Recharge installe des bornes de recharge pour véhicules électriques chez les particuliers,
partout en France. Ton : moderne, technologique, fiable, accessible. Signature : **« Le pouvoir de
recharger ! »**.

## The Frame

- Fond par défaut : **night `#102203`** plein. Le dégradé teal → volt est l'unique source
  d'éclat : texte clé, traits de câble, barres de charge, halos lumineux.
- Fond clair (`#F7F7F7` / blanc) autorisé pour des cartons d'info ; titres alors en `ink`.
- Motif naturel de la marque : le **câble** de l'icône — une ligne fluide qui se termine par une
  fiche, et une **jauge de charge** qui se remplit du teal au jaune.

## Composition Rules

- Do : Rigelstar en majuscules pour les titres courts (1–4 mots) ; Berlin pour tout le reste.
- Do : le dégradé toujours dans le sens teal → volt (gauche→droite ou bas→haut, comme une charge).
- Do : logo sur fond night avec une marge de sécurité ≥ la hauteur du « P ».
- Don't : pas d'autres couleurs vives ; pas de dégradé inversé ; pas de Rigelstar en paragraphe.
- Don't : ne pas recolorer, étirer ni redessiner le logo.

## Fonts note

Rigelstar et Berlin ne sont pas sur Google Fonts : déposer les fichiers (`.woff2`/`.otf`) dans
`brand/fonts/` pour un rendu exact. À défaut, utiliser les fallbacks indiqués (Orbitron / Urbanist).
