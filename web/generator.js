// Shared request builder for the website and tests. Mirrors tools/kosif.py `prompt`.
// Works in the browser (ES module) and in Node (node --test / plain import).
export const REPO_URL = 'https://github.com/kosif199022-jpg/kosif-tool';
export const RESOLUTIONS = { '9:16': '1080x1920', '16:9': '1920x1080', '1:1': '1080x1080', '4:5': '1080x1350' };
export const STACKS = {
  auto: { ar: 'اختر الأنسب للمادة (Remotion/React للتحرير القابل للتعديل، HTML Canvas أو SVG للرسوم الخفيفة، Three.js للمشاهد الفراغية الحقيقية)', en: 'choose the best fit for the material (Remotion/React for editable sequences, HTML Canvas or SVG for light vector motion, Three.js for true spatial scenes)' },
  remotion: { ar: 'Remotion/React (مشروع starters/remotion في المستودع)', en: 'Remotion/React (starters/remotion in the repository)' },
  canvas: { ar: 'HTML Canvas مع خط زمني حتمي (starters/html-canvas) والرندر عبر tools/render_html.cjs', en: 'HTML Canvas with a deterministic timeline (starters/html-canvas) rendered through tools/render_html.cjs' },
  svg: { ar: 'SVG + GSAP داخل صفحة HTML والرندر عبر tools/render_html.cjs في وضع virtual time', en: 'SVG + GSAP in an HTML page rendered through tools/render_html.cjs in virtual-time mode' },
  three: { ar: 'Three.js لمشهد ثلاثي الأبعاد حقيقي مع كاميرا متحركة', en: 'Three.js for a real 3D scene with a moving camera' },
};
export const SOURCES = {
  none: { ar: 'لا توجد مادة مرفقة — اكتب سردًا قصيرًا أصليًا وخطة مشاهد موقّتة', en: 'no material supplied — write a short original narration and a timestamped scene plan' },
  audio: { ar: 'ملف صوت مرفق: {detail} — هو المرجع الزمني الأساسي؛ فرّغه وزامن الحركة مع الكلمات', en: 'attached audio file: {detail} — it is the master clock; transcribe it and sync motion to the words' },
  video: { ar: 'ملف فيديو مرفق: {detail} — ادرس القطعات والحركة والكلام أولًا وحافظ على المادة المصرّح بها', en: 'attached video file: {detail} — study its cuts, movement and speech first and preserve the authorized material' },
  text: { ar: 'نص/سكريبت مرفق: {detail}', en: 'attached text/script: {detail}' },
};
export const AUDIO = {
  keep: { ar: 'احفظ الصوت المرفق كما هو دون أي تعديل في توقيته', en: 'keep the provided voice untouched, never alter its timing' },
  music: { ar: 'أضف موسيقى مرخّصة فقط مع خفضها تحت الصوت وتسليم بمستوى -14 LUFS', en: 'add licensed music only, ducked under the voice, delivered at -14 LUFS' },
  sfx: { ar: 'مؤثرات صوتية قصيرة فقط على اللحظات المفصلية', en: 'short sound effects only on key accents' },
  silent: { ar: 'بدون صوت', en: 'silent' },
};
export const LANGS = {
  ar: { ar: 'العربية فقط (RTL، خط عربي واضح)', en: 'Arabic only (RTL, a clear Arabic typeface)' },
  en: { ar: 'الإنجليزية فقط', en: 'English only' },
  both: { ar: 'العربية والإنجليزية معًا مع ضبط اتجاه كل سطر', en: 'Arabic and English together with correct direction per line' },
};

export function defaultsFor(record, brief) {
  const aspect = record && RESOLUTIONS[record.aspect_label] ? record.aspect_label : (brief && RESOLUTIONS[brief.aspect] ? brief.aspect : '9:16');
  const duration = (brief && brief.duration_s) || (record && record.duration_s) || 15;
  return { aspect, duration, fps: 30, stack: 'auto', source: 'none', audio: 'keep', lang: 'ar', reqLang: 'ar', brand: '', notes: '', detail: '' };
}

function fill(template, vars) {
  return template.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m));
}

/**
 * Build the Claude Code request text.
 * @param {object} p
 * @param {string} p.template - contents of templates/claude_request.<lang>.txt
 * @param {object} p.record - catalog record
 * @param {Array} p.categories - catalog/categories.json
 * @param {object} p.options - {reqLang, lang, source, detail, aspect, duration, fps, stack, brand, audio, notes}
 * @param {boolean} p.hasBrief
 */
export function buildRequest({ template, record, categories = [], options = {}, hasBrief = false }) {
  const L = options.reqLang === 'en' ? 'en' : 'ar';
  const catMap = Object.fromEntries(categories.map(c => [c.key, c]));
  const playbooks = (record.playbooks && record.playbooks.length)
    ? record.playbooks
    : (record.category || []).map(k => catMap[k] && catMap[k].playbook).filter(Boolean);
  const aspect = RESOLUTIONS[options.aspect] ? options.aspect : '9:16';
  const sourceKey = SOURCES[options.source] ? options.source : 'none';
  const detail = (options.detail || '').trim() || (L === 'ar' ? '(أرفق الملف)' : '(attach the file)');
  const vars = {
    repo: REPO_URL,
    id: record.id,
    name: record.name + (record.name_ar && record.name_ar !== record.name ? ' / ' + record.name_ar : ''),
    page: record.page,
    brief_line: hasBrief ? (L === 'ar' ? ` و styles/${record.id}/BRIEF.md` : ` and styles/${record.id}/BRIEF.md`) : '',
    playbooks: playbooks.length ? playbooks.join(L === 'ar' ? '، ' : ', ') : (L === 'ar' ? 'لا يوجد دليل فئة لهذا الاستايل' : 'no category playbook for this style'),
    source: SOURCES[sourceKey][L].replace('{detail}', detail),
    aspect,
    resolution: RESOLUTIONS[aspect],
    fps: String(options.fps || 30),
    duration: String(options.duration || 15),
    stack: (STACKS[options.stack] || STACKS.auto)[L],
    lang: (LANGS[options.lang] || LANGS.ar)[L],
    brand: (options.brand || '').trim() || (L === 'ar' ? 'لا توجد هوية محددة — اقترح نظام ألوان وخطوط أصليًا ووثّقه في STYLE.md' : 'no fixed brand — propose an original color and type system and document it in STYLE.md'),
    audio: (AUDIO[options.audio] || AUDIO.keep)[L],
    notes: (options.notes || '').trim() || (L === 'ar' ? 'لا شيء' : 'none'),
  };
  return fill(template, vars).trim() + '\n';
}

export function cliCommand(record, options = {}) {
  const parts = ['python3 tools/kosif.py prompt', record.id, '--lang', options.reqLang === 'en' ? 'en' : 'ar', '--aspect', options.aspect || '9:16', '--duration', String(options.duration || 15), '--fps', String(options.fps || 30), '--stack', options.stack || 'auto'];
  if (options.source && options.source !== 'none') parts.push('--source', JSON.stringify(`${options.source} ${options.detail || ''}`.trim()));
  if (options.audio) parts.push('--audio', options.audio);
  if (options.brand) parts.push('--brand', JSON.stringify(options.brand));
  if (options.notes) parts.push('--notes', JSON.stringify(options.notes));
  return parts.join(' ');
}
