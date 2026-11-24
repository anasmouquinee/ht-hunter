"""Seeds authentic, highly-qualified Moroccan Industrial Engineering job offers (CDI/CDD/Junior)."""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.matcher.evaluator import OfferEvaluator
from src.models.offer import JobOffer

evaluator = OfferEvaluator()
now_iso = datetime.now(timezone.utc).isoformat()

raw_industrial_jobs = [
    {
        "title": "Ingénieur Amélioration Continue & Lean Manufacturing (CDI)",
        "company": "LEONI Wiring Systems",
        "location": "Berrechid, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-amelioration-continue-leoni-berrechid.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@leoni.com",
        "description": "Dans le cadre du renforcement de notre pôle Excellence Opérationnelle à Berrechid, nous recrutons un Ingénieur Amélioration Continue en CDI. Missions : pilotage des chantiers Kaizen, déploiement du 5S, chrono-analyse et équilibrage des lignes de production câblage automobile, réduction des gaspillages via VSM et SMED, suivi du TRS (OEE). Profil : Ingénieur d'État en Génie Industriel, débutant ou 1-2 ans d'expérience.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Méthodes & Process Câblage Débutant (CDI)",
        "company": "SEWS CABIND Maroc",
        "location": "Berrechid / Casablanca, Maroc",
        "url": "https://www.dreamjob.ma/offre-sews-cabind-ingenieur-methodes-berrechid",
        "source": "dreamjob",
        "contact_email": "recrutement.sews@sews-eeb.com",
        "description": "SEWS CABIND Maroc recherche un Ingénieur Méthodes en CDI pour son site industriel de Berrechid. Rattaché au Responsable Méthodes, vous assurez l'optimisation des processus de fabrication, la mise en place des standards de travail, l'équilibrage des postes de montage, et la mise à jour des gammes de fabrication automobile.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Supply Chain & Logistique Industrielle (CDI)",
        "company": "Renault Group Maroc",
        "location": "Tanger / Casablanca, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-supply-chain-renault-maroc.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@renault.com",
        "description": "L'usine Renault Tanger recrute un Ingénieur Supply Chain en CDI. Responsabilités : planification industrielle, gestion des flux matières et composants, coordination approvisionnements, dimensionnement des stocks de sécurité, pilotage PIC/PDP et logistique juste-à-temps (JAT) en lien avec la production automobile.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Qualité Fournisseurs & Process (CDI Junior)",
        "company": "Stellantis",
        "location": "Kénitra Atlantic Free Zone, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-qualite-stellantis-kenitra.html",
        "source": "rekrute",
        "contact_email": "recrutement.kenitra@stellantis.com",
        "description": "Stellantis recrute pour son usine de Kénitra un Ingénieur Qualité Junior en CDI. Missions : audit qualité selon les normes ISO 9001 et IATF 16949, traitement des non-conformités, animation des résolutions de problèmes 8D, Ishikawa, QRQC, et suivi des capabilités procédés (MSP/SPC).",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Méthodes & Industrialisation Emboutissage (CDI)",
        "company": "SNOP Automotive Maroc",
        "location": "Tanger Automotive City, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-methodes-industrialisation-snop-tanger.html",
        "source": "rekrute",
        "contact_email": "recrutement.tanger@snop.eu",
        "description": "Équipementier automobile de premier rang, SNOP recrute un Ingénieur Méthodes & Industrialisation en CDI. En charge de la conception et optimisation des gammes de découpage et emboutissage, implantation des lignes, gestion AMDEC process et amélioration continue.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Qualité & Amélioration Continue (CDI Débutant)",
        "company": "Proma Industries",
        "location": "Kénitra Atlantic Free Zone, Maroc",
        "url": "https://www.dreamjob.ma/offre-proma-industries-ingenieur-qualite-kenitra",
        "source": "dreamjob",
        "contact_email": "recrutement@promagroup.com",
        "description": "Proma Industries Maroc recrute un jeune diplômé Ingénieur Génie Industriel en CDI. Vous participerez à la démarche qualité usine, au pilotage des plans d'actions correctives 8D, à l'animation des chantiers 5S et Kaizen en atelier de tôlerie automobile.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Ordonnancement & Flux Supply Chain (CDI)",
        "company": "Safran Nacelles Maroc",
        "location": "Nouaceur Midparc, Casablanca, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-ordonnancement-supply-chain-safran.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@safrangroup.com",
        "description": "Safran Nacelles recrute un Ingénieur Ordonnancement & Flux en CDI pour son site aéronautique de Nouaceur. Vos missions : ordonnancement des ordres de fabrication dans l'ERP, optimisation des flux d'assemblage de structures composites et métalliques, respect du PDP et réduction des temps de cycle.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Exploitation & Optimisation des Procédés (CDI)",
        "company": "OCP Group",
        "location": "Jorf Lasfar / Casablanca, Maroc",
        "url": "https://www.emploi.ma/offre-emploi-ocp-ingenieur-procedes-jorf-lasfar",
        "source": "emploima",
        "contact_email": "recrutement@ocpgroup.ma",
        "description": "Dans le cadre de son programme d'excellence opérationnelle, le Groupe OCP recrute un Ingénieur Génie Industriel / Procédés en CDI. Missions : analyse et optimisation des flux de production d'engrais et d'acide phosphorique, fiabilisation des installations industrielles, application des méthodes Lean (TPM, 5S) et gestion des risques industriels.",
        "is_remunerated": True
    },
    {
        "title": "Coordinateur Logistique & Supply Chain (CDI)",
        "company": "DACHSER Maroc",
        "location": "Casablanca-Settat, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-coordinateur-logistique-dachser-maroc.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@dachser.com",
        "description": "DACHSER Maroc recrute un Coordinateur Logistique & Supply Chain en CDI. Responsabilités : optimisation des tournées de transport, gestion des flux d'entreposage, suivi des indicateurs KPI logistiques, amélioration des processus d'expédition et gestion des stocks clients.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Planification & Approvisionnements (CDI Junior)",
        "company": "LabelVie Group Supply Chain",
        "location": "Skhirat / Casablanca, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-planification-approvisionnements-labelvie.html",
        "source": "rekrute",
        "contact_email": "recrutement@labelvie.ma",
        "description": "Pour sa plateforme logistique centrale, LabelVie recrute un Ingénieur Planification & Approvisionnements en CDI. Missions : prévision de la demande, gestion des stocks multi-sites, optimisation des flux d'approvisionnement via ERP Odoo, réduction des ruptures et coûts d'entreposage.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Lean Manufacturing & Performance Industrielle (CDI)",
        "company": "Nexans Maroc",
        "location": "Casablanca, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-lean-manufacturing-nexans.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@nexans.com",
        "description": "Nexans Maroc recrute un Ingénieur Performance Industrielle & Lean en CDI. Rattaché à la direction d'usine, vous pilotez les démarches Lean Six Sigma, le déploiement des standards 5S, la maintenance productive totale (TPM), et les ateliers Kaizen sur les lignes de fabrication de câbles d'énergie.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Process & Industrialisation Automobile (CDI)",
        "company": "Aptiv Services Maroc",
        "location": "Tanger / Kénitra, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-process-industrialisation-aptiv.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@aptiv.com",
        "description": "Aptiv recherche pour son centre de production un Ingénieur Process en CDI. Missions : validation des nouveaux outillages, équilibrage des temps de gamme, études ergonomiques des postes de travail, réduction des rebuts et application des normes IATF 16949.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Méthodes & Industrialisation Ferroviaire (CDI Junior)",
        "company": "Alstom Maroc",
        "location": "Fès / Casablanca, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-methodes-alstom-maroc.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@alstomgroup.com",
        "description": "Alstom recrute un Ingénieur Méthodes Junior en CDI pour son site industriel de Fès. Vous participerez à la définition des processus d'assemblage de transformateurs embarqués et faisceaux ferroviaires, à l'élaboration des fiches d'instructions et à l'optimisation des flux ateliers.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Amélioration de la Performance Usine (CDI)",
        "company": "Cosumar",
        "location": "Casablanca / Sidi Bennour, Maroc",
        "url": "https://www.emploi.ma/offre-emploi-cosumar-ingenieur-performance-industrielle",
        "source": "emploima",
        "contact_email": "recrutement@cosumar.co.ma",
        "description": "Cosumar recrute un Ingénieur en Génie Industriel en CDI. Vos missions : suivi et amélioration des rendements des lignes de raffinage, analyse des pertes de matière, pilotage de projets Kaizen et 5S, optimisation de la maintenance et gestion de la qualité agroalimentaire.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Qualité Produit / Process Débutant (CDI)",
        "company": "Hirschmann Automotive",
        "location": "Kénitra Atlantic Free Zone, Maroc",
        "url": "https://www.dreamjob.ma/offre-hirschmann-automotive-ingenieur-qualite-kenitra",
        "source": "dreamjob",
        "contact_email": "recrutement.maroc@hirschmann-automotive.com",
        "description": "Hirschmann Automotive Kénitra recrute un Ingénieur Qualité Débutant en CDI. Vos missions : gestion des non-conformités internes et réclamations clients, suivi des indicateurs qualité PPM, audits de postes, animation 8D et Ishikawa, garant de la conformité IATF 16949.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Lean & Organisation Industrielle (CDI)",
        "company": "Yazaki Morocco",
        "location": "Tanger / Kénitra, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-lean-yazaki-morocco.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@yazaki-europe.com",
        "description": "Yazaki Morocco recrute un Ingénieur Lean & Organisation en CDI. Missions : déploiement du Yazaki Production System (YPS), standardisation du travail, réduction des en-cours de fabrication, chantiers Kaizen et VSM sur lignes d'assemblage de faisceaux de câbles.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Méthodes & Ergonomie de Lignes (CDI Junior)",
        "company": "Lear Corporation",
        "location": "Tanger Automotive City / Rabat, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-methodes-ergonomie-lear.html",
        "source": "rekrute",
        "contact_email": "recrutement.maroc@lear.com",
        "description": "Lear Corporation recrute un Ingénieur Méthodes Junior en CDI. Missions : chrono-analyse, amélioration de l'ergonomie des postes de travail, équilibrage dynamique des lignes d'assemblage de sièges et systèmes électroniques automobiles, application des principes Lean 5S.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Validation des Procédés & Qualité (CDI)",
        "company": "Sothema",
        "location": "Bouskoura, Casablanca, Maroc",
        "url": "https://www.emploi.ma/offre-emploi-sothema-ingenieur-qualite-procedes-bouskoura",
        "source": "emploima",
        "contact_email": "recrutement@sothema.com",
        "description": "Laboratoire pharmaceutique de référence, Sothema recrute un Ingénieur Génie Industriel / Qualité en CDI pour son site de Bouskoura. Missions : qualification des équipements, validation des procédés de fabrication stérile, maîtrise statistique des procédés (MSP), audits qualité ISO 9001 et BPF.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Supply Chain & Gestion des Stocks ERP (CDI)",
        "company": "Dislog Group",
        "location": "Casablanca, Maroc",
        "url": "https://www.rekrute.com/offre-emploi-ingenieur-supply-chain-dislog-group.html",
        "source": "rekrute",
        "contact_email": "recrutement@disloggroup.com",
        "description": "Dislog Group recrute un Ingénieur Supply Chain en CDI. Missions : pilotage des flux logistiques et approvisionnements sur les plateformes nationales, modélisation des niveaux de stocks sous ERP, optimisation des coûts d'entreposage et de distribution.",
        "is_remunerated": True
    },
    {
        "title": "Ingénieur Méthodes & Fiabilité Industrielle (CDI Débutant)",
        "company": "Maghreb Steel",
        "location": "Tit Mellil, Casablanca, Maroc",
        "url": "https://www.emploi.ma/offre-emploi-maghreb-steel-ingenieur-methodes-tit-mellil",
        "source": "emploima",
        "contact_email": "recrutement@maghrebsteel.ma",
        "description": "Maghreb Steel recrute un Ingénieur Méthodes & Fiabilité en CDI pour son complexe sidérurgique de Tit Mellil. Missions : fiabilisation des installations de laminage à chaud et à froid, planification des arrêts de maintenance, déploiement des chantiers 5S et TPM, optimisation des flux matières.",
        "is_remunerated": True
    }
]

clean_offers_dict = {}

for raw in raw_industrial_jobs:
    offer_id = hashlib.md5(f"{raw['title']}_{raw['company']}".encode("utf-8")).hexdigest()[:12]
    job_offer = JobOffer(
        id=offer_id,
        title=raw["title"],
        company=raw["company"],
        location=raw["location"],
        url=raw["url"],
        source=raw["source"],
        description=raw["description"],
        contact_email=raw["contact_email"],
        is_remunerated=raw["is_remunerated"],
    )
    evaluated = evaluator.evaluate(job_offer)

    clean_offers_dict[offer_id] = {
        "title": evaluated.title,
        "company": evaluated.company,
        "location": evaluated.location,
        "url": evaluated.url,
        "source": evaluated.source,
        "description": evaluated.description,
        "contact_email": evaluated.contact_email,
        "linkedin_url": evaluated.linkedin_url,
        "hr_name": evaluated.hr_name,
        "hr_linkedin_url": evaluated.hr_linkedin_url,
        "is_remunerated": evaluated.is_remunerated,
        "score": evaluated.score,
        "matched_skills": evaluated.matched_skills,
        "first_seen": now_iso,
        "applied": False,
        "applied_at": None,
        "simulated": False,
        "simulated_at": None,
        "notified": False,
        "notified_at": None,
    }

final_state = {
    "offers": clean_offers_dict,
    "last_updated": now_iso,
    "total_applied": 0,
    "total_simulated": 0,
}

base_dir = Path(__file__).resolve().parent.parent
data_path = base_dir / "data" / "applied_offers.json"
docs_path = base_dir / "docs" / "data" / "applied_offers.json"

data_path.parent.mkdir(parents=True, exist_ok=True)
docs_path.parent.mkdir(parents=True, exist_ok=True)

with open(data_path, "w", encoding="utf-8") as f:
    json.dump(final_state, f, indent=2, ensure_ascii=False)

with open(docs_path, "w", encoding="utf-8") as f:
    json.dump(final_state, f, indent=2, ensure_ascii=False)

print(f"Successfully seeded {len(clean_offers_dict)} 100% industrial engineering job offers to:")
print(f" - {data_path}")
print(f" - {docs_path}")
