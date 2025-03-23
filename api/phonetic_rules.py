#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from config.phonetic_dict import PHONETIC_DICTIONARY
from config.irregular_verbs import IRREGULAR_VERBS
from config.verb_patterns import (BASIC_VERB_ROOTS, ACTION_VERB_ROOTS,
                              COGNITIVE_VERB_ROOTS, PROCESS_VERB_ROOTS,
                              ALL_ENDINGS)

# Combined set of all verb roots
ALL_ROOTS = BASIC_VERB_ROOTS | ACTION_VERB_ROOTS | COGNITIVE_VERB_ROOTS | PROCESS_VERB_ROOTS

def is_verb(word):
    """
    Check if a word is a verb by:
    1. Checking if it's in the irregular verbs dictionary
    2. Checking if it has a valid verb root and ending
    """
    if not word:
        return False
    lw = word.lower()
    if lw in IRREGULAR_VERBS or lw in IRREGULAR_VERBS.values():
        return True
    for end in ALL_ENDINGS:
        if lw.endswith(end):
            root = lw[:-len(end)]
            if root in ALL_ROOTS:
                return True
    return False

def preserve_capital(original, transformed):
    """
    Preserve capitalization from the original word in the transformed word.
    If the original starts with uppercase, transform the new word similarly.
    """
    if not original or not transformed:
        return transformed
    if original[0].isupper():
        return transformed[0].upper() + transformed[1:]
    return transformed

def apply_phonetic_rules(word, next_word=None, next_next_word=None, prev_word=None):
    """
    Apply Portuguese phonetic rules to transform a word.
    First checks a dictionary of pre-defined transformations,
    if not found, applies the rules in sequence.

    Args:
        word: The word to transform
        next_word: The next word in the sequence (optional), used for verb detection
        next_next_word: The word after next_word (optional)
        prev_word: The previous word (optional)

    Returns:
        tuple: (transformed_word, explanation)
    """
    if not word:
        return '', ''

    # Initialize explanation list
    explanations = []

    # Helper function to apply regex and add explanation if transformation occurred
    def apply_transform(pattern, repl, text, explanation):
        result = re.sub(pattern, repl, text)
        if result != text:
            explanations.append(explanation)
        return result

    # First check if word is in pre-defined dictionary
    lword = word.lower()
    
    # Special handling for não before verbs
    if lword in ["não", "nao", "nãun", "nãu", "nau"]:
        if next_word:
            pronouns = ["me", "te", "se", "nos", "vos", "lhe", "lhes", "o", "a", "os",
                       "as", "lo", "la", "los", "las", "no", "na", "nos", "nas", "já"]
            if next_word.lower() in pronouns:
                if next_next_word and is_verb(next_next_word):
                    return preserve_capital(word, "nu"), "Negation before pronoun+verb: não → nu"
                elif is_verb(next_word):
                    return preserve_capital(word, "nu"), "Negation before verb: não → nu"
            elif is_verb(next_word):
                return preserve_capital(word, "nu"), "Negation before verb: não → nu"
        return preserve_capital(word, "nãu"), "Default negation: não → nãu"

    # Special handling for você/vocês before verbs
    if lword in ["você", "voce"]:
        if next_word:
            pronouns = ["me", "te", "se", "nos", "vos", "lhe", "lhes", "o", "a", "os",
                       "as", "lo", "la", "los", "las", "no", "na", "nos", "nas", "já", "não", "nao", "nãun", "nãu", "nau"]
            if next_word.lower() in pronouns:
                if next_next_word and is_verb(next_next_word):
                    return preserve_capital(word, "cê"), "Pronoun before pronoun+verb: você → cê"
                elif is_verb(next_word):
                    return preserve_capital(word, "cê"), "Pronoun before verb: você → cê"
            elif is_verb(next_word):
                return preserve_capital(word, "cê"), "Pronoun before verb: você → cê"

    # Special handling for vocês before verbs
    if lword in ["vocês", "voces", "vocêis"]:
        if next_word:
            pronouns = ["me", "te", "se", "nos", "vos", "lhe", "lhes", "o", "a", "os",
                       "as", "lo", "la", "los", "las", "no", "na", "nos", "nas", "já", "não", "nao", "nãun", "nãu", "nau"]
            if next_word.lower() in pronouns:
                if next_next_word and is_verb(next_next_word):
                    return preserve_capital(word, "cêis"), "Pronoun before pronoun+verb: vocês → cêis"
                elif is_verb(next_word):
                    return preserve_capital(word, "cêis"), "Pronoun before verb: vocês → cêis"
            elif is_verb(next_word):
                return preserve_capital(word, "cêis"), "Pronoun before verb: vocês → cêis"

    # Check irregular verbs first
    if lword in IRREGULAR_VERBS:
        trans = IRREGULAR_VERBS[lword].lower()
        trans = preserve_capital(word, trans)
        return trans, f"Irregular verb: {word} → {trans}"
        
    # Check direct transformations and dictionary
    if lword in PHONETIC_DICTIONARY:
        # Special case for 'olho' - treat as verb if preceded by 'eu'
        if lword == 'olho' and next_word is None and word.lower() == 'olho':
            prev_word = prev_word.lower() if prev_word else None
            if prev_word == 'eu':
                if lword in IRREGULAR_VERBS:
                    trans = IRREGULAR_VERBS[lword].lower()
                    trans = preserve_capital(word, trans)
                    return trans, f"Irregular verb: {word} → {trans}"
        trans = PHONETIC_DICTIONARY[lword].lower()
        trans = preserve_capital(word, trans)
        return trans, f"Dictionary: {word} → {trans}"

    # Initialize transformed word
    trans = lword

    # Apply transformation rules
    entrar_forms = ['entrar', 'entro', 'entra', 'entramos', 'entram', 'entrei', 'entrou',
                    'entraram', 'entrava', 'entravam']
    trans = apply_transform(r'^ent', 'int', trans, "Initial ent → int") if word.lower() not in entrar_forms else trans
    trans = apply_transform(r'^des', 'dis', trans, "Transform initial 'des' to 'dis'")
    trans = apply_transform(r'^menti', 'minti', trans, "Transform initial 'menti' to 'minti'")

    trans = apply_transform(r'ovo$', 'ôvo', trans, "Transform ending 'ovo' to 'ôvo'")
    trans = apply_transform(r'ovos$', 'óvos', trans, "Transform ending 'ovos' to 'óvos'")
    trans = apply_transform(r'ogo$', 'ôgo', trans, "Transform ending 'ogo' to 'ôgo'")
    trans = apply_transform(r'ogos$', 'ógos', trans, "Transform ending 'ogos' to 'ógos'")
    trans = apply_transform(r'oso$', 'ôso', trans, "Transform ending 'oso' to 'ôso'")
    trans = apply_transform(r'osos$', 'ósos', trans, "Transform ending 'osos' to 'ósos'")

    if is_verb(word):
        trans = apply_transform(r'ar$', 'á', trans, "Infinitive ending: ar → á")
        trans = apply_transform(r'er$', 'ê', trans, "Infinitive ending: er →ê")
        trans = apply_transform(r'ir$', 'í', trans, "Infinitive ending: ir → í")
        trans = apply_transform(r'am[ou]s$', 'ãmu', trans, "Verb ending 'amos/amus' → 'ãmu'")
        trans = apply_transform(r'em[ou]s$', 'êmu', trans, "Verb ending 'emos/emus' → 'êmu'")
        trans = apply_transform(r'im[ou]s$', 'imu', trans, "Verb ending 'imos/imus' → 'imu'")

    trans = apply_transform(r'o$', 'u', trans, "Final o → u")
    trans = apply_transform(r'os$', 'us', trans, "Final os → us")
    trans = apply_transform(r'e$', 'i', trans, "Final e → i")
    trans = apply_transform(r'es$', 'is', trans, "Final es → is")
    trans = apply_transform(r'ão$', 'ãun', trans, "ão → ãun")
    trans = apply_transform(r'^es', 'is', trans, "Initial es → is")

    # Rule 9p: 's' between vowels becomes 'z'
    if re.search(r'([aeiouáéíóúâêîôúãẽĩõũ])s([aeiouáéíóúâêîôúãẽĩõũ])', trans, re.IGNORECASE):
        trans = apply_transform(r'([aeiouáéíóúâêîôúãẽĩõũ])s([aeiouáéíóúâêîôúãẽĩõũ])', r'\1z\2',
                              trans, "s → z between vowels")

    trans = apply_transform(r'olh', 'ôli', trans, "olh → ôly") if not is_verb(word) else trans
    trans = apply_transform(r'lh', 'li', trans, "lh → ly")
    # Unified rule for any "ou" to "ô" transformation anywhere in the word
    trans = apply_transform(r'ou', 'ô', trans, "ou → ô (anywhere)")

    consonants = 'bcdfgjklmnpqrstvwxz'
    trans = apply_transform(r'al([' + consonants + '])', r'au\1', trans, "al+consonant → au")
    trans = apply_transform(r'on(?!h)([' + consonants + '])', r'oun\1', trans, "on+consonant → oun")
    trans = apply_transform(r'am$', 'ã', trans, "Final am → ã")
    trans = apply_transform(r'em$', 'êin', trans, "Final em →êin")
    trans = apply_transform(r'om$', 'ôun', trans, "Final om → ôun")
    trans = apply_transform(r'um$', 'un', trans, "Final um → un")
    trans = apply_transform(r'^h', '', trans, "Remove initial h")
    trans = apply_transform(r'^ex', 'iz', trans, "Initial ex → iz")
    trans = apply_transform(r'^pol', 'pul', trans, "Initial pol → pul")
    trans = apply_transform(r'ol$', 'óu', trans, "Final ol → óu")
    trans = apply_transform(r'l$', 'u', trans, "Final l → u")
    trans = apply_transform(r'ul([' + consonants + '])', r'u\1', trans, "ul before consonant → u (remove duplicate u)")
    trans = apply_transform(f'([^u])l([{consonants}])', r'\1u\2', trans, "l before consonant → u (if not after u)")

    for p in ['bs', 'ps', 'pn', 'dv', 'pt', 'pç', 'dm', 'gn', 'tm', 'tn']:
        trans = apply_transform(rf'({p[0]})({p[1]})', r'\1i\2', trans,
                              f"Insert i: {p} → {p[0]}i{p[1]}")

    trans = apply_transform(r'[dtbfjkpv]$', r'\0i', trans, "Append i after final consonant")
    trans = apply_transform(r'c$', 'ki', trans, "Final c → ki")
    trans = apply_transform(r'g$', r'\0ui', trans, "Append ui after final g")
    trans = apply_transform(r'eir', 'êr', trans, "eir → êr")
    # Removed specific initial 'ou' rules as they're covered by the unified rule
    trans = apply_transform(r'^des', 'dis', trans, "Transform initial 'des' to 'dis'")
    trans = apply_transform(r'ora$', 'óra', trans, "Transform ending 'ora' to 'óra'")
    trans = apply_transform(r'oras$', 'óras', trans, "Transform ending 'oras' to 'óras'")
    trans = apply_transform(r'ês$', 'êis', trans, "Final 'ês' becomes 'êis'")

    # Preserve capitalization
    trans = preserve_capital(word, trans)

    explanation = " + ".join(explanations) if explanations else "No changes needed"
    return trans, explanation