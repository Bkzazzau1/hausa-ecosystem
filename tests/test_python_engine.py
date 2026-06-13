from core.python_engine import english_to_hausa, hausa_to_english, run_hausa_code


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
