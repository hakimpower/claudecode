# Audit migration Zapier → n8n — Power Recharge

Audit réalisé le 09/10/2026 (soir). Sources réellement consultées : alertes et factures Zapier reçues dans
Gmail, Zapier MCP (applications connectées, Skills), Google Drive, Routines Claude du compte.
Aucune donnée client n'est recopiée dans ce document (RGPD).

## 0. Ce qui a pu être vérifié, et ce qui ne l'a pas été

| Élément du compte rendu précédent | Vérifié ? | Constat |
|---|---|---|
| 19 Zaps sur Zapier | Partiellement | **13 noms de Zaps retrouvés** (voir §1). Les 6 autres n'ont jamais généré d'alerte et ne sont pas visibles sans accès à la liste des Zaps. |
| 13 Zaps actifs | Non | Impossible à lister sans connexion « Zapier Manager ». **4 Zaps sont certainement actifs** (erreurs reçues après le 31/08/2026) et 2 ont été mis en pause par Zapier le 11/04/2026. |
| Workflows déjà enregistrés dans n8n | Non | L'instance est `powerrecharge.app.n8n.cloud` (n8n Cloud, **compte d'essai créé le 09/10/2026 à 20h15 UTC**). Tous les workflows existants datent donc de ce soir. L'instance est **bloquée par la politique réseau** de cet environnement : aucun workflow n'a pu être lu. |
| Aucun workflow n8n publié | Non vérifiable | Idem. |
| Zap V2C de 71 étapes | Probable, non confirmé | Le candidat est « AUTO SITE DEVIS AXONAUT V2C » (Zap 363788427). Le nombre d'étapes n'est pas lisible sans l'éditeur Zapier ou un export. |
| Problème de pièces jointes Ekwateur | **Confirmé (cause probable)** | Le Zap EKWATEUR (369520892) échoue sur une étape « Webhooks by Zapier » : *Task timed out after 160 seconds*. C'est la signature typique d'un téléchargement ou envoi de fichier trop long. |
| Destinataires incomplets | **Confirmé, y compris dans Zapier** | NOTIF 5 (367070661) échoue avec *« needs at least one To, Cc or Bcc address »* : le champ destinataire est vide pour certains déclenchements **dans le Zap de production actuel**. |
| Champs Facebook « Province » / « Code Postal » | Non vérifié | À vérifier dans le formulaire Facebook Lead Ads (connexion Facebook disponible dans Zapier). |
| Connexions Gmail, Axonaut, Facebook, Sheets côté n8n | Non vérifiable | Côté **Zapier**, elles existent toutes : Axonaut (1), Google Sheets (1), Gmail (3 comptes), Facebook Lead Ads (1), WPForms (1), Zoho Invoice, Zoho Sign, WhatsApp Notifications. **WhatsApp Business : 0 connexion.** |

## 1. Inventaire des Zaps identifiés

Classement par priorité métier (1 = la plus haute, selon votre ordre) puis par complexité.

| # | Zap | ID Zapier | Domaine | État constaté | Dernière erreur connue | Priorité | Complexité |
|---|---|---|---|---|---|---|---|
| 1 | **PUB FB SHEET GMAIL** | 277279036 | Prospects Facebook → Google Sheets → email | **Actif** (erreur le 05/10/2026) | « The service is currently unavailable » (panne passagère côté application) — 9 alertes depuis août | 1–2 | Moyenne |
| 2 | **AUTO SITE DEVIS AXONAUT V2C** | 363788427 | Formulaire site → client + devis Axonaut, forfaits V2C | **Actif** (erreur le 01/09/2026) | Axonaut `GET /api/v2/quotations/{id}` : *socket hang up* (coupure réseau Axonaut, aucune relance automatique) | 2–3–4 | **Très élevée** (probable Zap de 71 étapes) |
| 3 | (Nv. design) AUTO SITE DEVIS AXONAUT | à récupérer | Ancienne version du flux site → devis | Probablement remplacé par le n°2 (24 alertes, la dernière le 06/08/2026) | — | 2–3 | Élevée |
| 4 | **EKWATEUR** | 369520892 | Dossiers partenaire Ekwateur + pièces jointes | **Actif** (erreur le 02/09/2026) | Webhooks by Zapier : délai dépassé de 160 s | 5 | Élevée |
| 5 | **NOTIF 5** | 367070661 | Notification email | **Actif** (erreur le 31/08/2026) | Gmail : aucun destinataire | 6 | Faible |
| 6 | NOTIF 8 | à récupérer | Notification | Probablement actif (alerte le 01/08/2026) | — | 6 | Faible |
| 7 | NOTIF 3 | à récupérer | Notification | Probablement actif (alerte le 24/07/2026) | — | 6 | Faible |
| 8 | NOTIF 2 | à récupérer | Notification | Inconnu (alerte le 17/06/2026) | — | 6 | Faible |
| 9 | NOTIF 7 | à récupérer | Notification | Inconnu (alerte le 17/06/2026) | — | 6 | Faible |
| 10 | MAIL DE RELANCE 1 | à récupérer | Relance commerciale | Inconnu (alerte le 29/06/2026) | — | 7 | Moyenne |
| 11 | MAIL DE RELANCE 2 | à récupérer | Relance commerciale | Inconnu (alerte le 17/06/2026) | — | 7 | Moyenne |
| 12 | Add new Facebook Lead Ads leads to rows on Google Sheets | à récupérer | Prospects Facebook → Sheets | **En pause depuis le 11/04/2026** (fonction hors forfait) | — | 1 | Faible |
| 13 | Untitled Zap | à récupérer | Inconnu | **En pause depuis le 11/04/2026** (fonction hors forfait) | — | ? | ? |
| 14–19 | *non identifiés* | — | Volteam ? Devis signé → Sheets ? Webhooks du tableau de bord installateurs ? | — | — | — | — |

Les Zaps 14 à 19 peuvent correspondre aux 4 Zaps décrits dans le guide Drive de mai 2025 (*Devis signé Axonaut → dossier + email*, *Dossier affecté → email installateur*, *RDV confirmé*, *Installation terminée*). Ce n'est **pas confirmé**. Je n'ai trouvé **aucune trace de Volteam** dans les alertes Zapier.

### Autres automatisations existantes (hors Zapier) à ne pas dupliquer

| Automatisation | Où | État | Rôle |
|---|---|---|---|
| **EKWATEUR email triage** | Routine Claude (tous les jours, 06h00 UTC) | **Active**, dernière exécution réussie le 09/10/2026 | Lit les emails Ekwateur et envoie le « Récapitulatif quotidien EKWATEUR » (dossiers en attente, installations non facturées). C'est déjà un premier **agent partenaires**. |
| RECAP STOCK LUNDI EKWATEUR | Routine Claude (lundi 07h00 UTC) | Désactivée depuis le 07/09/2026 | Récapitulatif hebdomadaire du stock Ekwateur |
| CHECK STOCK CHAQUE JOUR | Routine Claude (jours ouvrés, 06h00 UTC) | Désactivée depuis le 07/09/2026 | Rapport de stock quotidien |
| Skills Zapier « ajouter-installateur », « installation-terminee-mise-a-jour », « devis-signe-vers-chantier » | Zapier MCP | Exécutables à la demande | Mise à jour de la feuille « géo bornes » (onglet CHANTIERS, statuts `devis_signe` → `installation_terminee`) |

### Données de référence repérées

- Feuilles de suivi : « Suivi Leads V2C 2.0 », « SUIVI LEADS V2C », « Suivi dossiers installations 2025 », « géo bornes » (onglet 📋 CHANTIERS), « STOCK EKWATEUR – POWER RECHARGE ».
- Statuts prospects V2C utilisés : *Pas contacté, Devis automatique, Devis envoyé, En attente de devis, Pas de réponse, A rappeler par Hakim, Ne plus rappeler*.
- Critères techniques déjà collectés : type de logement (maison / appartement / entreprise), puissance de l'abonnement (6, 9, 12 kVA mono, 15 kVA tri…), distance tableau–borne, délestage, gestion solaire. Ce sont les **entrées naturelles de l'agent devis**.
- Ces feuilles contiennent des données personnelles (nom, email, téléphone, adresse) : accès restreint et durée de conservation à définir (RGPD).

## 2. Tableau de correspondance Zap ↔ workflow n8n

Je n'ai pas pu lire n8n. La colonne « Workflow n8n » doit être complétée à la première connexion. La règle est de **reprendre le workflow existant s'il y en a un et de ne jamais en créer un deuxième**.

| Zap | Workflow n8n existant | Nom cible n8n | Statut migration |
|---|---|---|---|
| PUB FB SHEET GMAIL | à vérifier | `P1 – Prospects Facebook → Sheets + email` | Non commencé (côté vérifié) |
| Add new Facebook Lead Ads leads… (en pause) | à vérifier | fusionné dans le précédent | Non commencé |
| AUTO SITE DEVIS AXONAUT V2C | à vérifier | `P2 – Formulaire site → Axonaut client + devis V2C` | Non commencé |
| (Nv. design) AUTO SITE DEVIS AXONAUT | à vérifier | à archiver si confirmé obsolète | Non commencé |
| EKWATEUR | à vérifier | `P5 – Ekwateur dossiers + pièces jointes` | Non commencé |
| NOTIF 2 / 3 / 5 / 7 / 8 | à vérifier (« tests hors ligne réussis » selon le compte rendu) | `P6 – Notifications internes` (1 workflow avec un aiguillage, ou 5 petits workflows) | Non commencé |
| MAIL DE RELANCE 1 / 2 | à vérifier | `P7 – Relances commerciales` | Non commencé |
| Untitled Zap | à vérifier | — | Non commencé |
| Zaps 14 à 19 | à vérifier | — | Non commencé |

« Non commencé » signifie : rien n'a été vérifié ou testé de mon côté. Si des workflows existent déjà dans n8n, ils passeront à « Créé » une fois inspectés.

## 3. Constats importants pour la suite

1. **Le coût Zapier dérape chaque mois.** Le forfait comprend 750 tâches. Il est dépassé tous les mois depuis décembre 2025, et les tâches supplémentaires sont facturées 1,25× puis **2,5×** le tarif de base (alertes du 31/08 et du 12/09/2026). Le Zap V2C, avec ses dizaines d'étapes, consomme des dizaines de tâches par prospect. Sur n8n, **une exécution compte pour 1, quel que soit le nombre d'étapes**.
2. **Trois des quatre erreurs récentes sont passagères** (Facebook indisponible, Axonaut *socket hang up*, délai webhook dépassé). Dans Zapier, elles ne sont pas relancées automatiquement et des prospects ou devis ont pu être perdus. Dans n8n : *Retry on fail* (3 essais, 5 à 30 s d'écart) sur chaque appel API, et un workflow d'erreurs central.
3. **NOTIF 5 a un vrai défaut métier** : son destinataire est parfois vide. Il faut définir qui doit recevoir cette notification (information métier à fournir) et ajouter une valeur de repli.
4. **Ekwateur** : la piste à vérifier en priorité est l'étape webhook qui dépasse 160 s. Dans n8n, la pièce jointe se manipule en binaire natif (Gmail → Drive/Axonaut), sans service intermédiaire, avec un délai réglable.
5. **L'essai n8n Cloud expire environ le 23/10/2026** (14 jours). Une décision d'abonnement devra être prise avant cette date, faute de quoi les workflows préparés ne seront plus accessibles.
