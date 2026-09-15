"""
text_cleaner.py
Cleans and normalizes raw resume text while preserving important
technical symbols such as C++, C#, and .NET.
"""

import re

# Tokens that must NOT be damaged by symbol-stripping.
# We protect them with placeholders before cleaning, then restore them.
PROTECTED_TOKENS = {
    "c++": "zzcpluspluszz",
    "c#": "zzcsharpzz",
    ".net": "zzdotnetzz",
    "node.js": "zznodejszz",
    "asp.net": "zzaspnetzz",
}


def clean_text(raw_text: str) -> str:
    """
    Lowercases text, protects known technical tokens, strips unwanted
    symbols and repeated whitespace, then restores the protected tokens.
    """
    text = raw_text.lower()

    # Step 1: protect special technical tokens
    for token, placeholder in PROTECTED_TOKENS.items():
        text = text.replace(token, placeholder)

    # Step 2: remove unwanted symbols (keep letters, numbers, spaces, placeholders)
    text = re.sub(r"[^a-z0-9_\s]", " ", text)

    # Step 3: collapse repeated whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Step 4: restore protected tokens
    for token, placeholder in PROTECTED_TOKENS.items():
        text = text.replace(placeholder, token)

    return text


if __name__ == "__main__":
    sample = "Experienced in C++, C#, .NET and Node.js!!  Also   Python & SQL."
    print(clean_text(sample))