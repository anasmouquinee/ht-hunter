"""Unit tests for Telegram, Discord, and Anonymous Digest notifiers."""

from unittest.mock import patch, MagicMock
from src.models.offer import JobOffer
from src.notifier.telegram_notifier import TelegramNotifier
from src.notifier.discord_notifier import DiscordNotifier
from src.notifier.anonymous_digest import AnonymousDigestNotifier


def test_telegram_formatting():
    offer = JobOffer(
        title="Ingénieur Lean Manufacturing",
        company="LEONI Berrechid",
        url="https://example.com/pfe",
        source="linkedin_guest",
        linkedin_url="https://linkedin.com/posts/hr-post-123",
        contact_email="rh@leoni.ma",
        is_remunerated=True,
        score=94,
        matched_skills=["Lean", "5S"]
    )

    notifier = TelegramNotifier(bot_token="fake_token", chat_id="12345")
    msg = notifier.format_message(offer, email_sent=True)

    assert "LEONI Berrechid" in msg
    assert "Ingénieur Lean" in msg
    assert "<b>Poste :</b>" in msg
    assert "94%" in msg
    assert "rh@leoni.ma" in msg


@patch("requests.post")
def test_discord_notifier_mock_send(mock_post):
    mock_post.return_value = MagicMock(status_code=204)

    offer = JobOffer(
        title="Ingénieur Supply Chain",
        company="SEWS Tanger",
        url="https://example.com/sews2",
        source="rekrute",
        linkedin_url="https://linkedin.com/in/hr-profile",
        contact_email="jobs@sews.ma",
        is_remunerated=True,
        score=90
    )

    notifier = DiscordNotifier(webhook_url="https://discord.com/api/webhooks/mock")
    success = notifier.send_alert(offer, email_sent=True)

    assert success is True
    assert mock_post.called


def test_anonymous_digest_notifier_html_generation():
    notifier = AnonymousDigestNotifier()
    offer = JobOffer(
        title="Ingénieur Amélioration Continue (Lean / SMED)",
        company="LEONI Wiring Systems",
        location="Berrechid, Maroc",
        url="https://example.com/leoni-lean",
        source="dreamjob",
        score=96,
        matched_skills=["Lean Manufacturing", "SMED", "5S"]
    )
    html = notifier.render_digest_html([offer], title="Veille Opportunités")
    assert "LEONI Wiring Systems" in html
    assert "Amélioration Continue" in html
    assert "Veille Opportunités" in html
    # Ensure complete anonymity: no trace of Anas Mouquine
    assert "Anas" not in html
    assert "mouquine" not in html.lower()
