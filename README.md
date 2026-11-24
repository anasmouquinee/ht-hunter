# Industrial Hunter · Plateforme Autonome de Veille & Portfolio Génie Industriel

<div align="center">

![Industrial Hunter](https://img.shields.io/badge/G%C3%A9nie%20Industriel-ENSA%20El%20Jadida-0284c7?style=for-the-badge)
![Status](https://img.shields.io/badge/Pipeline-Op%C3%A9rationnel%2024%2F7-10b981?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=for-the-badge&logo=python&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Showcase-818cf8?style=for-the-badge&logo=github)

**Plateforme intelligente de veille d'opportunités industrielles et vitrine d'ingénierie pour Houda Tazi.**  
*Diplômée Ingénieure d'État en Génie Industriel (ENSA El Jadida, 2026 — Mention Bien)*

[🌐 Découvrir la Plateforme en Ligne](https://anasmouquinee.github.io/ht-hunter/) · [📄 Dossier de Candidature (PDF)](docs/dossier_candidature_houda_tazi.pdf)

</div>

---

## 🎯 Objectifs du Projet

**Industrial Hunter** est un agent autonome et une application web unifiée conçus pour capturer, qualifier et exploiter en temps réel l'ensemble des offres d'emploi et de stages en **Génie Industriel, Production, Lean Manufacturing et Supply Chain** au Maroc.

### Cibles Contractuelles
- **CDI & CDD :** Postes débutants / juniors en Amélioration Continue, Méthodes, Qualité, Planification et Supply Chain.
- **Stages Pré-embauche & Insertion :** Pôles industriels automobiles, aéronautiques et chimie lourde (Tanger Med, Atlantic Free Zone Kénitra, Nouaceur, Jorf Lasfar, Casablanca).

---

## 🏗️ Architecture Technique

```
┌────────────────────────────────────────────────────────┐
│               1. COLLECTE MULTI-SOURCES                │
│ DreamJob · LinkedIn · Joblia · Talent · ReKrute · MA   │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│          2. AUDIT & QUALIFICATION SÉMANTIQUE            │
│  - Filtrage des homonymes et faux-positifs linguistiques│
│  - Exclusion des postes de direction (> 5 ans d'exp)   │
│  - Validation du périmètre Génie Industriel            │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│          3. SCORING MÉTIER & PONDÉRATION               │
│  - Lean Manufacturing & 5S (Kaizen, SMED, VSM, TPM)    │
│  - Supply Chain & ERP (Odoo, PIC, PDP, Stocks)         │
│  - Recherche Opérationnelle (IBM CPLEX, Arena)         │
│  - Normes Industrielles (ISO 9001 / QHSE)              │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│          4. NOTIFICATION ANONYME & CANDIDATURE         │
│  - Digest exécutif surprise vers la boîte personnelle  │
│  - Lettres de motivation contextualisées (LEONI/SEWS)   │
│  - Console Web interactive sur GitHub Pages (/docs)    │
└────────────────────────────────────────────────────────┘
```

---

## 💼 Piliers du Profil Candidat (Houda Tazi)

| Pôle d'Expertise | Réalisations & Expériences Clés | Outils & Méthodes |
| :--- | :--- | :--- |
| **Excellence Opérationnelle** | **LEONI Wiring Systems (Stage PFE)** : Réduction des temps de changement de série (SMED), réimplantation ergonomique de postes et standardisation 5S sur lignes de câblage automobile. | Lean 5S, Kaizen, SMED, VSM, TPM, DMAIC |
| **Méthodes & Lignes** | **SEWS CABIND Maroc (Stage Technique)** : Étude chronométrique, élimination des goulots d'étranglement et équilibrage des cadences de production. | Chronométrage, Takt Time, Équilibrage |
| **Procédés & Maintenance** | **OCP Group - PMP Jorf Lasfar (Stage d'Initiation)** : Immersion en production continue d'engrais et suivi de maintenance préventive TPM. | Maintenance TPM, Procédés Continus, Bilan Matière |
| **Recherche Opérationnelle** | **ENSA Lab (Projets R&D)** : Résolution de problèmes d'optimisation combinatoire (sac à dos, tournées de véhicules) et simulation stochastique. | IBM ILOG CPLEX, Arena Rockwell, Python, Excel VBA |
| **Supply Chain & Qualité** | Modélisation des flux d'approvisionnement et conformité aux systèmes de management de la qualité. | Odoo ERP, MRP, PIC/PDP, ISO 9001, QHSE |

---

## 🖥️ Vitrine Web Interactive (`/docs`)

La plateforme est construite en **Vanilla CSS / ES6 Modules** respectant les critères stricts de craft numérique :
1. **Accueil Storyboard :** Défilement interactif synchronisé avec le HUD de monitoring en 4 étapes de collecte et de qualification.
2. **Mission Control (Dashboard) :** Table filtrable en temps réel des 370+ offres archivées, indicateurs KPI avec sparklines et simulateur de scoring en direct.
3. **Portfolio Exécutif :** Fiches projets détaillées, certifications académiques et terminal CLI interactif (`bio`, `skills`, `projects`, `leoni`, `sews`, `ocp`, `cplex`).

---

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Git

### Installation Locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/anasmouquinee/ht-hunter.git
cd ht-hunter

# 2. Créer l'environnement virtuel et installer les dépendances
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Lancer la suite de tests unitaires
pytest tests/ -v

# 4. Exécuter l'agent en mode simulation (Dry-Run)
python run_agent.py --dry-run --send-digest
```

### Visualiser l'Interface Web Localement

Ouvrez simplement le fichier `docs/index.html` dans votre navigateur ou lancez un serveur local léger :

```bash
cd docs
python -m http.server 8000
# Rendez-vous sur http://localhost:8000
```

---

## 🔒 Confidentialité & Effet Surprise

Le module `AnonymousDigestNotifier` compile automatiquement les opportunités qualifiées sous forme de bulletin exécutif professionnel expédié depuis l'adresse d'automatisation (`tazihouda124@gmail.com`) vers l'adresse personnelle (`tazihouda1108@gmail.com`) avec une mise en page neutre, sans mention d'intermédiaire pour garantir une surprise totale.

---

## 📜 Licence

Ce projet est sous licence MIT. Développé pour valoriser l'excellence en Génie Industriel.
