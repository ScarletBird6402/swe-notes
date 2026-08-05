#!/usr/bin/env python3
"""기게시 HTML의 flow/pre 가운데 정렬 → 왼쪽 정렬 일괄 정정 (2026-08-03 규칙)
사용: 리포 루트에서  python fix_diagram_align.py           # dry-run
                    python fix_diagram_align.py --apply    # 적용
치환: <style> 안의 .flow / pre 셀렉터 규칙에서 text-align: center → left
      (본문 다른 요소의 center — 표 캡션·헤더 등 — 는 건드리지 않음)
"""
import re, sys
from pathlib import Path

APPLY = '--apply' in sys.argv
hits_total = 0
for f in sorted(Path('.').rglob('*.html')):
    if f.name == 'index.html': continue
    t = f.read_text(encoding='utf-8')
    def sub_css(m):
        css = m.group(1)
        pat = re.compile(r'((?:\.flow|pre)[^{}]*\{[^}]*?)text-align:\s*center', re.S)
        return m.group(0).replace(css, pat.sub(r'\1text-align: left', css))
    new = re.sub(r'<style[^>]*>(.*?)</style>', sub_css, t, flags=re.S)
    if new != t:
        n = len(re.findall(r'(?:\.flow|pre)[^{}]*\{[^}]*text-align:\s*center', t, re.S))
        hits_total += n
        print(f"[{'FIX' if APPLY else 'DRY'}] {f} — {n}건")
        if APPLY: f.write_text(new, encoding='utf-8')
print(f"\n{'적용' if APPLY else '검출(미적용)'}: 총 {hits_total}건", "" if APPLY else "→ 적용: --apply")
