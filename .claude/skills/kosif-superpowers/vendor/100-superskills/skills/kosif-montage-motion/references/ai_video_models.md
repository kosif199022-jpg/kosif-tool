# صياغة برومبتات نماذج الفيديو بالذكاء الاصطناعي — AI Video Model Prompts

دليل بناء الأوامر التوليدية لنماذج الفيديو الرائدة (Google Veo 2, OpenAI Sora, Kling 1.5, Runway Gen-3 Alpha, Luma Dream Machine).

---

## 1. التشريح السينمائي السباعي (7-Layer Anatomy)
للحصول على مشهد فائق الجودة متناسق، يجب أن يحتوي كل برومبت على الطبقات السبع التالية:
1. **Subject (الموضوع الرئيسي):** وصف فيزيائي دقيق للشخصية أو العنصر (بدون صفات غامضة مثل "رائع").
2. **Action & Motion (الحركة والزمن):** ما يفعله العنصر بدقة ومعدل سرعته.
3. **Environment & Atmosphere (البيئة والغلاف الجوي):** تفاصيل المكان، الغبار المعلق، المطر، الضباب الحجمي، الجزيئات.
4. **Lighting & Color (الإضاءة واللون):** نوع الإضاءة (Golden hour, Cyberpunk neon, 3-point studio)، وحرارة كلفن (3200K دافئ / 6500K نهاري).
5. **Camera & Lens (الكاميرا والعدسة):** حركة الكاميرا (Dolly-in, Orbit, Crane up, Tracking)، البعد البؤري (35mm Anamorphic, 85mm Portrait).
6. **Style & Texture (الأسلوب والملمس):** 35mm film stock, photorealistic, Unreal Engine 5 render, volumetric raytracing.
7. **Technical Parameters (المعاملات التقنية):** نسبة الأبعاد (9:16 أو 16:9)، معدل الإطارات (24fps / 60fps)، الدقة (4K).

---

## 2. قوالب المنصات المتخصصة

### Google Veo 2
> `Cinematic wide shot of [SUBJECT] performing [ACTION]. Volumetric light rays piercing through [ENVIRONMENT]. 35mm anamorphic lens, shallow depth of field, slow forward tracking camera movement, photorealistic, 4K, 24fps.`

### OpenAI Sora
> `Hyper-realistic close-up of [SUBJECT], detailed facial expressions, natural physics and cloth movement in [ENVIRONMENT]. Golden hour rim lighting, slow orbit camera move, cinema camera texture, subtle atmospheric dust particles.`

### Kling 1.5
> `[SUBJECT] in [ENVIRONMENT], cinematic composition, dynamic motion, dramatic chiaroscuro lighting, smooth dolly-in shot, high texture fidelity, 1080p, ultra-detailed.`

### Runway Gen-3 Alpha
> `Cinematic establishing shot: [CAMERA MOTION] showing [SUBJECT] in [ATMOSPHERE]. Volumetric fog, highly detailed PBR textures, soft warm key light, cool blue fill light.`
