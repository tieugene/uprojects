#!/usr/bin/env python3
"""Тестовое заданьице imot.io
Limitation:
- fix dict cannot have keys with same 1st word
- destination phrase not split into words (due timecodes abscense)
"""

import json
import sys
import pprint


def mk_fix_lens(fix: dict) -> dict[str, int]:
    """'Index' fixes lengths:
    'src1': 'res' -> 'src1': 1
    'src2 src3': 'res' -> 'src2': 2
    :param fix: fixes
    :return: dict of fixes lengths
    """
    retvalue = {}
    for k in fix.keys():
        k_list = k.split()
        retvalue[k_list[0]] = len(k_list)
    return retvalue


def fix_function(stt: list[dict], fix: dict) -> list[dict]:
    """Fix stt with fix.
    :param stt: dict to fix
    :param fix: fixes
    :return: fixed dic
    """
    fix_lens = mk_fix_lens(fix)
    result = []
    skip = 0
    for i, item in enumerate(stt):
        if skip:
            skip -= 1
            continue
        if _len := fix_lens.get(item['word']):
            phrase = ' '.join(w['word'] for w in stt[i:i + _len])
            if found := fix.get(phrase):
                result.append({
                    'word': found,
                    'start': item['start'],
                    'end': stt[i + _len - 1]['end']
                })
                skip = _len - 1
                continue
        result.append(item)
    return result


def main():
    """Main function (CLI)"""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <st_file.json> <fix_file.json", file=sys.stderr)
    else:
        with open(sys.argv[1], 'rt') as f_stt, open(sys.argv[2], 'rt') as f_fix:
            pprint.pprint(fix_function(json.load(f_stt), json.load(f_fix)))


if __name__ == '__main__':
    main()
