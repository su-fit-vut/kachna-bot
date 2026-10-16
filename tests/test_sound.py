from unittest.mock import Mock, call

import sound


def test_play_uses_paplay_for_each_file(monkeypatch):
    run = Mock()
    monkeypatch.setattr(sound.subprocess, "run", run)
    player = sound.Sound("test", ["first.wav", "second.ogg"], spotify=None)

    player.play()

    assert run.call_args_list == [
        call(["paplay", "first.wav"], check=True),
        call(["paplay", "second.ogg"], check=True),
    ]
