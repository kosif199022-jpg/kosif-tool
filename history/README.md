# سجل المهام / Task history

ذاكرة المهام المنجزة على GitHub: كل مهمة ينهيها مساعد يتبع USIP (فيديو، صورة، كود، مستند...) تُسجَّل هنا في ملف واحد، حتى تسأل لاحقًا «إيه المهام اللي عملتها؟» وتختار واحدة وتقول «كررها» فتصل إلى النتيجة نفسها. القواعد كاملة في [A35](../.claude/skills/kosif-superpowers/references/protocol/A35-task-history.md).

A memory of finished tasks, on GitHub: one JSON file per task under `tasks/`, so a later chat can list what was done, pick one and repeat it with the same tools, parameters and inputs.

## الملفات / files

| الملف | ما فيه |
|---|---|
| `tasks/<YYYYMMDD>-<name>.json` | سجل مهمة واحدة (المخطط `kosif.task-history.v1`): الطلب بكلماتك، والوضع والخطة، والأدوات والأوامر بمعاملاتها، والمدخلات والمخرجات ببصمة sha256، وطريقة الإعادة، والأدلة والدروس |
| `INDEX.md` | جدول كل المهام، الأحدث أولًا (مولَّد) |
| `index.json` | الجدول نفسه للآلات (مولَّد) |

## الأوامر / commands (from the repo root)

```bash
python3 .claude/skills/kosif-superpowers/scripts/task_history.py list                 # المهام، الأحدث أولًا
python3 .claude/skills/kosif-superpowers/scripts/task_history.py show 3               # المهمة رقم 3 بالتفصيل (أو بالمعرّف)
python3 .claude/skills/kosif-superpowers/scripts/task_history.py replay <id>          # خطة الإعادة؛ --format sh سكربت، ولا يشغّل شيئًا
python3 .claude/skills/kosif-superpowers/scripts/task_history.py compare <id>         # هل المخرجات الجديدة هي نفسها؟
python3 .claude/skills/kosif-superpowers/scripts/task_history.py new --kind video     # قالب سجل جديد
python3 .claude/skills/kosif-superpowers/scripts/task_history.py add --from entry.json            # يتحقق ويحسب البصمات ويكتب ويحدّث الفهرس
python3 .claude/skills/kosif-superpowers/scripts/task_history.py add --from entry.json --print    # بلا كتابة: السجل وأمر حفظ في سطر ورابط GitHub
```

## ما لا يدخل السجل / never recorded

هذا الفرع عام: يرفض `add` و`validate` أي سجل فيه مفتاح أو كلمة مرور، أو مسار جلسة أو scratchpad أو رفع خاص، أو بريد إلكتروني، أو رقم هاتف. الملفات الكبيرة والخاصة لا تُرفع؛ يُكتب مسارها أو رابطها العام مع بصمتها فقط.

This branch is public: a record with a credential, a session or upload path, an e-mail address or a phone number is refused. Large or private media are not committed; the record keeps a path or a public link and the file's sha256.
