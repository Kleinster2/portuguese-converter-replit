
def apply_combinations(word1, word2, punct1, punct2):
    """Apply combination rules to two adjacent words."""
    # Only try to combine if both tokens are words (no punctuation)
    if not word1 or not word2 or punct1:
        return None, None
        
    vowels = 'aeiouáéíóúâêîô úãẽĩõũy'
    combined = None
    rule_explanation = None
    
    # Skip bracketed pronouns
    if word1 in ["[eu]", "[nós]"]:
        combined = word2
        rule_explanation = f"Skip bracketed pronoun: {word1} {word2} → {combined}"
        return combined, rule_explanation

    # Rules for combining words
    if word1[-1] == 'r' and word2[0] in vowels:
        combined = word1 + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Keep 'r' when joining with vowel)"
    
    elif word1.endswith('n') and word2.startswith('m'):
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Drop 'n' before 'm')"
    
    elif word1[-1].lower() == word2[0].lower():
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Join same letter/sound)"
    
    elif word1[-1] == 'a' and word2[0] in vowels:
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Join 'a' with following vowel)"
    
    elif word1[-1] == 'u' and word2[0] in vowels:
        if word1.endswith(('eu', 'êu')):
            combined = word1 + word2
            rule_explanation = f"{word1} + {word2} → {combined} (Keep 'eu/êu' before vowel)"
        else:
            combined = word1[:-1] + word2
            rule_explanation = f"{word1} + {word2} → {combined} (Drop 'u' before vowel)"
    
    elif word1[-1] in 'sz' and word2[0] in vowels:
        combined = word1[:-1] + 'z' + word2
        rule_explanation = f"{word1} + {word2} → {combined} ('s' between vowels becomes 'z')"
    
    elif word1[-1] == 'm' and word2[0] in vowels:
        combined = word1 + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Join 'm' with following vowel)"
    
    elif word1.endswith('ia') and word2.startswith('i'):
        combined = word1[:-2] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Drop 'ia' before 'i')"
    
    elif word1.endswith('i') and word2[0] in 'eéê':
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Drop 'i' before e/é/ê)"
    
    elif word1.endswith('á') and word2.startswith('a'):
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Convert 'á' to 'a')"
    
    elif word1.endswith('ê') and word2.startswith('é'):
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Use é)"
    
    elif word1.endswith('yn') and word2.startswith('m'):
        combined = word1[:-2] + 'y' + word2
        rule_explanation = f"{word1} + {word2} → {combined} (yn + m → ym)"
    
    elif word1.endswith(('a', 'ã')) and word2[0] in 'ie':
        if word1.endswith('ga'):
            combined = word1[:-2] + 'gu' + word2
            rule_explanation = f"{word1} + {word2} → {combined} (ga + i/e → gui/gue)"
        elif word1.endswith('ca'):
            combined = word1[:-2] + 'k' + word2
            rule_explanation = f"{word1} + {word2} → {combined} (ca + i/e → ki/ke)"
        else:
            combined = word1[:-1] + word2
            rule_explanation = f"{word1} + {word2} → {combined} (Drop 'a' before i/e)"
    
    elif word1[-1] in vowels and word2[0] in vowels:
        combined = word1 + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Join vowels)"
    
    elif word1[-1].lower() == word2[0].lower():
        combined = word1[:-1] + word2
        rule_explanation = f"{word1} + {word2} → {combined} (Join same letter/sound)"
    
    return combined, rule_explanation
