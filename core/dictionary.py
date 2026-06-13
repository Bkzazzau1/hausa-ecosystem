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
}

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
