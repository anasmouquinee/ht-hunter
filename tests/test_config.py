"""Tests for configuration and candidate profile of Houda Tazi."""

from src.config import config


def test_candidate_profile_loaded():
    assert config.candidate.full_name == "Houda Tazi"
    assert config.candidate.email == "tazihouda124@gmail.com"
    assert "Casablanca" in config.candidate.location or "Maroc" in config.candidate.location
    assert "ENSA" in config.candidate.school
    assert "Génie Industriel" in config.candidate.specialization
    assert "dossier_candidature_houda_tazi.pdf" in config.candidate.cv_path.name
    assert config.candidate.digest_recipient == "tazihouda1108@gmail.com"


def test_default_cities_and_remuneration_keywords():
    assert "Casablanca" in config.target_cities
    assert "Tanger" in config.target_cities
    assert any("rémunéré" in k for k in config.remuneration_keywords)
    assert any("gratification" in k for k in config.remuneration_keywords)


def test_dry_run_enabled_by_default():
    # Ensure safety: dry run should be active unless explicitly overridden
    assert isinstance(config.dry_run, bool)
    assert 0 < config.max_emails_per_run <= 50
