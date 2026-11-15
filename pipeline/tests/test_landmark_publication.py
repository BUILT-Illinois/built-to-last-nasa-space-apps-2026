# Drafted with AI assistance (Codex); see docs/AI_USAGE.md.
from pathlib import Path

import pytest

from pipeline.validate_manifest import check_landmarks, load_json


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "app/public/data"
CONTENT = ROOT / "content/landmarks"


def read_json(path):
    value, problems = load_json(path)
    assert not problems, f"{path}: {problems}"
    return value


def card_fields(document):
    return {
        card["id"]: {key: value for key, value in card.items() if key != "series"}
        for card in document["landmarks"]
    }


@pytest.mark.parametrize("manifest_path", sorted(DATA.glob("*/manifest.json")), ids=lambda p: p.parent.name)
def test_published_landmarks_match_contract_and_authored_cards(manifest_path):
    region = manifest_path.parent.name
    manifest = read_json(manifest_path)
    source_ids = {source["id"] for source in manifest["sources"]}
    published_path = manifest_path.with_name("landmarks.json")
    published = read_json(published_path)
    problems = check_landmarks(published, region, source_ids)
    assert not problems, f"{published_path}: " + "\n".join(problems)

    authored_path = CONTENT / f"{region}.json"
    if authored_path.is_file():
        authored = read_json(authored_path)
        problems = check_landmarks(authored, region, source_ids)
        assert not problems, f"{authored_path}: " + "\n".join(problems)
        assert card_fields(published) == card_fields(authored), (
            f"{published_path}: publish the authored cards from {authored_path} "
            "with their original ids, coordinates, text, and sources"
        )


def test_every_authored_landmark_file_has_a_published_region():
    for authored in CONTENT.glob("*.json"):
        assert (DATA / authored.stem / "manifest.json").is_file(), (
            f"{authored}: no published manifest for region {authored.stem}"
        )
