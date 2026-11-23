import re

VOWELS = "аеиоуыэюя"

_rv_pattern = re.compile(f"[{VOWELS}]")
_r1_pattern = re.compile(f"[{VOWELS}][^{VOWELS}]")

PERFECTIVE_GERUND = re.compile(r"(((?P<keep>[ая])(в|вши|вшись))|(ив|ивши|ившись|ыв|ывши|ывшись))$")
REFLEXIVE = re.compile(r"(ся|сь)$")
ADJECTIVE = re.compile(
    r"(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$"
)
PARTICIPLE = re.compile(r"(((?P<keep>[ая])(ем|нн|вш|ющ|щ))|(ивш|ывш|ующ))$")
VERB = re.compile(
    r"(((?P<keep>[ая])(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно))|"
    r"(ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|ят|ует|уют|"
    r"ит|ыт|ены|ить|ыть|ишь|ую|ю))$"
)
NOUN = re.compile(
    r"(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|"
    r"ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$"
)
SUPERLATIVE = re.compile(r"(ейш|ейше)$")
DERIVATIONAL = re.compile(r"(ост|ость)$")
I_ENDING = re.compile(r"и$")
DOUBLE_N = re.compile(r"((?<=н)н)$")
SOFT_SIGN = re.compile(r"ь$")


def _find_rv(word):
    match = _rv_pattern.search(word)
    return match.end() if match else len(word)


def _find_r2(word):
    r1 = _r1_pattern.search(word)
    if not r1:
        return len(word)
    r2 = _r1_pattern.search(word, r1.end())
    return r2.end() if r2 else len(word)


def _cut(word, pattern, pos):
    match = pattern.search(word, pos)
    if not match:
        return None, word
    try:
        keep = match.group("keep") or ""
    except IndexError:
        keep = ""
    return match.group()[len(keep):], word[: match.start() + len(keep)]


def stem(word, trace=None):
    word = word.lower().replace("ё", "е")
    rv_pos = _find_rv(word)
    r2_pos = _find_r2(word)

    def log(message):
        if trace is not None:
            trace.append(message)

    log(f"RV (область после первой гласной): «{word[rv_pos:]}»")

    removed, word = _cut(word, PERFECTIVE_GERUND, rv_pos)
    if removed is not None:
        log(f"Шаг 1: деепричастный суффикс «{removed}» → {word}")
    else:
        removed, word = _cut(word, REFLEXIVE, rv_pos)
        if removed is not None:
            log(f"Шаг 1: возвратный суффикс «{removed}» → {word}")
        removed, word = _cut(word, ADJECTIVE, rv_pos)
        if removed is not None:
            log(f"Шаг 1: окончание прилагательного «{removed}» → {word}")
            removed, word = _cut(word, PARTICIPLE, rv_pos)
            if removed is not None:
                log(f"Шаг 1: причастный суффикс «{removed}» → {word}")
        else:
            removed, word = _cut(word, VERB, rv_pos)
            if removed is not None:
                log(f"Шаг 1: глагольное окончание «{removed}» → {word}")
            else:
                removed, word = _cut(word, NOUN, rv_pos)
                if removed is not None:
                    log(f"Шаг 1: существительное окончание «{removed}» → {word}")

    removed, word = _cut(word, I_ENDING, rv_pos)
    if removed is not None:
        log(f"Шаг 2: конечная «и» → {word}")

    removed, word = _cut(word, DERIVATIONAL, r2_pos)
    if removed is not None:
        log(f"Шаг 3: деривационный суффикс «{removed}» → {word}")

    removed, word = _cut(word, SUPERLATIVE, rv_pos)
    if removed is not None:
        log(f"Шаг 4: превосходная степень «{removed}» → {word}")
    removed, word = _cut(word, DOUBLE_N, rv_pos)
    if removed is not None:
        log("Шаг 4: удвоенная «нн» → " + word)
    else:
        removed, word = _cut(word, SOFT_SIGN, rv_pos)
        if removed is not None:
            log(f"Шаг 4: мягкий знак → {word}")

    log(f"Основа: «{word}»")
    return word
