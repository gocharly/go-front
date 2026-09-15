#!/usr/bin/env python3
"""
scan_slop.py - Детерминированный линтер и сканер текстов на соответствие стандарту GO-FRONT.
Механически выявляет 25+ Hard Bans, паразитные типографические маркеры, декоративные эмодзи
и монотонность ритмики (monotonous cadence).
Игнорирует блоки кода (code fences ```), инлайн-код (`...`) и YAML-frontmatter.
"""

import sys
import re
import argparse
import json
from pathlib import Path

HARD_BANS = [
    (r"не\s+просто\b[^,.!?;:]*,\s*а\b", "HARD_BAN_01", "Не просто X, а Y -> назовите Y прямо без отрицания"),
    (r"не\s+только\b[^,.!?;:]*,\s*но\s+и\b", "HARD_BAN_02", "Не только X, но и Y -> упростите до перечисления или разбейте на фразы"),
    (r"\bв\s+современном\s+мире\b", "HARD_BAN_03", "В современном мире -> throat-clearing, удалите преамбулу"),
    (r"\bв\s+эпоху\s+[а-яёa-z0-9_-]+", "HARD_BAN_04", "В эпоху ... -> штамп, начните сразу с факта"),
    (r"\bстоит\s+(?:отметить|подчеркнуть|заметить)\b", "HARD_BAN_05", "Стоит отметить -> удалите вводную фразу"),
    (r"\bважно\s+(?:понимать|помнить|отметить)\b", "HARD_BAN_06", "Важно понимать -> паразитная преамбула, срежьте"),
    (r"\bданн(?:ый|ая|ое|ую|ого|ому|ой|ою)\b|\bв\s+данном\b|\bв\s+данных\s+(?:случаях|условиях|ситуациях)\b", "HARD_BAN_07", "Данный -> канцелярит, замените на 'этот' или опустите"),
    (r"\bявляется\b", "HARD_BAN_08", "Является -> паразитная связка (is/are), замените на глагол действия или тире"),
    (r"\bиграет\s+(?:важную|ключевую|решающую|заметную)\s+роль\b", "HARD_BAN_09", "Играет важную роль -> назовите конкретное действие и метрику"),
    (r"\bможно\s+с\s+уверенностью\s+сказать\b", "HARD_BAN_10", "Можно с уверенностью сказать -> сформулируйте тезис прямо"),
    (r"\b(?:подводя\s+итог[и]?|в\s+сухом\s+остатке|в\s+заключение)\b", "HARD_BAN_11", "Подводя итог / В заключение -> школьный шаблон, начните с факта"),
    (r"\b(?:погрузимся\s+в|давайте\s+взглянем|давайте\s+разберемся|взглянем\s+поближе)\b", "HARD_BAN_12", "Чатботовский зачин -> перейдите сразу к сути"),
    (r"\b(?:раскрыть\s+потенциал|выйти\s+на\s+(?:качественно\s+)?новый\s+уровень)\b", "HARD_BAN_13", "Корпоративный булшит -> укажите оцифрованный результат"),
    (r"\bкомплексн(?:ый|ое|ая|ые)\s+(?:подход|решение|проблема)\b", "HARD_BAN_14", "Комплексный подход/решение -> перечислите состав по пунктам"),
    (r"\b(?:в\s+связи\s+с\s+этим|вследствие\s+этого)\b", "HARD_BAN_15", "В связи с этим -> замените на 'Поэтому' или разбейте мысль"),
    (r"\bни\s+для\s+кого\s+не\s+секрет\b", "HARD_BAN_16", "Ни для кого не секрет -> пустой зачин, удалите"),
    (r"\bключевой\s+вывод\s+заключается\b", "HARD_BAN_17", "Ключевой вывод заключается -> напишите вывод без маркировки"),
    (r"\b(?:и\s+это\s+нормально|вы\s+не\s+одн[иао]|вы\s+имеете\s+право\s+чувствовать)\b", "HARD_BAN_18", "Псевдо-терапия -> вырежьте поглаживания"),
    (r"\bдавайте\s+будем\s+честны\b", "HARD_BAN_19", "Давайте будем честны -> ложная драматургия, удалите"),
    (r"\bширокий\s+спектр\s+возможностей\b", "HARD_BAN_20", "Широкий спектр -> назовите конкретные возможности"),
    (r"\bнадеюсь,?\s*(?:эта\s+)?статья\s+была\s+полезна\b", "HARD_BAN_21", "Финальный сервильный подхалимаж -> удалите"),
    (r"\b(?:на\s+самом\s+деле|правда\s+в\s+том)\b", "HARD_BAN_22", "На самом деле / Правда в том -> ложная интрига"),
    (r"\b(?:своего\s+рода|в\s+некотором\s+смысле)\b", "HARD_BAN_23", "Хеджирование / размытие ответственности -> утверждайте твердо"),
    (r"\b(?:забегая\s+вперед|как\s+мы\s+увидим\s+позже)\b", "HARD_BAN_24", "Паразитный анонс -> излагайте мысли в естественном порядке"),
    (r"\bне\s+потому\s+что\b[^,.!?;:]*,\s*а\s+потому\s+что\b", "HARD_BAN_25", "Не потому что X, а потому что Y -> сразу утвердите Y"),
    (r"\bдело\s+не\s+в\b[^,.!?;:]*,\s*а\s+в\b", "HARD_BAN_26", "Дело не в X, а в Y -> срежьте X, оставьте Y"),
    (r"\bвопрос\s+не\s+в\s+том\b[^,.!?;:]*,\s*вопрос\s+в\b", "HARD_BAN_27", "Вопрос не в X, вопрос в Y -> сформулируйте главный вопрос"),
    (r"\bчто,?\s*если\s+я\s+скажу\s+вам\b", "HARD_BAN_28", "Что если я скажу вам -> поза коуча, удалите"),
    (r"\bподумайте\s+об\s+этом\b", "HARD_BAN_29", "Подумайте об этом -> высокомерное поучение, удалите"),
    (r"\bвот\s+что\s+я\s+имею\s+в\s+виду\b", "HARD_BAN_30", "Вот что я имею в виду -> лишняя прокладка перед тезисом"),
]

EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff"
    r"\u2600-\u26ff"
    r"\u2700-\u27bf"
    r"\u2300-\u23ff"
    r"\u2b50\u2b55\u231a\u231b\u2934\u2935\u25aa\u25ab\u25fe\u25fd]"
)

EM_DASH_PATTERN = re.compile(r"(?<!\d)—(?!\d)")
CHEVRON_QUOTES_PATTERN = re.compile(r"[«»]")
INLINE_CODE_PATTERN = re.compile(r"`[^`]+`")


def mask_inline_code(text):
    """Маскирует инлайн-код пробелами одинаковой длины, чтобы сохранить индексы символов."""
    def replacer(match):
        return " " * len(match.group(0))
    return INLINE_CODE_PATTERN.sub(replacer, text)


def is_in_frontmatter_or_code(lines, line_idx):
    """Определяет, находится ли строка внутри markdown frontmatter (---) или code-fence (```)."""
    # Frontmatter check
    if lines and lines[0].strip() == "---":
        closing_fm = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                closing_fm = i
                break
        if closing_fm != -1 and line_idx <= closing_fm:
            return True

    # Code fences check
    in_code = False
    for i in range(line_idx + 1):
        if lines[i].strip().startswith("```"):
            in_code = not in_code
    return in_code


def check_rhythm(text):
    clean_lines = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.strip().startswith(("#", "-", "*", ">", "|")):
            continue
        clean_lines.append(line)
    
    clean_text = " ".join(clean_lines)
    sentences = re.split(r"(?<=[.!?])\s+", clean_text.strip())
    clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
    if len(clean_sentences) < 4:
        return []

    violations = []
    consecutive_medium = 0
    start_idx = 0

    for idx, s in enumerate(clean_sentences):
        words = len(re.findall(r"\b[а-яёa-z0-9_-]+\b", s, flags=re.IGNORECASE))
        if 11 <= words <= 26:
            if consecutive_medium == 0:
                start_idx = idx
            consecutive_medium += 1
            if consecutive_medium >= 4:
                sample = clean_sentences[start_idx][:35] + "..."
                violations.append({
                    "rule": "MONOTONOUS_CADENCE",
                    "line": 0,
                    "snippet": f"4+ предложения подряд длиной 11-26 слов (начало: {sample})",
                    "fix": "Разбейте монотонный ритм короткой рубленой добивкой (1-4 слова)"
                })
                consecutive_medium = 0
        else:
            consecutive_medium = 0

    return violations


def audit_text(text):
    lines = text.splitlines()
    violations = []
    
    for line_idx, raw_line in enumerate(lines, start=1):
        if is_in_frontmatter_or_code(lines, line_idx - 1):
            continue
        
        # Маскируем инлайн-код перед поиском слопа
        scannable_line = mask_inline_code(raw_line)

        # Заголовки
        if raw_line.strip().startswith("#"):
            if re.search(r"^#+\s+[^:\n]+:\s+как\s+мы\b", scannable_line, re.IGNORECASE):
                violations.append({
                    "rule": "SLOP_HEADER_COLON",
                    "line": line_idx,
                    "snippet": raw_line.strip(),
                    "fix": "Заголовок с двоеточием вида 'X: как мы сделали Y' -> перепишите естественно"
                })

        # Hard bans
        for pattern, rule_id, fix_hint in HARD_BANS:
            matches = list(re.finditer(pattern, scannable_line, flags=re.IGNORECASE))
            for m in matches:
                violations.append({
                    "rule": rule_id,
                    "line": line_idx,
                    "snippet": raw_line[m.start():m.end()],
                    "fix": fix_hint
                })

        # Эмодзи
        for m in EMOJI_PATTERN.finditer(scannable_line):
            violations.append({
                "rule": "DECORATIVE_EMOJI",
                "line": line_idx,
                "snippet": m.group(0),
                "fix": "Удалите декоративный эмодзи (стандарт Zero-Emoji)"
            })

        # Длинное тире
        for m in EM_DASH_PATTERN.finditer(scannable_line):
            violations.append({
                "rule": "TYPOGRAPHY_EM_DASH",
                "line": line_idx,
                "snippet": "—",
                "fix": "Замените длинное тире '—' на дефис '-' с пробелами или запятую"
            })

        # Кавычки-елочки
        for m in CHEVRON_QUOTES_PATTERN.finditer(scannable_line):
            violations.append({
                "rule": "TYPOGRAPHY_CHEVRON",
                "line": line_idx,
                "snippet": m.group(0),
                "fix": "Замените кавычки « » на прямые кавычки \" \""
            })

    rhythm_violations = check_rhythm(text)
    violations.extend(rhythm_violations)

    penalty = 0
    for v in violations:
        rule = v["rule"]
        if rule.startswith("HARD_BAN"):
            penalty += 12
        elif rule == "DECORATIVE_EMOJI":
            penalty += 5
        elif rule == "MONOTONOUS_CADENCE":
            penalty += 10
        elif rule.startswith("TYPOGRAPHY"):
            penalty += 2
        else:
            penalty += 5

    score = max(0, 100 - penalty)
    return {
        "score": score,
        "violations": violations,
        "total_violations": len(violations)
    }


def auto_fix(text):
    lines = text.splitlines()
    fixed_lines = []
    
    for line_idx, line in enumerate(lines):
        if is_in_frontmatter_or_code(lines, line_idx):
            fixed_lines.append(line)
            continue
        
        parts = []
        last_end = 0
        for m in INLINE_CODE_PATTERN.finditer(line):
            segment = line[last_end:m.start()]
            segment = EMOJI_PATTERN.sub("", segment)
            segment = segment.replace("«", '"').replace("»", '"')
            segment = EM_DASH_PATTERN.sub("-", segment)
            parts.append(segment)
            parts.append(m.group(0))
            last_end = m.end()
        
        remaining = line[last_end:]
        remaining = EMOJI_PATTERN.sub("", remaining)
        remaining = remaining.replace("«", '"').replace("»", '"')
        remaining = EM_DASH_PATTERN.sub("-", remaining)
        parts.append(remaining)
        fixed_lines.append("".join(parts))

    return "\n".join(fixed_lines)


def main():
    parser = argparse.ArgumentParser(description="GO-FRONT Slop Scanner & Linter")
    parser.add_argument("paths", nargs="*", help="Файлы или директории для проверки")
    parser.add_argument("--fix", action="store_true", help="Автоматически исправить тривиальные маркеры (тире, кавычки, эмодзи)")
    parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")
    parser.add_argument("--strict", action="store_true", help="Возвращать ошибку (exit 1), если скор ниже 100")
    args = parser.parse_args()

    files = []
    if not args.paths or "-" in args.paths:
        text = sys.stdin.read()
        res = audit_text(text)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print_report("stdin", res)
        if args.fix:
            fixed = auto_fix(text)
            sys.stdout.write(fixed)
        sys.exit(1 if (args.strict and res["score"] < 100) else 0)

    for p_str in args.paths:
        p = Path(p_str)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for ext in ("*.md", "*.txt", "*.html"):
                files.extend(p.rglob(ext))

    overall_failed = False
    all_results = {}

    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        if args.fix:
            new_content = auto_fix(content)
            if new_content != content:
                f.write_text(new_content, encoding="utf-8")
                content = new_content
        
        res = audit_text(content)
        all_results[str(f)] = res
        if res["score"] < 100:
            overall_failed = True
        
        if not args.json:
            print_report(str(f), res)

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))

    sys.exit(1 if (args.strict and overall_failed) else 0)


def print_report(source_name, res):
    score = res["score"]
    violations = res["violations"]
    print(f"\n[GO-FRONT AUDIT] {source_name}")
    print(f"Чистота текста: {score}/100 | Нарушений найдено: {len(violations)}")
    if not violations:
        print("Статус: ЧИСТО (100% соблюдение GO-FRONT)")
        return

    print("-" * 60)
    for v in violations:
        line_info = f"Строка {v['line']}:" if v['line'] > 0 else "Ритмика:"
        print(f"  * {line_info} [{v['rule']}] -> \"{v['snippet']}\"")
        print(f"    Действие: {v['fix']}")
    print("-" * 60)


if __name__ == "__main__":
    main()
