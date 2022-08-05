from pathlib import Path

ROOT = Path(__file__).parents[2]
print(ROOT)
gettext_compact = False
locale_dirs = [str(ROOT/'locales/')]
language = 'zh_CN'