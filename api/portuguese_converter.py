#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import traceback
import io
import unicodedata
from phonetic_rules import apply_phonetic_rules
from word_combinations import apply_combinations
from config.verb_patterns import (BASIC_VERB_ROOTS, ACTION_VERB_ROOTS,
                                COGNITIVE_VERB_ROOTS, PROCESS_VERB_ROOTS)
from config.word_pairs import WORD_PAIRS

# Words ending in 'l' that have special accent patterns
ACCENTED_L_SUFFIXES = {
    'avel': 'ável',  # amável, notável, etc.
    'ável': 'ável',  # For words that already have the accent
    'ivel': 'ível',  # possível, visível, etc.
    'ível': 'ível',  # For words that already have the accent
    'ovel': 'óvel',  # móvel, imóvel, etc.
    'óvel': 'óvel',  # For words that already have the accent
}

# Words ending in 'l' that have unique accent patterns
ACCENTED_L_WORDS = {
    'ágil', 'útil', 'fácil', 'fútil', 'hábil', 'débil', 'dócil', 'fértil',
    'fóssil', 'frágil', 'hífen', 'hóstil', 'húmil', 'lábil', 'míssil',
    'pénsil', 'réptil', 'têxtil', 'tátil', 'túnel', 'dúctil', 'cônsul',
    'níquel', 'álcool'
}



# Direct transformations that bypass the phonetic rules pipeline
DIRECT_TRANSFORMATIONS = {
    'vamos': 'vam',
    'para': 'pra',
    'nova': 'nôva',
    'novas': 'nóvas',
    'novamente': 'nóvamenti',
    'otimo': 'ótimu',
    'ótimo': 'ótimu'
}

# Combined set of all verb roots
ALL_ROOTS = BASIC_VERB_ROOTS | ACTION_VERB_ROOTS | COGNITIVE_VERB_ROOTS | PROCESS_VERB_ROOTS


def remove_accents(text):
    """
    Remove all accents from text while preserving case.
    Uses Unicode normalization to handle both precomposed and combining characters.
    """
    # Normalize to NFD (decompose): e.g. "ê" => "e" + combining ^
    text = unicodedata.normalize('NFD', text)
    # Remove all combining marks in the range U+0300 to U+036F
    text = re.sub(r'[\u0300-\u036f]', '', text)
    # Re-normalize back to NFC for consistency
    return unicodedata.normalize('NFC', text)


def restore_accents(word, template):
    """
    Restore accents to a word based on a template word.
    For example:
        word = "que", template = "quê" -> returns "quê"
        word = "por que", template = "por quê" -> returns "por quê"
    """
    # If lengths don't match, can't restore accents
    if len(word) != len(template):
        return word

    # Convert both to NFD to separate base characters and combining marks
    template = unicodedata.normalize('NFD', template)
    word = unicodedata.normalize('NFD', word)

    # For each character in the word, if the template has an accent at that position,
    # add it to the word
    result = []
    i = 0
    while i < len(word):
        # Get base character from word
        result.append(word[i])

        # If template has combining marks after this position, add them
        j = i + 1
        while j < len(template) and unicodedata.combining(template[j]):
            result.append(template[j])
            j += 1

        i += 1
        # Skip any combining marks in word
        while i < len(word) and unicodedata.combining(word[i]):
            i += 1

    # Convert back to NFC (composed form)
    return unicodedata.normalize('NFC', ''.join(result))


def merge_word_pairs(tokens):
    """
    Merge only if two adjacent tokens are both words (no punctuation in between)
    and the exact pair (in lowercase) is in WORD_PAIRS.
    """
    new_tokens = []
    i = 0
    explanations = []  # Move explanations list up here
    while i < len(tokens):
        word1, punct1 = tokens[i]

        # If this token is punctuation, just keep it and move on
        if not word1:
            new_tokens.append((word1, punct1))
            i += 1
            continue

        # Check if there is a "next" token to form a pair
        if i + 1 < len(tokens):
            word2, punct2 = tokens[i + 1]

            # If the next token is actually punctuation, we cannot form a pair
            if not word2:
                # Keep the current token (word1)
                new_tokens.append((word1, punct1))
                i += 1
                continue

            # Build a pair string in lowercase
            pair = f"{word1.lower().strip()} {word2.lower().strip()}"

            # Try an exact match against WORD_PAIRS
            if pair in WORD_PAIRS:
                # If matched, create a single merged token
                replacement = WORD_PAIRS[pair]
                # Merge punctuation from both tokens
                merged_punct = punct1 + punct2
                # Add to new_tokens
                new_tokens.append((replacement, merged_punct))
                explanations.append(
                    f"Common pronunciation and usage: {pair} → {replacement}")
                # Skip the second token in the pair
                i += 2
            else:
                # No match, keep word1 as-is
                new_tokens.append((word1, punct1))
                i += 1
        else:
            # Last token, no pair to form
            new_tokens.append((word1, punct1))
            i += 1

    return new_tokens, explanations


def tokenize_text(text):
    """
    Capture words vs. punctuation lumps in a single pass.
    - ([A-Za-zÀ-ÖØ-öø-ÿ0-9]+): words (including accented or numeric characters).
    - ([.,!?;:]+): one or more punctuation marks.
    - (-): hyphens are captured separately to preserve them
    Returns a list of (word, punct) tuples, e.g.:
        "Olá, mundo!" => [("Olá", ""), ("", ","), ("mundo", ""), ("", "!")]
        "bem-vindo" => [("bem", ""), ("", "-"), ("vindo", "")]
    """
    pattern = r'([A-Za-zÀ-ÖØ-öø-ÿ0-9]+)|([.,!?;:]+)|(-)'
    tokens = []

    for match in re.finditer(pattern, text):
        word = match.group(1)
        punct = match.group(2)
        if word:
            tokens.append((word, ''))  # (word, "")
        elif punct:
            tokens.append(('', punct))  # ("", punctuation)

    return tokens


def reassemble_tokens_smartly(final_tokens):
    """
    Reassemble (word, punct) tokens into a single string without
    introducing extra spaces before punctuation.

    Example final_tokens could be: [("Olá", ""), ("", ","), ("mundo", ""), ("", "!")]
    We want to get: "Olá, mundo!"

    Example with hyphen: [("bem", ""), ("", "-"), ("vindo", "")]
    We want to get: "bem-vindo"

    Logic:
      - If 'word' is non-empty, append it to output (with a leading space if it's not the first).
      - If 'punct' is non-empty:
        - If it's a hyphen, append it directly (no leading space)
        - Otherwise, append it directly (no leading space).
      - Special case: if punctuation is a hyphen and followed by a word, don't add space after hyphen
    """
    output = []
    i = 0
    while i < len(final_tokens):
        word, punct = final_tokens[i]
        
        # If there's a word
        if word:
            if not output:
                # First token => add the word as is
                output.append(word)
            else:
                # Check if previous token was a hyphen
                prev_punct = final_tokens[i-1][1] if i > 0 else ""
                if prev_punct == "-":
                    # If previous token was a hyphen, don't add space
                    output.append(word)
                else:
                    # Not the first and not after hyphen => prepend space
                    output.append(" " + word)

        # If there's punctuation => attach immediately (no space)
        if punct:
            output.append(punct)
            
        i += 1

    # Join everything into a single string
    return "".join(output)


def transform_text(text):
    """
    1) Tokenize the input.
    2) Merge known word pairs from WORD_PAIRS before single-word phonetic rules.
    3) Apply single-word transformations (apply_phonetic_rules).
    4) Run multiple passes of inline combination rules (the big if/elif
       for 'r' + vowel, 'a' + vowel, 'sz' + vowel, etc.).
    5) Reassemble into the final text.
    """
    print("DEBUG: Input text =", repr(text))
    try:
        # ---------------------------------------------------------------------
        # 1) Normalize non-breaking spaces (optional)
        # ---------------------------------------------------------------------
        text = text.replace('\xa0', ' ')

        # ---------------------------------------------------------------------
        # 2) Tokenize
        # ---------------------------------------------------------------------
        tokens = tokenize_text(text)

        # ---------------------------------------------------------------------
        # 3) Merge word pairs first (e.g. "por que" -> "purkê")
        # ---------------------------------------------------------------------
        tokens, word_pair_explanations = merge_word_pairs(tokens)

        # ---------------------------------------------------------------------
        # 4) Apply single-word phonetic transformations to each token
        #    (including those merged into single tokens)
        # ---------------------------------------------------------------------
        transformed_tokens = []
        explanations = word_pair_explanations  # Start with word pair explanations
        for i, (word, punct) in enumerate(tokens):
            if word:
                next_word = tokens[i + 1][0] if (i + 1 < len(tokens)) else None
                next_next_word = tokens[i +
                                        2][0] if (i +
                                                  2 < len(tokens)) else None
                prev_word = tokens[i - 1][0] if (i - 1 >= 0) else None

                # Apply dictionary + phonetic rules to this single word
                new_word, explanation = apply_phonetic_rules(
                    word, next_word, next_next_word, prev_word)
                if explanation != "No changes needed":
                    explanations.append(f"{word}: {explanation}")

                transformed_tokens.append((new_word, punct))
            else:
                # This token is punctuation-only => just keep it
                transformed_tokens.append((word, punct))

        # ---------------------------------------------------------------------
        # Capture state after transformations but before combinations
        # ---------------------------------------------------------------------
        before_combinations = reassemble_tokens_smartly(transformed_tokens)

        # ---------------------------------------------------------------------
        # 5) Now apply inline combination rules in a loop until no more merges
        #    (the big if/elif checks for 'r'+vowel, 'a'+vowel, 'sz'+vowel, etc.)
        # ---------------------------------------------------------------------
        combination_explanations = []
        combinations = []  # Initialize combinations list
        made_combination = True  # Start as True to enter the loop

        while made_combination:
            made_combination = False  # Reset for this iteration
            new_tokens = []
            i = 0

            while i < len(transformed_tokens):
                if i < len(transformed_tokens) - 1:
                    word1, punct1 = transformed_tokens[i]
                    word2, punct2 = transformed_tokens[i + 1]

                    # Try to combine words using the combination rules
                    combined, rule_explanation = apply_combinations(word1, word2, punct1, punct2)
                    if combined is not None and rule_explanation is not None and not made_combination:

                            # If we found a combination to apply
                            if combined is not None and rule_explanation is not None:
                                print(
                                    f"DEBUG: Found combination: {rule_explanation}"
                                )
                                combination_explanations.append(
                                    rule_explanation)
                                new_tokens.append((combined, punct2))
                                i += 2
                                made_combination = True
                                continue

                # If no combination was applied, keep the current token and move on
                new_tokens.append(transformed_tokens[i])
                i += 1

            # Update tokens for next iteration
            if made_combination:
                transformed_tokens = new_tokens

        # ---------------------------------------------------------------------
        # 6) Reassemble the final text
        # ---------------------------------------------------------------------
        after_combinations = reassemble_tokens_smartly(transformed_tokens)

        return {
            'before': before_combinations,
            'after': after_combinations,
            'explanations': explanations,
            'combinations': combination_explanations
        }

    except Exception as e:
        print(f"Error in transform_text: {e}")
        traceback.print_exc()
        return {
            'before': text,
            'after': text,
            'explanations': [f"Error: {str(e)}"],
            'combinations': []
        }


def convert_text(text):
    """Convert Portuguese text to its phonetic representation with explanations."""
    result = transform_text(text)
    return result


def main():
    # Set UTF-8 encoding for stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Check if file is provided as a command-line argument
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            input_text = f.read()
    else:
        # If not, read from standard input
        print("Enter the text to convert (Ctrl+D to end):")
        input_text = sys.stdin.read()

    # Process each line separately
    lines = input_text.splitlines()
    if not lines:
        lines = ['']

    # Convert and display each line
    for line in lines:
        result = convert_text(line)
        print("Word Transformations:")
        print(result['before'])
        print(result['after'])
        for explanation in result['explanations']:
            print(explanation)
        print("\nWord Combinations:")
        for combination in result['combinations']:
            print(combination)
        print()


if __name__ == "__main__":
    main()