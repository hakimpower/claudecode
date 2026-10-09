# Plan de migration, agents IA et guide n8n — Power Recharge

Complète `01-audit-zapier-n8n.md`. Règle de base : **Zapier reste la production** tant qu'un workflow n8n
n'a pas passé toutes les étapes ci-dessous **et** reçu votre accord écrit.

## 1. Accès et validations nécessaires (bloquants)

| # | Ce qu'il faut | Pourquoi | Qui |
|---|---|---|---|
| A1 | Autoriser le domaine `powerrecharge.app.n8n.cloud` dans les paramètres réseau de l'environnement Claude Code (menu de l'environnement → Modifier → Accès réseau → Domaines autorisés) | Sans cela, je ne peux ni lire ni corriger les workflows n8n | Vous |
| A2 | Créer une clé API n8n (n8n → Settings → n8n API → Create API key) et l'enregistrer comme **secret d'environnement** `N8N_API_KEY`, jamais dans le chat | Lire et modifier les workflows sans stocker la clé dans un nœud | Vous |
| A3 | Ouvrir le lien de connexion « Zapier Manager » que je vous ai donné | Lister les 19 Zaps et leur état actif/inactif | Vous |
| A4 | Exporter les Zaps (dans les paramètres du compte Zapier, rubrique d'export des données ; si l'option n'existe pas dans votre forfait, des captures d'écran de chaque étape) et déposer le fichier dans Google Drive | **Seule source fiable** des étapes, filtres, chemins, formules et code. Indispensable pour reproduire le Zap V2C à l'identique | Vous |
| A5 | Créer dans n8n les credentials : Gmail (OAuth), Google Sheets/Drive (OAuth), Facebook Lead Ads (OAuth), Axonaut (Header Auth `userApiKey`) | Les authentifications OAuth doivent être faites par le titulaire du compte | Vous, guidé |
| A6 | Informations métier : destinataire(s) de NOTIF 5, liste des emails internes à notifier, ce que doit faire le Zap « Untitled » | Le compte rendu les signalait déjà comme incomplets | Vous |
| A7 | Choisir l'abonnement n8n avant la fin de l'essai (~23/10/2026) | Sinon, l'instance et les workflows deviennent inaccessibles | Vous |

Sécurité appliquée dès maintenant : sur le serveur Zapier MCP, j'ai activé « Zapier Manager » en lecture et **retiré les actions « inviter un membre » et « valider une demande »**. L'action « Turn Zap On/Off » reste présente, car c'est elle qui fournit la liste des Zaps, mais **je ne l'exécuterai jamais** sans votre accord explicite. Vous pouvez aussi la retirer vous-même.

## 2. Procédure de migration, workflow par workflow

Chaque workflow suit les mêmes étapes. On ne passe à l'étape suivante que si les critères sont remplis.

| Étape | Ce qui est fait | Critère pour passer à la suite |
|---|---|---|
| 1. Relevé | Lecture du Zap (export JSON) : déclencheur, filtres, chemins, formules, champs obligatoires | Chaque étape du Zap a un équivalent n8n identifié |
| 2. Construction | Reprise du workflow n8n existant (jamais de doublon). Credentials n8n uniquement. Nœud **Config** en tête avec `MODE = test` | Le workflow s'enregistre sans erreur |
| 3. Tests à blanc | Données de test épinglées (*pinned data*), une par branche (chaque chemin et chaque filtre). En `MODE = test`, les emails partent vers une adresse de test, et les écritures Axonaut et Sheets sont remplacées par une écriture dans une feuille « n8n – bac à sable » | 100 % des branches passent et les résultats sont identiques au Zap (montants, forfaits, statuts) |
| 4. Mode fantôme (7 jours) | Le workflow n8n reçoit les mêmes événements que Zapier, mais n'écrit que dans le journal. Comparaison quotidienne avec l'historique Zapier | 0 écart sur 7 jours, ou écarts expliqués et corrigés |
| 5. Bascule (sur votre accord) | Dans la même minute : activer le workflow n8n en `MODE = prod`, puis couper le Zap. Les URL de webhook sont changées à la source (formulaire du site) | Premier événement réel traité correctement |
| 6. Surveillance (14 jours) | Le Zap reste **intact mais éteint**. Résumé quotidien de supervision | Aucune erreur non résolue |
| 7. Clôture | Le Zap reste archivé, jamais supprimé | Votre validation |

### Éviter les doubles déclenchements et les doublons

- **Un seul système écrit à la fois.** En mode fantôme, n8n n'écrit nulle part ailleurs que dans son journal.
- **Clé d'unicité** pour chaque événement : `leadgen_id` pour Facebook, identifiant de soumission ou email + téléphone normalisés pour le site, numéro DIB pour Ekwateur. Elle est enregistrée dans une table n8n (*Data Table*) « deja_traites ». Une clé déjà présente arrête l'exécution.
- **Axonaut** : recherche du client par email ou téléphone avant toute création. Aucun devis n'est créé si un devis lié à la même clé existe déjà.
- Les webhooks n8n et Zapier ont des URL différentes. Seule la source (le site) choisit où elle envoie.

### Gestion des erreurs et journal

- *Retry on fail* sur chaque appel externe (3 essais, avec un délai croissant).
- Un workflow `00 – Gestion des erreurs` (nœud *Error Trigger*) relié à tous les autres : il écrit dans la feuille « n8n – journal » (date, workflow, étape, message, clé d'unicité, sans données sensibles) et vous envoie une alerte.
- Les exécutions réussies et échouées sont conservées dans n8n. Une exécution échouée peut être **rejouée** depuis l'écran *Executions*.

### Retour arrière vers Zapier (moins de 5 minutes)

1. Dans n8n, désactiver le workflow (interrupteur *Active* en haut à droite).
2. Dans Zapier, rallumer le Zap correspondant (il n'a jamais été modifié ni supprimé).
3. Si le flux est déclenché par webhook, remettre l'URL Zapier dans le formulaire source.
4. Dans le journal n8n, repérer les événements reçus pendant l'incident et les rejouer côté Zapier ou à la main.

## 3. Architecture des agents IA

Principe : l'IA **lit, classe, rédige et signale**. Elle ne fixe **jamais** un prix, n'envoie jamais un devis, ne prend aucun engagement et ne fait aucune action irréversible. Toute action sortante passe par une validation humaine (brouillon Gmail, ligne « à valider » dans Sheets, ou bouton d'approbation n8n).

| Agent | Déclencheur | L'IA apporte | Reste déterministe (sans IA) | Validation humaine | État |
|---|---|---|---|---|---|
| **Commercial** | Nouveau prospect (après le workflow P1/P2) | Score de priorité et justification, informations manquantes, brouillon de réponse WhatsApp ou email, proposition « appel » ou « devis » | Dédoublonnage, normalisation téléphone et code postal, département | Brouillon à relire avant tout envoi | À construire après P1/P2 |
| **Devis** | Prospect complet (puissance, distance, logement, photos) | Lecture des photos (tableau électrique, emplacement), contraintes techniques (triphasé, distance > 15 m, appartement ou copropriété) | **Calcul du forfait et du prix**, à reprendre à l'identique du Zap V2C | Toujours : l'agent prépare, vous validez dans Axonaut | À construire après P2 |
| **Administratif** | Quotidien + nouveaux emails avec pièces jointes | Vérification que les pièces reçues sont les bonnes (attestation, photos, rapport), relance des dossiers incomplets | Classement dans Drive, mise à jour des statuts | Brouillons de relance | À construire |
| **Partenaires** | Emails Ekwateur, TBS/Kizeo, Volteam | Classement (pré-visite / installation / relance urgente / rapport), détection d'urgence, résumé | Extraction du numéro DIB, statut dans Sheets | Alerte sur les urgences | **Existe déjà en partie** : Routine Claude « EKWATEUR email triage » (récap quotidien). À conserver, et à brancher plus tard sur n8n |
| **Supervision** | Toutes les heures + résumé quotidien | Résumé lisible des incidents | Comptage des exécutions, erreurs, doublons, workflows sans activité anormalement longue | Non | À construire avec `00 – Gestion des erreurs` |

Pour l'IA dans n8n, le nœud *AI Agent* ou *Basic LLM Chain* est relié à un credential Anthropic, avec un modèle léger (classe Haiku) pour le tri et un modèle plus capable seulement pour la lecture de photos. La sortie est imposée au format JSON (*structured output*) pour être exploitée par des nœuds classiques.

## 4. Estimation des coûts mensuels (ordre de grandeur, à confirmer)

| Poste | Aujourd'hui | Après migration |
|---|---|---|
| Zapier | Forfait 750 tâches **+ dépassement mensuel facturé 1,25× à 2,5×** (constaté de décembre 2025 à septembre 2026) | Plus rien une fois tous les Zaps migrés et validés (garder le forfait gratuit pour le retour arrière pendant 1 mois) |
| n8n Cloud | — | Offre « Starter » ou « Pro » selon le volume (en 2025 : environ 24 € pour 2 500 exécutions et environ 60 € pour 10 000). **Tarif 2026 à vérifier sur la page de facturation de l'essai** |
| IA (API Anthropic) | Routines Claude existantes | Quelques euros à quelques dizaines d'euros par mois pour quelques centaines de prospects (tri avec un modèle léger ; la lecture de photos coûte plus cher) |
| **Total estimé** | Forfait Zapier + dépassements | **environ 30 à 90 €/mois** selon l'offre n8n et le volume d'IA |

Les montants exacts de votre facture Zapier ne figurent pas dans les emails consultés. Une comparaison précise demande la page *Billing* de Zapier.

## 5. Guide n8n pour débutant

**Vocabulaire Zapier → n8n**

| Zapier | n8n |
|---|---|
| Zap | Workflow |
| Trigger | Nœud déclencheur (le premier, avec l'icône éclair) |
| Action | Nœud |
| Filter | Nœud *If* ou *Filter* |
| Paths | Nœud *Switch* |
| Formatter | Nœud *Edit Fields (Set)* ou *Code* |
| Zap On/Off | Interrupteur **Active** en haut à droite du workflow |
| Zap History | Onglet **Executions** |
| Connected accounts | **Credentials** (menu de gauche) |
| Task (facturée par étape) | Exécution (facturée **une fois** par passage, quel que soit le nombre de nœuds) |

**Les gestes de base**

- **Tester sans risque** : ouvrir le workflow, cliquer sur *Test workflow*. Avec des données épinglées (icône punaise sur le déclencheur), le test rejoue toujours le même exemple. Tant que le nœud Config est en `MODE = test`, rien de réel n'est envoyé.
- **Voir ce qui s'est passé** : onglet *Executions*. Chaque passage y apparaît en vert (réussi) ou en rouge (échec). En cliquant dessus, on voit les données entrées et sorties à chaque nœud.
- **Rejouer une exécution échouée** : depuis *Executions*, bouton *Retry*.
- **Désactiver un workflow** : basculer l'interrupteur *Active* sur Off. Effet immédiat, rien n'est supprimé.
- **Ne jamais faire** : supprimer un workflow, coller une clé API dans un nœud, ou activer un workflow encore en `MODE = test` en même temps que le Zap équivalent.

**Fiche type par workflow** (à remplir pour chacun au fil de la migration)

> **Rôle** · **Déclencheur** · **Informations reçues** · **Opérations** · **Connexions utilisées** · **Agent IA éventuel** · **Conséquence en cas d'erreur** · **Comment le tester** · **Comment le désactiver**

## 6. Tableau de suivi

Statuts possibles : Non commencé · En cours · Créé · Testé · Prêt pour activation · Actif.

| Workflow n8n | Zap(s) d'origine | Priorité | Statut | Blocage |
|---|---|---|---|---|
| 00 – Gestion des erreurs + journal | — | Socle | Non commencé | A1, A2 |
| P1 – Prospects Facebook → Sheets + email | PUB FB SHEET GMAIL (+ Zap en pause) | 1 | Non commencé | A1, A2, A4, A5 ; champs Province/Code postal |
| P2 – Formulaire site → Axonaut client + devis V2C | AUTO SITE DEVIS AXONAUT V2C, (Nv. design) | 2–4 | Non commencé | A1, A2, **A4 indispensable** (71 étapes) |
| P5 – Ekwateur dossiers + pièces jointes | EKWATEUR | 5 | Non commencé | A1, A2, A4 |
| P6 – Notifications internes | NOTIF 2, 3, 5, 7, 8 | 6 | Non commencé | A1, A2, A4, **A6** |
| P7 – Relances commerciales | MAIL DE RELANCE 1, 2 | 7 | Non commencé | A1, A2, A4 |
| P8 – Partenaires et autres | Zaps 14 à 19, Untitled | 8 | Non commencé | A3, A4 |
| Agent supervision | — | après le socle | Non commencé | 00 terminé |
| Agent partenaires | Routine « EKWATEUR email triage » | — | **Actif (hors n8n)** | — |
