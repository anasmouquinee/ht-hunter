"""Unit tests for CoverLetterGenerator and EmailSender for Houda Tazi."""

from src.models.offer import JobOffer
from src.mailer.cover_letter_generator import CoverLetterGenerator
from src.mailer.email_sender import EmailSender


def test_cover_letter_generator():
    offer = JobOffer(
        title="Ingénieur Amélioration Continue & Lean Manufacturing",
        company="LEONI Wiring Systems",
        url="https://example.com/leoni-pfe",
        source="rekrute",
        contact_email="recrutement@leoni.com",
        matched_skills=["Lean Manufacturing", "SMED", "5S"]
    )

    subject = CoverLetterGenerator.generate_subject(offer)
    body = CoverLetterGenerator.generate_body(offer)

    assert "Houda Tazi" in subject or "Houda TAZI" in subject
    assert "LEONI" in body
    assert "ENSA El Jadida" in body
    assert "Curriculum Vitae" in body


def test_email_sender_dry_run():
    offer = JobOffer(
        title="Ingénieur Supply Chain",
        company="SEWS CABIND Maroc",
        url="https://example.com/sews",
        source="rekrute",
        contact_email="rh@sews-cabind.ma"
    )

    sender = EmailSender()
    sender.dry_run = True  # Ensure dry-run
    success = sender.send_application(offer)

    assert success is True


def test_cover_letter_html_generation():
    offer = JobOffer(
        title="Ingénieur Méthodes & Industrialisation",
        company="Valeo Maroc",
        url="https://example.com/valeo",
        source="linkedin_guest",
        matched_skills=["Lean Manufacturing", "5S", "SMED", "VSM"]
    )

    html_body = CoverLetterGenerator.generate_html_body(offer)
    assert "<!DOCTYPE html>" in html_body
    assert "Valeo" in html_body
    assert "ENSA El Jadida" in html_body
    assert "LEONI" in html_body
    assert "SEWS" in html_body
    assert "tazihouda124@gmail.com" in html_body or "tazihouda1108@gmail.com" in html_body


def test_formal_cover_letter_custom_offer(tmp_path):
    offer = JobOffer(
        title="Ingénieur Organisation & Excellence Opérationnelle",
        company="Renault Tanger",
        location="Tanger, Maroc",
        url="https://example.com/renault-lean",
        source="rekrute",
        description="Amélioration continue des flux, standardisation 5S et réduction des gaspillages.",
        matched_skills=["Lean Manufacturing", "5S", "Kaizen"]
    )

    text_letter = CoverLetterGenerator.generate_formal_letter_text(offer)
    html_letter = CoverLetterGenerator.generate_formal_letter_html(offer)

    assert "Houda Tazi" in text_letter or "Houda TAZI" in text_letter
    assert "Renault Tanger" in text_letter
    assert "ENSA El Jadida" in text_letter
    assert "LEONI" in text_letter

    assert "<!DOCTYPE html>" in html_letter
    assert "Renault Tanger" in html_letter
    assert "window.print()" in html_letter
    assert "copyLetterText()" in html_letter

    # Test saving to disk
    paths = CoverLetterGenerator.save_letter_for_offer(
        offer,
        output_dir=tmp_path,
        custom_slug="Lettre_Motivation_Renault_Houda_Tazi"
    )
    assert paths["txt"].exists()
    assert paths["html"].exists()
