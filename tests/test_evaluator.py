"""Unit tests for OfferEvaluator tailored for Houda Tazi (Génie Industriel)."""

from src.models.offer import JobOffer
from src.matcher.evaluator import OfferEvaluator


def test_evaluator_industrial_and_remunerated():
    evaluator = OfferEvaluator()
    offer = JobOffer(
        title="Ingénieur Amélioration Continue & Lean Manufacturing",
        company="LEONI Wiring Systems",
        location="Berrechid, Maroc",
        url="https://example.com/leoni-lean",
        description="Poste pour ingénieur en organisation industrielle, chantiers 5S, SMED, VSM et Kaizen. Salaire motivant.",
        source="rekrute"
    )

    evaluated = evaluator.evaluate(offer)
    assert evaluator.is_industrial_offer(evaluated) is True
    assert evaluator.is_contract_match(evaluated) is True
    assert evaluated.is_remunerated is True
    assert any("Lean" in s or "5S" in s or "SMED" in s for s in evaluated.matched_skills)
    assert evaluated.score >= 75


def test_evaluator_disqualify_senior_over_5_years():
    evaluator = OfferEvaluator()
    offer = JobOffer(
        title="Directeur d'Usine / Senior Plant Manager (10 ans d'expérience)",
        company="HeavyIndustry Maroc",
        location="Casablanca",
        url="https://example.com/senior-manager",
        description="Poste de direction générale d'usine, minimum 10 ans d'expérience exigée.",
        source="emploima"
    )

    assert evaluator.is_contract_match(offer) is False
    evaluated = evaluator.evaluate(offer)
    assert evaluated.score < 50


def test_evaluator_accepts_cdi_and_cdd_junior():
    evaluator = OfferEvaluator()
    offer_cdi = JobOffer(
        title="Ingénieur Méthodes & Process CDI Débutant",
        company="SEWS CABIND Maroc",
        location="Casablanca",
        url="https://example.com/cdi-methodes",
        description="Recrutement en CDI pour ingénieur débutant ou première expérience en méthodes industrielles, chronométrage et équilibrage de chaîne.",
        source="linkedin_guest"
    )

    assert evaluator.is_contract_match(offer_cdi) is True
    assert evaluator.is_industrial_offer(offer_cdi) is True
    evaluated = evaluator.evaluate(offer_cdi)
    assert evaluated.score >= 60


def test_evaluator_rejects_non_industrial_offers():
    evaluator = OfferEvaluator()

    # Case 1: Pure web/frontend developer
    offer_web = JobOffer(
        title="Développeur Frontend React / Redux",
        company="WebAgency",
        location="Casablanca",
        url="https://example.com/frontend",
        description="Développement d'interfaces utilisateur modernes en React, CSS3 et TypeScript.",
        source="linkedin_guest"
    )
    assert evaluator.is_industrial_offer(offer_web) is False

    # Case 2: IT Support / Helpdesk
    offer_support = JobOffer(
        title="Stagiaire Support Technique & Helpdesk IT",
        company="TelecomCorp",
        location="Casablanca",
        url="https://example.com/stage-support",
        description="Support utilisateurs niveau 1, gestion de parc informatique et ticketing.",
        source="emploima"
    )
    assert evaluator.is_industrial_offer(offer_support) is False

    # Case 3: Pure Accounting
    offer_compta = JobOffer(
        title="Comptable Confirmé",
        company="FinanceCorp",
        location="Casablanca",
        url="https://example.com/compta",
        description="Tenue des journaux comptables, rapprochements bancaires et déclarations fiscales.",
        source="emploima"
    )
    assert evaluator.is_industrial_offer(offer_compta) is False


def test_evaluator_accepts_core_industrial_topics():
    evaluator = OfferEvaluator()

    # Case 1: Lean Manufacturing & 5S
    offer_lean = JobOffer(
        title="Ingénieur Lean & Performance Industrielle",
        company="Automotive Plant Tanger",
        location="Tanger",
        url="https://example.com/lean-tanger",
        description="Déploiement des chantiers Kaizen, 5S, management visuel et optimisation DMAIC.",
        source="dreamjob"
    )
    assert evaluator.is_industrial_offer(offer_lean) is True
    assert evaluator.evaluate(offer_lean).score >= 70

    # Case 2: Supply Chain & Logistics
    offer_supply = JobOffer(
        title="Chargé de Planification & Supply Chain",
        company="LogisticsHub Casablanca",
        location="Casablanca",
        url="https://example.com/supply-casa",
        description="Gestion des approvisionnements, calcul des stocks de sécurité, planification PIC et PDP avec ERP Odoo.",
        source="joblia"
    )
    assert evaluator.is_industrial_offer(offer_supply) is True
    assert evaluator.evaluate(offer_supply).score >= 70


def test_evaluator_rejects_french_jai_false_positive():
    """Ensures French expressions like 'j'ai' do not falsely match an offer."""
    evaluator = OfferEvaluator()
    offer = JobOffer(
        title="Poste en Administration & Secrétariat",
        company="Société Casablancaise",
        location="Casablanca",
        url="https://example.com/admin-sec",
        description="Nous cherchons un candidat. J'ai le plaisir de partager cette opportunité administrative.",
        source="rekrute"
    )

    assert evaluator.is_industrial_offer(offer) is False
    assert evaluator.evaluate(offer).score < 50


def test_company_directory_auto_email_resolution():
    """Verifies that known Moroccan industrial/tech employers have their recruitment email auto-resolved."""
    offer_cap = JobOffer(
        title="Ingénieur Qualité / Méthodes",
        company="Capgemini Engineering Maroc",
        location="Casablanca",
        url="https://example.com/capgemini",
        source="rekrute"
    )
    assert offer_cap.contact_email == "recrutementmaroc.ceg@capgemini.com"

    # Alten without email
    offer_alten = JobOffer(
        title="Ingénieur Systèmes Industriels",
        company="Alten Delivery Center Maroc",
        location="Fès",
        url="https://example.com/alten",
        source="rekrute"
    )
    assert offer_alten.contact_email == "recrutement.maroc@alten.com"


def test_evaluator_rejects_pfe_and_internships():
    """Verifies that pure PFE internships are disqualified in favor of real job offers."""
    evaluator = OfferEvaluator()
    offer_pfe = JobOffer(
        title="Stage PFE – Ingénieur Amélioration Continue / Lean",
        company="Industrie Automobile Maroc",
        location="Casablanca",
        url="https://example.com/stage-pfe-lean",
        description="Sujet de Stage PFE de 6 mois pour étudiant en fin d'études d'ingénieur. Encadrement projet Lean.",
        source="dreamjob"
    )

    assert evaluator.is_contract_match(offer_pfe) is False
    assert evaluator.is_industrial_offer(offer_pfe) is False
    evaluated = evaluator.evaluate(offer_pfe)
    assert evaluated.score == 0


def test_evaluator_rejects_ai_data_science_offers():
    """Verifies that software, AI, and Data Science offers from legacy databases are disqualified."""
    evaluator = OfferEvaluator()
    offer_ai = JobOffer(
        title="Opportunités PFE chez BTP Consulting, postulez dès maintenant",
        company="BTP Consulting",
        location="Casablanca",
        url="https://example.com/btp-ai",
        description="Stage pour spécialiste en Intelligence Artificielle, Machine Learning, RAG et LangChain.",
        source="linkedin_guest"
    )

    assert evaluator.is_industrial_offer(offer_ai) is False
    assert evaluator.is_contract_match(offer_ai) is False
    evaluated = evaluator.evaluate(offer_ai)
    assert evaluated.score == 0

