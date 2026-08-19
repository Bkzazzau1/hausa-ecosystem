# core/dictionary.py
"""Keyword and error mappings for Hausa-flavoured programming files."""

PYTHON_KEYWORDS = {
    # Basic Input/Output & Logic Flow
    "buga": "print",
    "shigar": "input",
    "idan": "if",
    "sauran_idan": "elif",
    "in_ba_haka_ba": "else",

    # Native Data Types
    "lamba": "int",
    "lamba_dige": "float",
    "rubutu": "str",
    "jeri": "list",
    "makullai": "dict",
    "saiti": "set",
    "biyu_biyu": "tuple",

    # SQL & NoSQL Database Engine Keywords
    "bude_rufa": "connect",
    "binciko": "SELECT",
    "saka_cikin": "INSERT",
    "sabunta": "UPDATE",
    "goge_daga": "DELETE",
    "tebur": "TABLE",
    "Abokin_Hadin_Mongo": "MongoClient",
    "kunshe_bayanai": "collection",
    "takarda": "document",
    "nemo_guda": "find_one",
    "saka_guda": "insert_one",

    # Practical SQLite / database method names
    "samu_cursor": "cursor",
    "aiwatar": "execute",
    "aiwatar_da_yawa": "executemany",
    "karba_guda": "fetchone",
    "karba_duka": "fetchall",
    "ajiye": "commit",
    "janye": "rollback",
    "rufe": "close",
    "layuka": "rowcount",
    "sabon_id": "lastrowid",

    # Common ORM / query builder vocabulary
    "tace": "filter",
    "tace_da": "filter_by",
    "farko": "first",
    "duka": "all",
    "kirkiro": "create",
    "adana": "save",
    "nemo": "find",
    "nemo_ko_404": "get_or_404",
    "shafi": "paginate",
    "oda_da": "order_by",
    "hawa": "asc",
    "sauka": "desc",

    # Full-Backend Routing & HTTP Server Keywords
    "Injin_Yanar_Gizo": "Flask",
    "bude_hanya": "route",
    "bukata": "request",
    "buƙata": "request",
    "amsa": "response",
    "tsarin_bayanai": "dict",
    "juya_zuwa_json": "jsonify",
    "rufe_sirri": "hashlib",
    "karanta_json": "get_json",
    "samu": "get",
    "aika": "post",
    "saka": "put",
    "gyara_sashe": "patch",
    "goge_hanya": "delete",

    # FastAPI / modern backend vocabulary
    "Saurin_API": "FastAPI",
    "Mai_Hanya": "APIRouter",
    "Kuskuren_HTTP": "HTTPException",
    "Dogaro": "Depends",
    "Matsayi": "status",
    "Tushen_Model": "BaseModel",
    "Filin": "Field",
    "Sabar_Uvicorn": "uvicorn",
    "gudanar": "run",

    # Loops & Controls
    "ga": "for",
    "cikin": "in",
    "yayin": "while",
    "tsaya": "break",
    "wuce": "continue",

    # Structural blocks, objects & scoping
    "aiki": "def",
    "mayar": "return",
    "aji": "class",
    "kamar": "as",
    "babban_gari": "global",
    "ba_na_ciki": "nonlocal",
    "goge": "del",

    # Pattern Matching (Python 3.10+)
    "dace": "match",
    "hali": "case",

    # Error Handling & Context
    "gwada": "try",
    "kama": "except",
    "karshe": "finally",
    "tada": "raise",
    "tabbatar": "assert",
    "tare_da": "with",

    # Imports & Packages
    "daga": "from",
    "shigo": "import",

    # Core Constants & Booleans
    "karya": "False",
    "gaskiya": "True",
    "babu": "None",

    # Logical Operators
    "kuma": "and",
    "ko": "or",
    "ba": "not",
    "shi_ne": "is",

    # Asynchronous Multi-threading
    "babu_guda": "async",
    "jira": "await",

    # Anonymous functions & place-holders
    "alamun_haske": "lambda",
    "wuce_kawai": "pass",

    # Python 3.14 language additions completed for Version 1.
    "bayar": "yield",
    "nau_i": "type",
}

# Python 3.14 built-in functions. These live in their own profile because names
# such as ``map`` and ``filter`` are ordinary identifiers, not reserved syntax.
PYTHON_BUILTINS = {
    "cikakkiyar_daraja": "abs",
    "mai_maimaitawa_maras_jira": "aiter",
    "na_gaba_maras_jira": "anext",
    "duk_gaskiya": "all",
    "wani_gaskiya": "any",
    "askil": "ascii",
    "tsarin_biyu": "bin",
    "gaskiya_ko_karya": "bool",
    "wurin_tsayawa": "breakpoint",
    "jerin_baiti": "bytearray",
    "baitoci": "bytes",
    "mai_kira": "callable",
    "harafi": "chr",
    "aikin_aji": "classmethod",
    "hada_shiri": "compile",
    "lamba_hadaddiya": "complex",
    "goge_sifa": "delattr",
    "kundin_siffofi": "dir",
    "rabo_da_saura": "divmod",
    "kirga_jeri": "enumerate",
    "kimanta": "eval",
    "aiwatar_rubutu": "exec",
    "tace": "filter",
    "tsara": "format",
    "saitin_daskare": "frozenset",
    "samu_sifa": "getattr",
    "sunayen_duniya": "globals",
    "yana_da_sifa": "hasattr",
    "tambarin_hash": "hash",
    "taimako": "help",
    "tsarin_goma_sha_shida": "hex",
    "shaida": "id",
    "nau_in_abu_ne": "isinstance",
    "karamin_aji_ne": "issubclass",
    "mai_maimaitawa": "iter",
    "tsawo": "len",
    "sunayen_ciki": "locals",
    "taswira": "map",
    "mafi_girma": "max",
    "kallon_ma_ajiya": "memoryview",
    "mafi_karami": "min",
    "na_gaba": "next",
    "abu": "object",
    "tsarin_takwas": "oct",
    "bude_fayil": "open",
    "lambar_harafi": "ord",
    "daukaka": "pow",
    "sifa": "property",
    "kewayo": "range",
    "wakilci": "repr",
    "juya_baya": "reversed",
    "zagaye_lamba": "round",
    "saita_sifa": "setattr",
    "yanki": "slice",
    "jera": "sorted",
    "aikin_tsaye": "staticmethod",
    "jimla": "sum",
    "uwar_aji": "super",
    "sauye_sauye": "vars",
    "hada_jeri": "zip",
    "shigo_na_ciki": "__import__",
}

# These common types/functions already have stable names in PYTHON_KEYWORDS.
PYTHON_BUILTIN_WORDS = set(PYTHON_BUILTINS) | {
    "buga", "shigar", "lamba", "lamba_dige", "rubutu", "jeri", "makullai",
    "saiti", "biyu_biyu", "nau_i",
}
PYTHON_KEYWORDS.update(PYTHON_BUILTINS)

RUST_KEYWORDS = {
    # Functional Declarations & Variables
    "aiki": "fn",
    "bari": "let",
    "sauya": "mut",
    "aji": "class",  # Reserved word in Rust for future use

    # Conditional & Structural Control Flow
    "idan": "if",
    "in_ba_haka_ba": "else",
    "dace": "match",

    # Loops
    "yayin": "while",
    "zagaye": "loop",
    "ga": "for",
    "cikin": "in",
    "tsaya": "break",
    "wuce": "continue",

    # Jumps & Flows
    "mayar": "return",

    # Modules & Visibility
    "jama'a": "pub",
    "amfani": "use",
    "sashe": "mod",
    "akwati": "crate",
    "babba": "super",
    "kamar": "as",

    # Custom Types & Behaviors
    "tsari": "struct",
    "lissafi": "enum",
    "hali": "trait",
    "aiwatar": "impl",
    "nau'i": "type",
    "kai_tsaye": "self",
    "KAI_TSAYE": "Self",

    # Data Integrity & Constants
    "tabbatacce": "const",
    "tsayayye": "static",
    "nuni": "ref",
    "motsa": "move",
    "hadari": "unsafe",
    "inda": "where",
    "waje": "extern",
    "sauye_sauye": "dyn",

    # Asynchronous Programming
    "babu_guda": "async",
    "jira": "await",

    # Booleans
    "gaskiya": "true",
    "karya": "false",
}

# Comprehensive Python Error Mapping
PYTHON_ERRORS = {
    "SyntaxError": "Kuskuren Tsarin Rubutu (SyntaxError)",
    "NameError": "Kuskuren Suna - An yi amfani da kalma ko variable da ba a bayyana ba (NameError)",
    "TypeError": "Kuskuren Nau'in Bayanai - Kana kokarin hada abubuwa mabanbanta (TypeError)",
    "ValueError": "Kuskuren Darajar Bayanai - Bayanin da ka shigar bai dace ba (ValueError)",
    "IndentationError": "Kuskuren Tazarar Layi - Duba tazarar dake farkon layinka (IndentationError)",
    "ZeroDivisionError": "Kuskuren Raba Lamba - Ba za a iya raba lamba da sifili (0) ba (ZeroDivisionError)",
    "ModuleNotFoundError": "Ba a sami wannan kunshin (Library) dake cikin shirinka ba (ModuleNotFoundError)",
    "OperationalError": "Kuskuren tafiyar da Database (OperationalError)",
    "IntegrityError": "Kuskuren ka'idar Database - bayanin ya karya sharadin tebur (IntegrityError)",
    "IndexError": "Kuskuren Jeri - Gurbin da kake nema a cikin jeri (List) bai wanzu ba (IndexError)",
    "KeyError": "Kuskuren Makulli - Makullin (Key) da kake nema a Dictionary bai wanzu ba (KeyError)",
    "AttributeError": "Kuskuren Kaddara - Wannan aji (Class) din ba shi da wannan kaddarar (AttributeError)",

    # Common Raw Sub-Strings inside messages
    "is not defined": "ba a ayyana shi ba sam a cikin shirinka",
    "invalid syntax": "tsarin rubutunka yana da kuskure gaba daya",
    "division by zero": "ba za a iya raba lamba da sifili (0) ba",
    "unexpected indent": "an sami tazarar layi mara kyau da ba a gata ba",
    "no such table": "ba a sami wannan teburin a database ba",
    "UNIQUE constraint failed": "an karya ka'idar UNIQUE a database",
}

# Comprehensive Rust Compiler Warnings & Error Sub-strings
RUST_ERRORS = {
    "cannot mutate immutable variable": "Ba za ka iya canza darajar variable tabbatacce ba! (Kada ka manta sanya 'sauya' / 'mut')",
    "cannot assign twice to immutable variable": "Ba za ka iya ba variable daraja sau biyu ba idan ba ka sanya 'sauya' / 'mut' ba",
    "cannot find function": "Ba a sami wannan aiki (Function) din ba gaba daya. Duba rubutunka",
    "expected struct": "An saba samun tsari (Struct) anan amma an sami wani abu daban",
    "mismatched types": "Nau'ikan bayanai ba su dace ba (Mismatched Types)",
    "cannot find type": "Ba a sami wannan nau'in bayani (Type) ba a cikin shirinka",
    "unresolved import": "Ba a sami wannan kunshe dake kokarin shigo da shi ba (Unresolved Import)",
    "expected semicolon": "An manta sanya alamar datsa ';' a karshen wannan layin",
    "borrow of moved value": "Kuskuren Mallakar Bayani! An riga an motsa wannan bayanin zuwa wani wurin daban (Borrow of Moved Value)",
}

# Vocabulary is deliberately split into profiles.  ``all`` remains the default
# for backward compatibility, while applications can select smaller profiles to
# avoid translating framework method names that happen to match user names.
PYTHON_CORE_WORDS = {
    "buga", "shigar", "idan", "sauran_idan", "in_ba_haka_ba", "lamba",
    "lamba_dige", "rubutu", "jeri", "makullai", "saiti", "biyu_biyu",
    "ga", "cikin", "yayin", "tsaya", "wuce", "aiki", "mayar", "aji",
    "kamar", "babban_gari", "ba_na_ciki", "goge", "dace", "hali", "gwada",
    "kama", "karshe", "tada", "tabbatar", "tare_da", "daga", "shigo",
    "karya", "gaskiya", "babu", "kuma", "ko", "ba", "shi_ne", "babu_guda",
    "jira", "alamun_haske", "wuce_kawai", "bayar", "nau_i",
}
PYTHON_DATABASE_WORDS = {
    "bude_rufa", "binciko", "saka_cikin", "sabunta", "goge_daga", "tebur",
    "Abokin_Hadin_Mongo", "kunshe_bayanai", "takarda", "nemo_guda", "saka_guda",
    "samu_cursor", "aiwatar", "aiwatar_da_yawa", "karba_guda", "karba_duka",
    "ajiye", "janye", "rufe", "layuka", "sabon_id", "tace", "tace_da",
    "farko", "duka", "kirkiro", "adana", "nemo", "nemo_ko_404", "shafi",
    "oda_da", "hawa", "sauka",
}
PYTHON_FLASK_WORDS = {
    "Injin_Yanar_Gizo", "bude_hanya", "bukata", "buƙata", "amsa",
    "tsarin_bayanai", "juya_zuwa_json", "rufe_sirri", "karanta_json",
    "samu", "aika", "saka", "gyara_sashe", "goge_hanya",
}
PYTHON_FASTAPI_WORDS = {
    "Saurin_API", "Mai_Hanya", "Kuskuren_HTTP", "Dogaro", "Matsayi",
    "Tushen_Model", "Filin", "Sabar_Uvicorn", "gudanar", "samu", "aika",
    "saka", "gyara_sashe", "goge_hanya",
}
PYTHON_WEB_WORDS = PYTHON_FLASK_WORDS | PYTHON_FASTAPI_WORDS

PYTHON_VOCABULARY_PROFILES = {
    "core": {key: PYTHON_KEYWORDS[key] for key in PYTHON_CORE_WORDS},
    "database": {key: PYTHON_KEYWORDS[key] for key in PYTHON_CORE_WORDS | PYTHON_DATABASE_WORDS},
    "web": {key: PYTHON_KEYWORDS[key] for key in PYTHON_CORE_WORDS | PYTHON_WEB_WORDS},
    "flask": {key: PYTHON_KEYWORDS[key] for key in PYTHON_CORE_WORDS | PYTHON_DATABASE_WORDS | PYTHON_FLASK_WORDS},
    "fastapi": {key: PYTHON_KEYWORDS[key] for key in PYTHON_CORE_WORDS | PYTHON_DATABASE_WORDS | PYTHON_FASTAPI_WORDS},
    "builtins": {key: PYTHON_KEYWORDS[key] for key in PYTHON_CORE_WORDS | PYTHON_BUILTIN_WORDS},
    "all": dict(PYTHON_KEYWORDS),
}
RUST_VOCABULARY_PROFILES = {"core": dict(RUST_KEYWORDS), "all": dict(RUST_KEYWORDS)}


def get_python_vocabulary(profile="all"):
    """Return a copy of a named Hausa Python vocabulary profile."""
    try:
        return dict(PYTHON_VOCABULARY_PROFILES[profile])
    except KeyError as error:
        raise ValueError(f"Unknown Python vocabulary profile: {profile}") from error


def get_rust_vocabulary(profile="all"):
    """Return a copy of a named Hausa Rust vocabulary profile."""
    try:
        return dict(RUST_VOCABULARY_PROFILES[profile])
    except KeyError as error:
        raise ValueError(f"Unknown Rust vocabulary profile: {profile}") from error
