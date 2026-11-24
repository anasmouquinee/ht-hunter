"""Cover letter and email body generator dynamically tailored to industrial engineering opportunities."""

import html
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.config import config
from src.models.offer import JobOffer
from src.utils.logger import logger

FRENCH_MONTHS = [
    "", "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre"
]


def format_french_date(dt: Optional[datetime] = None) -> str:
    """Returns current date formatted in standard French correspondence format (e.g., '24 novembre 2026')."""
    now = dt or datetime.now()
    month_name = FRENCH_MONTHS[now.month] if 1 <= now.month <= 12 else str(now.month)
    return f"{now.day} {month_name} {now.year}"


class CoverLetterGenerator:
    """
    Generates personalized, high-converting application emails and formal cover letters
    (Lettres de Motivation) in both plain text and A4 print-ready HTML for Houda Tazi.
    """

    @staticmethod
    def generate_subject(offer: JobOffer) -> str:
        """Standardized professional email subject line for job/internship applications."""
        clean_title = re.sub(r"^\[.*?\]\s*", "", offer.title).strip()
        role_label = clean_title if clean_title else "Ingénieur(e) Génie Industriel"
        return f"Candidature : {role_label} -- {config.candidate.full_name}"

    @staticmethod
    def _select_highlighted_projects(offer: JobOffer) -> list[tuple[str, str]]:
        """
        Dynamically selects the top 3 most relevant industrial experiences/projects
        based on the offer's domain (Automotive/Lean, Process/OCP, or Supply Chain/CPLEX).
        """
        text = f"{offer.title} {offer.description}".lower()
        projects: list[tuple[str, str]] = []

        is_lean_or_automotive = any(kw in text for kw in ("lean", "5s", "kaizen", "smed", "vsm", "tpm", "automobile", "câblage", "cablage", "production", "méthode", "methode", "chaine", "chaîne"))
        is_chemical_or_heavy = any(kw in text for kw in ("ocp", "chimie", "phosphate", "procédé", "procede", "énergie", "energie", "bilan"))
        is_supply_or_logistics = any(kw in text for kw in ("supply", "logistique", "stock", "approvisionnement", "ordonnancement", "cplex", "arena"))

        if is_chemical_or_heavy:
            projects.append((
                "OCP Group / Pakistan Maroc Phosphore (Jorf Lasfar)",
                "Établissement du bilan matière pour la production de 1800T/j de P2O5 au niveau de l'attaque filtration et détection des goulots d'étranglement."
            ))
            projects.append((
                "LEONI Wiring Systems (Berrechid)",
                "Stage de fin d'études : Amélioration continue de l'efficience de la ligne de production LAD MERGE P2JO PPL (Lean, chrono-analyse, équilibrage des postes)."
            ))
        elif is_lean_or_automotive:
            projects.append((
                "LEONI Wiring Systems (Berrechid)",
                "Stage de fin d'études : Amélioration continue de l'efficience de la ligne de production LAD MERGE P2JO PPL (Lean Manufacturing, chrono-analyse, équilibrage des cadences)."
            ))
            projects.append((
                "SEWS CABIND Maroc (Casablanca - Ain Sebaa)",
                "Amélioration de la productivité de la chaîne de production LAD (Projet Porta Ducato MY21) : Cartographie VSM, chasse aux gaspillages (Muda) et chantiers 5S."
            ))
        else:
            # Supply Chain / OR / Modeling Focus
            projects.append((
                "Optimisation Logistique & Recherche Opérationnelle (CPLEX & Arena)",
                "Résolution du problème du Sac à Dos appliqué au chargement optimal de conteneurs sous IBM ILOG CPLEX et simulation dynamique des flux sous Arena."
            ))
            projects.append((
                "Projet ERP & Système d'Information Achats",
                "Développement d'une application sous Excel VBA pour la gestion des approvisionnements, intégrant la modélisation MCD/MLD d'une base de données relationnelle."
            ))

        # Add third pillar
        if len(projects) < 3:
            projects.append((
                "Plateforme ECOBITE (Logistique Inverse & Valorisation)",
                "Conception d'une chaîne logistique inverse innovante pour la revalorisation de surplus alimentaires, avec analyse multicritère des processus."
            ))

        return projects[:3]

    @classmethod
    def generate_body(cls, offer: JobOffer) -> str:
        """Generates dynamic French plain-text email body tailored to the company and role."""
        company = offer.company if offer.company else "votre entreprise"
        raw_title = offer.title if offer.title else "Ingénieure Génie Industriel"
        clean_title = re.sub(r"^\[.*?\]\s*", "", raw_title).strip()
        cand = config.candidate

        skills_text = ""
        if offer.matched_skills:
            top_skills = ", ".join(offer.matched_skills[:4])
            skills_text = f"notamment autour de domaines tels que {top_skills}, "

        if offer.hr_name:
            last = offer.hr_name.strip().split()[-1]
            greeting = f"Bonjour Monsieur/Madame {last},"
        else:
            greeting = "Madame, Monsieur,"

        projects = cls._select_highlighted_projects(offer)
        projects_str = "\n".join(f"- **{name}** : {desc}" for name, desc in projects)

        body = f"""{greeting}

Je vous adresse ma candidature pour l'opportunité de **{clean_title}** au sein de **{company}**.

Diplômée Ingénieure d'État en **{cand.specialization}** de l'{cand.school} (Promotion 2026, mention Bien), je souhaite mettre ma rigueur, mes compétences d'optimisation et ma vision terrain au service de vos défis industriels.

Mon parcours académique et mes immersions industrielles m'ont permis de développer une solide maîtrise méthodologique {skills_text}illustrée par mes projets et réalisations :
{projects_str}

Rigoureuse, force de proposition et dotée d'une forte culture du résultat (Lean Manufacturing, Maîtrise statistique des procédés, fluidification des flux logistiques), intégrer {company} représente pour moi l'opportunité idéale d'apporter une valeur ajoutée concrète à vos équipes opérationnelles.

Vous trouverez ci-joint mon dossier de candidature détaillé comprenant mon Curriculum Vitae. Je reste à votre entière disposition pour tout échange ou entretien.

En vous remerciant pour l'attention portée à ma démarche, je vous prie d'agréer, {greeting}, l'expression de mes salutations distinguées.


Cordialement,

{cand.full_name}
Ingénieure d'État en Génie Industriel ({cand.school})
Téléphone : {cand.phone} | Email : {cand.personal_email}
LinkedIn : {cand.linkedin_url}
"""
        return body

    @classmethod
    def generate_html_letter(cls, offer: JobOffer) -> str:
        """Generates an elegant, print-ready A4 HTML cover letter for Houda Tazi."""
        company = html.escape(offer.company if offer.company else "L'Entreprise")
        location = html.escape(offer.location if offer.location else "Casablanca, Maroc")
        clean_title = html.escape(re.sub(r"^\[.*?\]\s*", "", offer.title if offer.title else "Ingénieure Génie Industriel").strip())
        cand = config.candidate
        current_date_str = format_french_date()

        projects = cls._select_highlighted_projects(offer)
        projects_html = "".join(
            f"<li><strong>{html.escape(name)} :</strong> {html.escape(desc)}</li>"
            for name, desc in projects
        )

        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Lettre de Motivation - {clean_title} - {cand.full_name}</title>
  <style>
    @page {{ size: A4; margin: 20mm; }}
    body {{
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      color: #1a1a1a;
      line-height: 1.6;
      font-size: 11pt;
      margin: 0;
      padding: 0;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 25px;
      border-bottom: 2px solid #0284c7;
      padding-bottom: 15px;
    }}
    .candidate-info h1 {{
      font-size: 16pt;
      margin: 0 0 5px 0;
      color: #0f172a;
    }}
    .candidate-info p {{
      margin: 2px 0;
      color: #475569;
      font-size: 9.5pt;
    }}
    .recipient-info {{
      text-align: right;
      color: #334155;
    }}
    .recipient-info strong {{
      font-size: 12pt;
      color: #0f172a;
    }}
    .subject-line {{
      font-weight: bold;
      margin: 20px 0;
      padding: 8px 12px;
      background: #f1f5f9;
      border-left: 4px solid #0284c7;
      font-size: 11pt;
    }}
    .content p {{
      margin-bottom: 14px;
      text-align: justify;
    }}
    .projects-list {{
      margin: 12px 0 16px 20px;
      padding: 0;
    }}
    .projects-list li {{
      margin-bottom: 8px;
    }}
    .signature {{
      margin-top: 30px;
      float: right;
      text-align: right;
    }}
    .signature-name {{
      font-weight: bold;
      color: #0f172a;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div class="candidate-info">
      <h1>{cand.full_name}</h1>
      <p>Ingénieure d'État en Génie Industriel</p>
      <p>{cand.school} (Promotion 2026)</p>
      <p>Tél : {cand.phone} | Email : {cand.personal_email}</p>
      <p>LinkedIn : {cand.linkedin_url}</p>
    </div>
    <div class="recipient-info">
      <p>À l'attention de la Direction des Ressources Humaines</p>
      <p><strong>{company}</strong></p>
      <p>{location}</p>
      <p>Le {current_date_str}</p>
    </div>
  </div>

  <div class="subject-line">
    Objet : Candidature au poste de {clean_title}
  </div>

  <div class="content">
    <p>Madame, Monsieur,</p>

    <p>
      Récemment diplômée Ingénieure d'État en <strong>{cand.specialization}</strong> de l'<strong>{cand.school}</strong> (mention Bien),
      je me permets de vous adresser ma candidature pour le poste de <strong>{clean_title}</strong> au sein de <strong>{company}</strong>.
    </p>

    <p>
      Mon parcours d'ingénieur m'a permis d'acquérir une expertise pointue dans l'amélioration continue, l'optimisation des flux de production
      et la gestion de la chaîne logistique, enrichie par plusieurs expériences opérationnelles :
    </p>

    <ul class="projects-list">
      {projects_html}
    </ul>

    <p>
      Reconnaissant l'excellence opérationnelle et le positionnement stratégique de votre organisation, je serais honorée de mettre mes compétences d'analyse,
      ma rigueur de modélisation et mon dynamisme de terrain au service de vos lignes de production et de vos processus logistiques.
    </p>

    <p>
      Je reste à votre entière disposition pour convenir d'un entretien afin de vous exposer plus en détail mes motivations et mon adéquation avec vos besoins.
    </p>

    <p>
      Dans cette attente, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations les plus distinguées.
    </p>
  </div>

  <div class="signature">
    <div class="signature-name">{cand.full_name}</div>
    <div style="font-size: 9pt; color: #64748b;">Ingénieure d'État en Génie Industriel</div>
  </div>

  <div class="no-print" style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #e2e8f0; text-align: center;">
    <button onclick="window.print()" style="padding: 8px 16px; background: #0284c7; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">Imprimer / Enregistrer en PDF</button>
  </div>
  <script>
    function copyLetterText() {{
      const text = document.querySelector('.content').innerText;
      navigator.clipboard.writeText(text);
    }}
  </script>
</body>
</html>"""

    # Backwards-compatible aliases
    generate_html_body = generate_html_letter
    generate_html = generate_html_letter

    @classmethod
    def generate_formal_letter_html(cls, offer: JobOffer) -> str:
        """Alias for generate_html_letter."""
        return cls.generate_html_letter(offer)

    @classmethod
    def generate_formal_letter_text(cls, offer: JobOffer) -> str:
        """Generates formal French plain-text cover letter."""
        company = offer.company if offer.company else "Madame, Monsieur"
        clean_title = re.sub(r"^\[.*?\]\s*", "", offer.title if offer.title else "Ingénieure Génie Industriel").strip()
        cand = config.candidate
        current_date = format_french_date()
        projects = cls._select_highlighted_projects(offer)
        projects_txt = "\n".join(f"  * {name} : {desc}" for name, desc in projects)

        return f"""{cand.full_name}
Ingénieure d'État en Génie Industriel
{cand.school} (Promotion 2026, mention Bien)
Tél : {cand.phone} | Email : {cand.personal_email}
LinkedIn : {cand.linkedin_url}

À l'attention de la Direction des Ressources Humaines
{company}
Fait le {current_date}

OBJET : Candidature au poste de {clean_title}

Madame, Monsieur,

Diplômée Ingénieure d'État en {cand.specialization} de l'{cand.school}, je vous soumets ma candidature pour le poste de {clean_title} au sein de {company}.

Mon parcours m'a permis d'acquérir une solide rigueur d'optimisation opérationnelle et d'amélioration continue, éprouvée au travers de réalisations concrètes :
{projects_txt}

Reconnaissant l'exigence opérationnelle de votre organisation, je serais honorée de mettre mon dynamisme et mes compétences au service de vos lignes de production et de vos flux logistiques.

Je reste à votre entière disposition pour tout échange ou entretien approfondi.

Dans cette attente, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{cand.full_name}
Ingénieure d'État en Génie Industriel
"""

    @classmethod
    def save_letter_for_offer(
        cls,
        offer: JobOffer,
        output_dir: Optional[Path] = None,
        custom_slug: Optional[str] = None
    ) -> dict[str, Path]:
        """Generates and saves both .html and .txt versions of the formal cover letter."""
        out_dir = output_dir or (config.BASE_DIR / "letters")
        os.makedirs(out_dir, exist_ok=True)

        if custom_slug:
            slug = custom_slug
        else:
            safe_co = re.sub(r'[^a-zA-Z0-9]+', '_', offer.company or 'Entreprise').strip('_')
            safe_ti = re.sub(r'[^a-zA-Z0-9]+', '_', offer.title or 'Industriel').strip('_')
            offer_id = getattr(offer, 'id', '000000') or '000000'
            slug = f"Lettre_Motivation_{safe_co}_{safe_ti[:32]}_{offer_id[:6]}"

        html_path = out_dir / f"{slug}.html"
        txt_path = out_dir / f"{slug}.txt"

        html_content = cls.generate_formal_letter_html(offer)
        txt_content = cls.generate_formal_letter_text(offer)

        html_path.write_text(html_content, encoding="utf-8")
        txt_path.write_text(txt_content, encoding="utf-8")

        logger.info("Saved cover letter files for %s: %s, %s", offer.company, html_path.name, txt_path.name)
        return {"html": html_path, "txt": txt_path}
