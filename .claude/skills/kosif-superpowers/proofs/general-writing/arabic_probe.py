#!/usr/bin/env python3
"""Arabic language-processing probe: what works on THIS machine, with real outputs.

Each check prints PASS, SKIP (library or binary missing; the install command is shown) or FAIL.
Optional libraries are imported only if present; nothing is installed and nothing outside a temp
dir is written. Run it with the interpreter that has the libraries you want to test, e.g.
  python3 -I proofs/general-writing/arabic_probe.py
  /path/to/venv/bin/python -I proofs/general-writing/arabic_probe.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1]
sys.dont_write_bytecode = True          # leave no __pycache__ inside the skill
sys.path.insert(0, str(SKILL / 'scripts'))
import anchor_gate  # noqa: E402
import tell_scan    # noqa: E402

FONTS = SKILL / 'proofs' / '_shared' / 'fonts'
results = []


def report(name, status, detail):
    results.append(status)
    print(f'{status:4}  {name:34} {detail}')


def check(name, fn, install=''):
    try:
        out = fn()
        report(name, 'PASS', out)
    except ImportError as e:
        report(name, 'SKIP', f'{e.name} not installed' + (f' -> {install}' if install else ''))
    except Exception as e:  # noqa: BLE001 - a probe reports every failure instead of stopping
        report(name, 'FAIL', f'{type(e).__name__}: {e}')


def normalization():
    a, b = tell_scan.norm_ar('ختامًا إلى مُستشفى المدينةِ'), tell_scan.norm_ar('ختاما الى مستشفي المدينه')
    assert a == b, (a, b)
    return f'"ختامًا إلى مُستشفى المدينةِ" -> "{a}" (equals the bare spelling)'


def original_spelling():
    r = tell_scan.scan('وفي الختامِ، تُعزّز الأداةُ التجربةَ.')
    shown = [h['match'] for h in r['hits']]
    assert 'وفي الختامِ' in shown and 'تُعزّز' in shown, shown
    return f'matched on normalized text, shown as {shown}'


def clitic_numbers():
    c = anchor_gate.anchors('افتتحنا و٥ مكاتب بـ١٠٠ ألف سنة ٢٠٢٤م بنسبة ٪١٥')
    nums = sorted(v for (k, v), n in c.items() if k == 'number')
    assert nums == ['100', '15%', '2024', '5'], nums
    return f'و٥ / بـ١٠٠ / ٢٠٢٤م / ٪١٥ -> {nums}'


def raqm():
    from PIL import features, Image, ImageDraw, ImageFont
    assert features.check('raqm'), 'Pillow built without RAQM: use arabic-reshaper + python-bidi instead'
    f = ImageFont.truetype(str(FONTS / 'Amiri-Regular.ttf'), 48, layout_engine=ImageFont.Layout.RAQM)
    w = ImageDraw.Draw(Image.new('L', (10, 10))).textlength('سلام', font=f, direction='rtl')
    return f'Pillow RAQM on; Amiri shaped "سلام" width {w:.0f}px from raw logical text'


def reshaper_bidi():
    import arabic_reshaper
    from bidi import get_display
    shaped = arabic_reshaper.reshape('سلام 2024')
    vis = get_display(shaped)
    assert ord(shaped[0]) >= 0xFE70, 'no presentation forms'
    return f'reshape -> {[hex(ord(c)) for c in shaped[:4]]}, visual order "{vis}" (only for renderers that do not shape)'


def camel_utils():
    from camel_tools.utils.charmap import CharMapper
    from camel_tools.utils.dediac import dediac_ar
    from camel_tools.utils.normalize import normalize_alef_ar
    s = 'مُحَمَّدٌ يَقْرَأُ القُرْآنَ'
    bw = CharMapper.builtin_mapper('ar2bw')(s)
    back = CharMapper.builtin_mapper('bw2ar')(bw)
    assert back == s
    return f'ar2bw "{bw}" (round trip exact); dediac "{dediac_ar(s)}"; alef "{normalize_alef_ar("أحمد إبراهيم")}"'


def pyarabic_check():
    import pyarabic.araby as araby
    toks = araby.tokenize('قال: «لن نتراجع»، ثم مضى.')
    return f'strip_tashkeel "{araby.strip_tashkeel("مُحَمَّدٌ")}", strip_tatweel "{araby.strip_tatweel("عـــربي")}", tokenize {toks}'


def mojibake():
    garbled = 'سلام عليكم'.encode('utf-8').decode('cp1252')
    fixed = garbled.encode('cp1252').decode('utf-8')
    legacy = 'سلام'.encode('cp1256')
    try:
        legacy.decode('utf-8')
        raise AssertionError('cp1256 bytes decoded as UTF-8')
    except UnicodeDecodeError:
        legacy_fixed = legacy.decode('cp1256')
    assert fixed == 'سلام عليكم' and legacy_fixed == 'سلام'
    return f'"{garbled}" -> "{fixed}"; cp1256 bytes {legacy.hex()} -> "{legacy_fixed}"'


def fonts():
    have = sorted(p.name for p in FONTS.glob('*.tt[fc]')) if FONTS.is_dir() else []
    sysar = ''
    if shutil.which('fc-list'):
        out = subprocess.run(['fc-list', ':lang=ar', 'family'], capture_output=True, text=True, timeout=20).stdout
        fams = sorted({x.strip() for ln in out.splitlines() for x in ln.split(',') if x.strip()})
        sysar = f'; system families covering Arabic (fc-list :lang=ar): {", ".join(fams) or "none"}'
    assert have, 'no bundled fonts'
    return f'bundled (OFL): {", ".join(have)}{sysar}'


def ocr():
    if not shutil.which('tesseract'):
        raise ImportError(name='tesseract (binary)')
    langs = subprocess.run(['tesseract', '--list-langs'], capture_output=True, text=True).stdout.split()
    if 'ara' not in langs:
        raise ImportError(name='tesseract-ocr-ara (language data)')
    from PIL import Image, ImageDraw, ImageFont
    truth = 'ارتفعت المبيعات بنسبة ٢٥٪ في عام ٢٠٢٤\nوتواصل معنا يوم الخميس ١٢ مارس'
    f = ImageFont.truetype(str(FONTS / 'Cairo[slnt,wght].ttf'), 56, layout_engine=ImageFont.Layout.RAQM)
    with tempfile.TemporaryDirectory() as td:
        im = Image.new('L', (1400, 260), 255)
        d = ImageDraw.Draw(im)
        for i, line in enumerate(truth.splitlines()):
            d.text((1360, 30 + i * 110), line, font=f, fill=0, anchor='ra', direction='rtl')
        png = Path(td) / 'ar.png'
        im.save(png)
        text = subprocess.run(['tesseract', str(png), '-', '-l', 'ara', '--psm', '6'],
                              capture_output=True, text=True, timeout=120).stdout.strip()
    gate = anchor_gate.compare(truth, text)
    words_ok = all(w in text for w in ('ارتفعت', 'المبيعات', 'مارس'))
    assert words_ok, text
    drops = [(x['kind'], x['value']) for x in gate['dropped']]
    return f'OCR "{" | ".join(text.splitlines())}"; words read; anchor gate {gate["status"]} dropped {drops}'


print(f'python {sys.version.split()[0]} at {sys.executable}')
check('normalize for matching', normalization)
check('report in original spelling', original_spelling)
check('numbers glued to clitics', clitic_numbers)
check('Pillow RAQM shaping', raqm, 'pip install pillow')
check('arabic-reshaper + python-bidi', reshaper_bidi, 'pip install arabic-reshaper python-bidi')
check('camel-tools utils (no models)', camel_utils, 'pip install --no-deps camel-tools emoji')
check('pyarabic (GPL)', pyarabic_check, 'pip install pyarabic')
check('mojibake repair', mojibake)
check('Arabic fonts', fonts)
check('tesseract Arabic OCR', ocr, 'apt-get install -y tesseract-ocr tesseract-ocr-ara')
print(f"\n{results.count('PASS')} pass, {results.count('SKIP')} skip, {results.count('FAIL')} fail")
sys.exit(1 if 'FAIL' in results else 0)
