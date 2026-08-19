import pytest

from core.python_engine import TranslationError, english_to_hausa, hausa_to_english, run_hausa_code


def test_hausa_python_translates_to_english():
    source = '''
suna = "Bashir"
buga("Sannu", suna)
idan gaskiya:
    buga("Hausa Python yana aiki")
'''

    translated = hausa_to_english(source)

    assert 'print("Sannu", suna)' in translated
    assert 'if True:' in translated
    assert 'print("Hausa Python yana aiki")' in translated


def test_english_python_translates_to_hausa():
    source = '''
name = "Bashir"
print("Hello", name)
if True:
    print("English to Hausa works")
'''

    translated = english_to_hausa(source)

    assert 'buga("Hello", name)' in translated
    assert 'idan gaskiya:' in translated
    assert 'buga("English to Hausa works")' in translated


def test_hausa_python_runner_executes_file(tmp_path, capsys):
    test_file = tmp_path / "hello.hausa"
    test_file.write_text(
        '''
suna = "Bashir"
buga("Sannu", suna)
idan gaskiya:
    buga("Hausa Python yana aiki")
''',
        encoding="utf-8",
    )

    exit_code = run_hausa_code(str(test_file))
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Sannu Bashir" in captured.out
    assert "Hausa Python yana aiki" in captured.out


def test_hausa_python_runner_shows_localized_error(tmp_path, capsys):
    test_file = tmp_path / "error.hausa"
    test_file.write_text("buga(abun_da_babu)\n", encoding="utf-8")

    exit_code = run_hausa_code(str(test_file))
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "AN SAMI KUSKURE" in captured.out
    assert "Kuskuren Suna" in captured.out
    assert "ba a ayyana shi ba" in captured.out


def test_core_profile_does_not_translate_database_methods():
    translated = hausa_to_english("hadi.ajiye()\nbuga('ok')\n", profile="core")
    assert "hadi.ajiye()" in translated
    assert "print('ok')" in translated


def test_malformed_token_stream_is_rejected_without_regex_fallback():
    with pytest.raises(TranslationError):
        hausa_to_english('buga("idan')


def test_python_314_keyword_and_builtins_profile():
    source = """aiki lambobi():
    ga daraja cikin kewayo(3):
        bayar daraja

buga(jimla(lambobi()))
"""
    translated = hausa_to_english(source, profile="builtins")
    assert "for daraja in range(3):" in translated
    assert "yield daraja" in translated
    assert "print(sum(lambobi()))" in translated


def test_python_314_soft_type_keyword_translation():
    assert "type Suna = str" in hausa_to_english("nau_i Suna = rubutu\n", profile="core")
