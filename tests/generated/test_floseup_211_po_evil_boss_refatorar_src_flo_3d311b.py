from flose.solutions.floseup_211_po_evil_boss_refatorar_src_flo_3d311b import *
import pytest

async def test_do_real_commit():
    hero_key = "test_hero"
    topic = "test_topic"
    card_id = "test_card"

    result = await _do_real_commit(hero_key, topic, card_id)
    
    assert isinstance(result, str)
    assert result == f"Commit realizado com sucesso para {topic} e ID de cartão {card_id}"