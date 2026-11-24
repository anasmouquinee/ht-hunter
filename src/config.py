"""Configuration module for Industrial Hunter & Career Automation Agent (Houda Tazi)."""

import os
from pathlib import Path
from pydantic import BaseModel, Field
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


class CandidateProfile(BaseModel):
    """Pre-configured candidate profile for Houda Tazi (Ingénieure d'État en Génie Industriel)."""
    full_name: str = "Houda Tazi"
    email: str = "tazihouda124@gmail.com"  # Automated dispatch sender
    personal_email: str = "tazihouda1108@gmail.com"
    digest_recipient: str = "tazihouda1108@gmail.com"  # Personal contact / notification email
    phone: str = "+212 695-957464"
    location: str = "Berrechid / Casablanca-Settat / El Jadida, Maroc"
    linkedin_url: str = "https://www.linkedin.com/in/houda-tazi-625b11389"
    github_url: str = ""
    portfolio_url: str = ""  # Will point to GitHub Pages once published
    school: str = "École Nationale des Sciences Appliquées (ENSA El Jadida)"
    education_level: str = "Diplôme d'Ingénieur d'État (Promotion 2026, mention Bien)"
    specialization: str = "Génie Industriel (Production, Supply Chain, Qualité, Lean & Amélioration Continue)"
    target_contracts: str = "CDI, CDD, Emploi Ingénieur Débutant / Junior (Génie Industriel)"
    cv_path: Path = BASE_DIR / "dossier_candidature_houda_tazi.pdf"

    # Core technical keywords for scoring -- Industrial Engineering, Lean, Supply Chain, Quality
    core_skills: list[str] = [
        # Production & Lean Manufacturing
        "Génie Industriel", "Ingénierie Industrielle", "Production", "Gestion de la Production",
        "Amélioration Continue", "Lean Manufacturing", "Lean Six Sigma", "Six Sigma",
        "Kaizen", "5S", "VSM", "Value Stream Mapping", "DMAIC", "SMED", "TPM",
        "Chrono-analyse", "Équilibrage de Postes", "Chantier Kaizen", "Ligne de Production",
        "TRS", "OEE", "Poka-Yoke", "Kanban", "Juste-à-Temps", "JAT",

        # Supply Chain & Logistics
        "Supply Chain", "Supply Chain Management", "Logistique", "Logistique Industrielle",
        "Logistique Inverse", "Gestion des Stocks", "Approvisionnement", "Ordonnancement",
        "Planification", "PIC", "PDP", "Plan Industriel et Commercial", "Optimisation des Flux",
        "Entreposage", "Transport & Distribution", "ERP", "Odoo", "Gestion des Achats",

        # Quality & Process Engineering
        "Qualité", "Assurance Qualité", "Contrôle Qualité", "Management de la Qualité",
        "MSP", "SPC", "Maîtrise Statistique des Procédés", "MiniTab", "Capabilité",
        "ISO 9001", "IATF 16949", "Résolution de Problèmes", "8D", "Ishikawa", "5 Pourquoi",
        "QRQC", "Audit Qualité", "AMDEC", "FMEA",

        # Modeling, Operations Research & Tools
        "Recherche Opérationnelle", "Optimisation", "IBM ILOG CPLEX", "CPLEX",
        "Simulation de Flux", "Arena", "CATIA", "Simulink", "Dessin Industriel",
        "TIA Portal", "Automatisme", "Systèmes Industriels", "Excel VBA", "VBA",
        "Python", "SQL", "Bases de Données", "Gestion des Risques", "Gestion de Projet"
    ]


class AgentConfig(BaseModel):
    """Global configuration for scraping, email dispatch, and alerting."""
    candidate: CandidateProfile = Field(default_factory=CandidateProfile)

    # Search parameters -- covering Industrial Engineering, Production, Supply Chain & Quality
    target_cities: list[str] = [
        "Casablanca", "Casablanca-Settat", "Berrechid", "Nouaceur", "Bouskoura",
        "Settat", "El Jadida", "Jorf Lasfar", "Mohammedia", "Rabat", "Kénitra",
        "Tanger", "Tanger Automotive City", "Tout le Maroc", "Remote", "Hybride"
    ]

    target_roles: list[str] = [
        "Ingénieur Génie Industriel", "Ingénieur Méthodes", "Ingénieur Production",
        "Ingénieur Amélioration Continue", "Ingénieur Lean Manufacturing",
        "Ingénieur Supply Chain", "Ingénieur Logistique", "Ingénieur Qualité",
        "Ingénieur Planification & Ordonnancement", "Ingénieur Process & Industrialisation",
        "Consultant Génie Industriel / Supply Chain", "Ingénieur Débutant Génie Industriel",
        "Ingénieur Junior Production / Qualité / Logistique"
    ]

    search_keywords: list[str] = [
        "genie industriel",
        "ingenieur industriel",
        "ingenieur methodes",
        "ingenieur production",
        "ingenieur supply chain",
        "ingenieur logistique",
        "ingenieur qualite",
        "amelioration continue",
        "lean manufacturing",
        "cdi genie industriel",
        "recrutement ingenieur industriel",
        "gestion des stocks",
        "ordonnancement",
        "planification industrielle",
        "lean six sigma",
        "responsable production junior",
    ]

    remuneration_keywords: list[str] = [
        "rémunéré", "remunere", "gratification", "indemnité",
        "indemnite", "bourse", "payé", "paye", "stipend", "salaire"
    ]

    # Email & Safety Controls (Default to Dry-Run for safety)
    dry_run: bool = Field(default_factory=lambda: os.getenv("DRY_RUN", "true").lower() in ("true", "1", "yes"))
    gmail_user: str = Field(default_factory=lambda: os.getenv("GMAIL_USER", "tazihouda124@gmail.com"))
    gmail_app_password: str = Field(default_factory=lambda: os.getenv("GMAIL_APP_PASSWORD", ""))
    resend_api_key: str = Field(default_factory=lambda: os.getenv("RESEND_API_KEY", ""))
    resend_from_email: str = Field(default_factory=lambda: os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev"))

    # Anonymous Offer Digest Feature (Surprise delivery to Houda's personal email)
    digest_enabled: bool = Field(default_factory=lambda: os.getenv("DIGEST_ENABLED", "true").lower() in ("true", "1", "yes"))
    digest_recipient: str = Field(default_factory=lambda: os.getenv("DIGEST_RECIPIENT", "tazihouda1108@gmail.com"))
    digest_sender_name: str = Field(default_factory=lambda: os.getenv("DIGEST_SENDER_NAME", "Veille Opportunités Emploi · Génie Industriel"))

    # LinkedIn & Platform Accounts
    linkedin_li_at: str = Field(default_factory=lambda: os.getenv("LINKEDIN_LI_AT", ""))
    auto_easy_apply: bool = Field(
        default_factory=lambda: os.getenv(
            "AUTO_EASY_APPLY",
            "true" if os.getenv("LINKEDIN_LI_AT") else "false",
        ).lower() in ("true", "1", "yes")
    )

    rekrute_email: str = Field(default_factory=lambda: os.getenv("REKRUTE_EMAIL", os.getenv("GMAIL_USER", "tazihouda124@gmail.com")))
    rekrute_password: str = Field(default_factory=lambda: os.getenv("REKRUTE_PASSWORD", ""))
    auto_platform_apply: bool = Field(
        default_factory=lambda: os.getenv(
            "AUTO_PLATFORM_APPLY",
            "true" if (os.getenv("LINKEDIN_LI_AT") or os.getenv("REKRUTE_PASSWORD")) else "false",
        ).lower() in ("true", "1", "yes")
    )

    max_emails_per_run: int = Field(default_factory=lambda: int(os.getenv("MAX_EMAILS_PER_RUN", "20")))
    max_offer_age_days: int = Field(default_factory=lambda: int(os.getenv("MAX_OFFER_AGE_DAYS", "14")))

    # Notification Webhooks
    telegram_bot_token: str = Field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    telegram_chat_id: str = Field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))
    discord_webhook_url: str = Field(default_factory=lambda: os.getenv("DISCORD_WEBHOOK_URL", ""))

    # AI / LLM Evaluation (Optional)
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

    # Data Persistence & Outputs
    base_dir: Path = BASE_DIR
    letters_dir: Path = BASE_DIR / "letters"
    data_dir: Path = BASE_DIR / "data"
    state_file: Path = BASE_DIR / "data" / "applied_offers.json"

    @property
    def BASE_DIR(self) -> Path:
        return self.base_dir


# Singleton instance
config = AgentConfig()
