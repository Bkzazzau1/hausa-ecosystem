import shutil

import pytest

from core.rust_engine import english_to_hrust, hrust_to_english, run_rust_code


def test_hausa_rust_translates_to_standard_rust():
    source = '''
jama'a aiki main() {
    bari sauya kudi = 1000;
    kudi = kudi + 500;

    idan gaskiya {
        println!("Kudin dake asusunka shine: {}", kudi);
    }
}
'''

    translated = hrust_to_english(source)

    assert "pub fn main()" in translated
    assert "let mut kudi = 1000;" in translated
    assert "if true" in translated


def test_standard_rust_translates_to_hausa_rust():
    source = '''
pub fn main() {
    let mut kudi = 1000;
    kudi = kudi + 500;

    if true {
        println!("Balance: {}", kudi);
    }
}
'''

    translated = english_to_hrust(source)

    assert "jama'a aiki main()" in translated
    assert "bari sauya kudi = 1000;" in translated
    assert "idan gaskiya" in translated


def test_hausa_rust_translation_preserves_strings_and_comments():
    source = '''
// idan gaskiya should stay inside comment
jama'a aiki main() {
    bari sako = "idan gaskiya should stay inside string";
    /* bari sauya should stay inside block comment */
    idan gaskiya {
        println!("{}", sako);
    }
}
'''

    translated = hrust_to_english(source)

    assert "// idan gaskiya should stay inside comment" in translated
    assert '"idan gaskiya should stay inside string"' in translated
    assert "/* bari sauya should stay inside block comment */" in translated
    assert "pub fn main()" in translated
    assert "let sako" in translated
    assert "if true" in translated


def test_standard_rust_translation_preserves_strings_and_comments():
    source = '''
// if true should stay inside comment
pub fn main() {
    let message = "if true should stay inside string";
    /* let mut should stay inside block comment */
    if true {
        println!("{}", message);
    }
}
'''

    translated = english_to_hrust(source)

    assert "// if true should stay inside comment" in translated
    assert '"if true should stay inside string"' in translated
    assert "/* let mut should stay inside block comment */" in translated
    assert "jama'a aiki main()" in translated
    assert "bari message" in translated
    assert "idan gaskiya" in translated


@pytest.mark.skipif(shutil.which("rustc") is None, reason="rustc is not installed")
def test_hausa_rust_runner_executes_file(tmp_path, capsys):
    test_file = tmp_path / "gwaji.hrust"
    test_file.write_text(
        '''
jama'a aiki main() {
    bari sauya kudi = 1000;
    kudi = kudi + 500;

    idan gaskiya {
        println!("Kudin dake asusunka shine: {}", kudi);
    }
}
''',
        encoding="utf-8",
    )

    exit_code = run_rust_code(str(test_file))
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Kudin dake asusunka shine: 1500" in captured.out
