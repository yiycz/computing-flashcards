"""Small build hook: validate the collection and pass content to the theme."""
import json
from pathlib import Path

from mkdocs.exceptions import PluginError


def on_config(config):
    topics = config.extra.get("topics", [])
    ids = [topic["id"] for topic in topics]
    if len(ids) != len(set(ids)):
        raise PluginError("Each topic in mkdocs.yml needs a unique id.")
    path = Path(config.docs_dir) / "assets" / "flashcards.json"
    try:
        cards = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PluginError(f"Cannot read flashcards.json: {exc}") from exc
    if not isinstance(cards, list):
        raise PluginError("flashcards.json must contain a JSON array.")
    seen = set()
    for card in cards:
        if not isinstance(card, dict) or not all(
            isinstance(card.get(key), str) and card[key].strip()
            for key in ("id", "topic", "question", "answer")
        ):
            raise PluginError("Every flashcard needs id, topic, question, and answer strings.")
        if card["id"] in seen or card["topic"] not in ids:
            raise PluginError(f"Duplicate card id or unknown topic: {card['id']}")
        seen.add(card["id"])
    config.extra["study_cards"] = cards
    return config


def on_page_context(context, page, config, nav):
    context["study_data"] = {"topics": config.extra["topics"], "cards": config.extra["study_cards"]}
    return context
