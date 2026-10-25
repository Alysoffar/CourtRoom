    // 1. WEB AUDIO SYNTHESIZER (Zero-Dependency Game SFX: Gavel, Objection, Blips)
    // ============================================================================
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playSFX(type) {
      if (!document.getElementById('sfx-toggle')?.checked) return;
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const now = audioCtx.currentTime;

      if (type === 'blip') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(520 + Math.random() * 180, now);
        gain.gain.setValueAtTime(0.025, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.045);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.045);
      } else if (type === 'gavel') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.exponentialRampToValueAtTime(38, now + 0.22);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.25);
      } else if (type === 'objection') {
        [440, 554.37, 659.25].forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'square';
          osc.frequency.setValueAtTime(freq, now + idx * 0.04);
          gain.gain.setValueAtTime(0.06, now + idx * 0.04);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now + idx * 0.04); osc.stop(now + 0.35);
        });
      }
    }

    // ============================================================================
    // 2. THREE.JS 3D COURTROOM SCENE & CHIBI CHARACTER BUILDER
    // ============================================================================
    const canvas = document.getElementById('webgl-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0b0c12);
    scene.fog = new THREE.FogExp2(0x0b0c12, 0.028);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
    const camPosTarget = new THREE.Vector3(0, 5.2, 13.5);
    const camLookTarget = new THREE.Vector3(0, 2.0, 0);
    const currentLook = new THREE.Vector3(0, 2.0, 0);
    camera.position.copy(camPosTarget);

    // Ambient + Dramatic Courtroom Lighting
    const ambientLight = new THREE.AmbientLight(0xd8c8b8, 0.55);
    scene.add(ambientLight);

    const mainDirLight = new THREE.DirectionalLight(0xffe6ba, 0.75);
    mainDirLight.position.set(6, 14, 10);
    mainDirLight.castShadow = true;
    scene.add(mainDirLight);

    function createSpotlight(color, x, z) {
      const spot = new THREE.SpotLight(color, 0.3, 25, Math.PI / 6, 0.45, 1.5);
      spot.position.set(x, 11, z + 2);
      spot.target.position.set(x, 0, z);
      spot.castShadow = true;
      scene.add(spot);
      scene.add(spot.target);
      return spot;
    }

    const spotPros = createSpotlight(0xff4b5c, -5.2, 1.2);
    const spotJury = createSpotlight(0xf5c869, 0, -3.5);
    const spotDef  = createSpotlight(0x38b6ff, 5.2, 1.2);

    // Courtroom Floor & Carpet
    const floorGeo = new THREE.PlaneGeometry(36, 28);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x1e1612, roughness: 0.4, metalness: 0.1 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    // Royal Red Runner Carpet
    const carpetGeo = new THREE.PlaneGeometry(5.5, 16);
    const carpetMat = new THREE.MeshStandardMaterial({ color: 0x5c131d, roughness: 0.8 });
    const carpet = new THREE.Mesh(carpetGeo, carpetMat);
    carpet.rotation.x = -Math.PI / 2;
    carpet.position.set(0, 0.01, 2);
    carpet.receiveShadow = true;
    scene.add(carpet);

    // Back Wood-Paneled Wall & Gold Pillars
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x261911, roughness: 0.7 });
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(32, 14, 0.6), wallMat);
    backWall.position.set(0, 7, -7);
    backWall.receiveShadow = true;
    scene.add(backWall);

    const goldMat = new THREE.MeshStandardMaterial({ color: 0xd8ad60, metalness: 0.7, roughness: 0.25 });
    for (let x of [-11, -5.5, 5.5, 11]) {
      const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 14, 16), goldMat);
      pillar.position.set(x, 7, -6.5);
      pillar.castShadow = true;
      scene.add(pillar);
    }

    // Golden Seal Behind Supreme Jury
    const sealRing = new THREE.Mesh(new THREE.TorusGeometry(1.4, 0.12, 16, 48), goldMat);
    sealRing.position.set(0, 6.6, -6.6);
    scene.add(sealRing);

    // Wooden Podium / Bench Builder
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x59371c, roughness: 0.55 });
    const darkWoodMat = new THREE.MeshStandardMaterial({ color: 0x361f0d, roughness: 0.65 });

    function createBench(w, h, d, x, y, z, rotY = 0) {
      const group = new THREE.Group();
      const base = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), woodMat);
      base.position.y = h / 2;
      base.castShadow = true;
      base.receiveShadow = true;
      group.add(base);

      const topTrim = new THREE.Mesh(new THREE.BoxGeometry(w + 0.25, 0.18, d + 0.25), goldMat);
      topTrim.position.y = h + 0.05;
      group.add(topTrim);

      const frontPlaque = new THREE.Mesh(new THREE.BoxGeometry(w * 0.55, h * 0.35, 0.08), darkWoodMat);
      frontPlaque.position.set(0, h * 0.6, d / 2 + 0.03);
      group.add(frontPlaque);

      group.position.set(x, y, z);
      group.rotation.y = rotY;
      scene.add(group);
      return group;
    }

    // Elevated Jury Bench + Side Prosecutor & Defense Podiums
    const juryTier = new THREE.Mesh(new THREE.BoxGeometry(8, 1.1, 4.2), darkWoodMat);
    juryTier.position.set(0, 0.55, -3.6);
    juryTier.receiveShadow = true;
    scene.add(juryTier);

    createBench(4.6, 1.8, 1.6, 0, 1.1, -3.1, 0);
    createBench(3.0, 1.5, 1.4, -5.2, 0, 1.2, 0.38);
    createBench(3.0, 1.5, 1.4, 5.2, 0, 1.2, -0.38);

    // 3D Chibi Character Builder (Big Expressive Head, Suit, Hair, Animated Arms)
    function createChibiCharacter({ suitColor, accentColor, hairColor, isJudge = false, isProsecutor = false }) {
      const chibi = new THREE.Group();

      // Torso / Robe
      const bodyGeo = new THREE.CylinderGeometry(0.45, 0.62, 1.25, 20);
      const bodyMat = new THREE.MeshStandardMaterial({ color: suitColor, roughness: 0.5 });
      const body = new THREE.Mesh(bodyGeo, bodyMat);
      body.position.y = 0.65;
      body.castShadow = true;
      chibi.add(body);

      // Tie / Cravat / Gold Stole
      const tieGeo = new THREE.ConeGeometry(0.18, 0.65, 4);
      const tieMat = new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.3 });
      const tie = new THREE.Mesh(tieGeo, tieMat);
      tie.position.set(0, 0.85, 0.46);
      tie.rotation.x = Math.PI;
      chibi.add(tie);

      // Big Chibi Head
      const skinMat = new THREE.MeshStandardMaterial({ color: 0xffe0c8, roughness: 0.45 });
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.68, 28, 28), skinMat);
      head.scale.set(1.06, 0.96, 0.98);
      head.position.y = 1.82;
      head.castShadow = true;
      chibi.add(head);

      // Anime Eyes
      const eyeWhiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const pupilMat = new THREE.MeshBasicMaterial({ color: 0x161622 });
      [-0.23, 0.23].forEach(xOffset => {
        const eyeW = new THREE.Mesh(new THREE.SphereGeometry(0.11, 14, 14), eyeWhiteMat);
        eyeW.scale.set(0.85, 1.15, 0.4);
        eyeW.position.set(xOffset, 1.84, 0.61);
        chibi.add(eyeW);

        const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.065, 12, 12), pupilMat);
        pupil.position.set(xOffset, 1.84, 0.66);
        chibi.add(pupil);
      });

      // Blush Cheeks
      const blushMat = new THREE.MeshBasicMaterial({ color: 0xff7b93, transparent: true, opacity: 0.55 });
      [-0.36, 0.36].forEach(xOffset => {
        const blush = new THREE.Mesh(new THREE.SphereGeometry(0.08, 10, 10), blushMat);
        blush.scale.set(1.3, 0.6, 0.3);
        blush.position.set(xOffset, 1.70, 0.60);
        chibi.add(blush);
      });

      // Stylized Hair / Wig
      const hairMat = new THREE.MeshStandardMaterial({ color: hairColor, roughness: 0.55 });
      const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.72, 24, 24, 0, Math.PI * 2, 0, Math.PI * 0.58), hairMat);
      hairCap.position.set(0, 1.86, -0.02);
      chibi.add(hairCap);

      if (isJudge) {
        // Golden Crown / Tribunal Crest + Gavel Arm
        const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.26, 0.28, 8), goldMat);
        crown.position.set(0, 2.62, 0.1);
        chibi.add(crown);
      } else {
        // Spiky Anime Hair Tufts
        for (let i = -2; i <= 2; i++) {
          const spike = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.5, 6), hairMat);
          spike.position.set(i * 0.22, 2.38, 0.25);
          spike.rotation.z = -i * 0.25;
          spike.rotation.x = 0.35;
          chibi.add(spike);
        }
      }

      // Expressive Right Arm (Points or Holds Gavel)
      const rightArmPivot = new THREE.Group();
      rightArmPivot.position.set(0.52, 1.1, 0.1);
      const armMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.1, 0.7, 12), bodyMat);
      armMesh.position.y = -0.25;
      rightArmPivot.add(armMesh);

      const handMesh = new THREE.Mesh(new THREE.SphereGeometry(0.13, 12, 12), skinMat);
      handMesh.position.y = -0.62;
      rightArmPivot.add(handMesh);

      if (isJudge) {
        // Judge's 3D Gavel
        const handle = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.45), woodMat);
        handle.position.set(0, -0.65, 0.18);
        handle.rotation.x = Math.PI / 2;
        rightArmPivot.add(handle);
        const mallet = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, 0.26), goldMat);
        mallet.position.set(0, -0.65, 0.38);
        mallet.rotation.z = Math.PI / 2;
        rightArmPivot.add(mallet);
      }

      chibi.add(rightArmPivot);
      chibi.userData = { rightArmPivot, baseY: 0, isProsecutor, isJudge };
      return chibi;
    }

    const chibiPros = createChibiCharacter({ suitColor: 0x9e192d, accentColor: 0xf7f4ef, hairColor: 0x262335, isProsecutor: true });
    chibiPros.position.set(-5.2, 0.5, 0.45);
    chibiPros.rotation.y = 0.38;
    chibiPros.userData.baseY = 0.5;
    scene.add(chibiPros);

    const chibiJury = createChibiCharacter({ suitColor: 0x1b1f2e, accentColor: 0xe5b869, hairColor: 0xe8e6f2, isJudge: true });
    chibiJury.position.set(0, 2.0, -3.7);
    chibiJury.userData.baseY = 2.0;
    scene.add(chibiJury);

    const chibiDef = createChibiCharacter({ suitColor: 0x16569c, accentColor: 0xe02f44, hairColor: 0x161d2b });
    chibiDef.position.set(5.2, 0.5, 0.45);
    chibiDef.rotation.y = -0.38;
    chibiDef.userData.baseY = 0.5;
    scene.add(chibiDef);

    // Camera Presets for Each Speaker
    let activeSpeakerRole = 'IDLE';
    function setCameraTarget(role) {
      if (role === 'PROSECUTION') {
        camPosTarget.set(-2.4, 3.0, 5.6);
        camLookTarget.set(-5.0, 2.0, 0.5);
      } else if (role === 'DEFENSE') {
        camPosTarget.set(2.4, 3.0, 5.6);
        camLookTarget.set(5.0, 2.0, 0.5);
      } else if (role === 'JURY') {
        camPosTarget.set(0, 4.3, 3.2);
        camLookTarget.set(0, 3.4, -3.7);
      } else {
        camPosTarget.set(0, 5.2, 13.2);
        camLookTarget.set(0, 2.0, -0.5);
      }
    }

    function setActiveSpeaker(role) {
      if (activeSpeakerRole !== role) {
        activeSpeakerRole = role;
        setCameraTarget(role);
        if (role === 'PROSECUTION') {
          triggerCallout('💥 OBJECTION!', 'from-rose-600 to-red-900');
          playSFX('objection');
        } else if (role === 'DEFENSE') {
          triggerCallout('🛡️ HOLD IT!', 'from-sky-500 to-blue-900');
          playSFX('objection');
        } else if (role === 'JURY') {
          triggerCallout('⚖️ FINAL VERDICT!', 'from-amber-500 to-yellow-800');
          playSFX('gavel');
        }
      }
      spotPros.intensity = role === 'PROSECUTION' ? 2.6 : 0.25;
      spotDef.intensity  = role === 'DEFENSE'     ? 2.6 : 0.25;
      spotJury.intensity = role === 'JURY'        ? 2.8 : 0.4;
    }

    function triggerCallout(text, gradientClasses) {
      const el = document.getElementById('callout-banner');
      el.className = `px-8 py-3 rounded-2xl border-4 border-white shadow-2xl font-cinzel font-extrabold text-3xl tracking-widest text-white bg-gradient-to-r ${gradientClasses} show`;
      el.innerText = text;
      setTimeout(() => el.classList.remove('show'), 1400);
    }

    // 60FPS Animation Loop
    const clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      const t = clock.getElapsedTime();

      // Smooth Camera Interpolation
      camera.position.lerp(camPosTarget, 0.055);
      currentLook.lerp(camLookTarget, 0.065);
      camera.lookAt(currentLook);

      // Animate Chibi Characters (Idle breathing vs Excited speaking bounce & arm gesture)
      [
        { mesh: chibiPros, role: 'PROSECUTION' },
        { mesh: chibiDef,  role: 'DEFENSE' },
        { mesh: chibiJury, role: 'JURY' }
      ].forEach(({ mesh, role }, i) => {
        const isSpeaking = activeSpeakerRole === role;
        const bounceSpeed = isSpeaking ? 11 : 2.2;
        const bounceAmp   = isSpeaking ? 0.16 : 0.035;
        mesh.position.y = mesh.userData.baseY + Math.abs(Math.sin(t * bounceSpeed + i)) * bounceAmp;

        const arm = mesh.userData.rightArmPivot;
        if (isSpeaking) {
          arm.rotation.x = -1.35 + Math.sin(t * 14) * 0.35;
        } else {
          arm.rotation.x = THREE.MathUtils.lerp(arm.rotation.x, -0.2, 0.1);
        }
      });

      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // ============================================================================
    // 3. STATE, WEBSOCKET STREAMING & DRAWER MANAGEMENT
    // ============================================================================
    let appState = {
      transcript: [],
      evidence_md: "*No exhibits logged yet...*",
      verdict_md: "*The Supreme Jury is waiting for arguments to conclude...*",
      latest_statement: "",
      activeDrawer: null
    };
    let activeSocket = null;
    let lastBlipTime = 0;
    let drawerRenderScheduled = false;

    function scheduleDrawerRender() {
      if (drawerRenderScheduled) return;
      drawerRenderScheduled = true;
      window.setTimeout(() => {
        drawerRenderScheduled = false;
        renderDrawerContent();
      }, 120);
    }

    async function loadConfig() {
      const res = await fetch('/api/config');
      const cfg = await res.json();

      const crimeSel = document.getElementById('input-crime');
      crimeSel.innerHTML = cfg.preset_crimes.map(c => `<option value="${c}">${c}</option>`).join('');

      ['input-pros-model', 'input-def-model', 'input-jury-model'].forEach((id, idx) => {
        const sel = document.getElementById(id);
        sel.innerHTML = cfg.models.map(m => `<option value="${m}">${m}</option>`).join('');
        sel.value = [cfg.default_pros, cfg.default_def, cfg.default_jury][idx];
      });
    }
    loadConfig();

    function toggleCustomCrime() {
      const val = document.getElementById('input-crime').value;
      document.getElementById('custom-crime-wrap').classList.toggle('hidden', !val.includes('Custom'));
    }

    function toggleModal(id) {
      document.getElementById(id).classList.toggle('hidden');
    }

    function toggleDrawer(tab) {
      const drawer = document.getElementById('side-drawer');
      if (appState.activeDrawer === tab) {
        closeDrawer();
        return;
      }
      appState.activeDrawer = tab;
      drawer.classList.remove('translate-x-[520px]');
      renderDrawerContent();
    }

    function closeDrawer() {
      appState.activeDrawer = null;
      document.getElementById('side-drawer').classList.add('translate-x-[520px]');
    }

    function renderDrawerContent() {
      const titleEl = document.getElementById('drawer-title');
      const bodyEl  = document.getElementById('drawer-body');
      if (!appState.activeDrawer) return;

      if (appState.activeDrawer === 'transcript') {
        titleEl.innerText = '🎙️ FULL COURTROOM TRANSCRIPT';
        if (!appState.transcript.length) {
          bodyEl.innerHTML = `<p class="text-slate-400 italic">No arguments recorded yet.</p>`;
          return;
        }
        bodyEl.innerHTML = appState.transcript.map((t) => {
          const isPros = t.role_key === 'PROSECUTION';
          const border = isPros ? 'border-rose-500/50 bg-rose-950/25' : 'border-sky-500/50 bg-sky-950/25';
          const badge  = isPros ? '🔴' : '🔵';
          const statement = (t.statement || '*Streaming...*')
            .replace(/^\s*\[Round\s+\d+\s*[–-]\s*[^\]]+\]\s*/i, '');
          return `
            <div class="p-3.5 rounded-xl border ${border}">
              <div class="text-xs font-bold text-amber-300 mb-1.5">${badge} ${t.role_label} · Round ${t.round_number}</div>
              <div class="prose prose-invert prose-sm max-w-none text-slate-200 leading-relaxed">${marked.parse(statement)}</div>
            </div>
          `;
        }).join('');
        bodyEl.scrollTop = bodyEl.scrollHeight;
      } else if (appState.activeDrawer === 'evidence') {
        titleEl.innerText = '🗂️ EVIDENCE LOCKER';
        bodyEl.innerHTML = `<div class="prose prose-invert prose-sm max-w-none">${marked.parse(appState.evidence_md)}</div>`;
      } else if (appState.activeDrawer === 'verdict') {
        titleEl.innerText = '🏛️ SUPREME JURY VERDICT';
        bodyEl.innerHTML = `<div class="prose prose-invert prose-sm max-w-none">${marked.parse(appState.verdict_md)}</div>`;
      }
    }

    function startTrial() {
      if (activeSocket) activeSocket.close();

      const country = document.getElementById('input-country').value.trim() || 'Egypt';
      const rounds  = parseInt(document.getElementById('input-rounds').value, 10) || 3;
      const preset  = document.getElementById('input-crime').value;
      const custom  = document.getElementById('input-custom-crime').value.trim();
      const crime   = preset.includes('Custom') ? custom : preset;

      const pros_model = document.getElementById('input-pros-model').value;
      const def_model  = document.getElementById('input-def-model').value;
      const jury_model = document.getElementById('input-jury-model').value;

      document.getElementById('hud-subtitle').innerText = `JURISDICTION: ${country.toUpperCase()} · SESSION LIVE`;
      document.getElementById('vn-status-indicator').innerText = '🟡 CONVENING TRIBUNAL...';
      playSFX('gavel');

      const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
      activeSocket = new WebSocket(`${proto}://${window.location.host}/ws/trial`);

      activeSocket.onopen = () => {
        activeSocket.send(JSON.stringify({ country, crime, rounds, pros_model, def_model, jury_model }));
      };

      activeSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
          document.getElementById('vn-status-indicator').innerText = `🔴 ERROR: ${data.error}`;
          document.getElementById('vn-dialogue-text').innerHTML = `<span class="text-rose-400 font-bold">${data.error}</span>`;
          return;
        }

        appState.transcript = data.transcript || [];
        appState.evidence_md = data.evidence_md || appState.evidence_md;
        appState.verdict_md  = data.verdict_md  || appState.verdict_md;
        appState.latest_statement = data.latest_statement || "";

        document.getElementById('badge-turns').innerText = appState.transcript.length;
        setActiveSpeaker(data.active_role);

        // Update VN Speaker Badge & Text
        const badgeEl = document.getElementById('vn-speaker-badge');
        document.getElementById('vn-speaker-name').innerText = data.speaker_title;
        document.getElementById('vn-round-badge').innerText = data.round_label;

        if (data.active_role === 'PROSECUTION') {
          document.getElementById('vn-speaker-icon').innerText = '🔴';
          badgeEl.className = 'absolute -top-5 left-6 px-5 py-1.5 rounded-xl font-cinzel font-extrabold text-sm tracking-widest text-white shadow-xl border-2 border-rose-300 bg-gradient-to-r from-rose-700 to-red-950 flex items-center gap-2 z-20';
        } else if (data.active_role === 'DEFENSE') {
          document.getElementById('vn-speaker-icon').innerText = '🔵';
          badgeEl.className = 'absolute -top-5 left-6 px-5 py-1.5 rounded-xl font-cinzel font-extrabold text-sm tracking-widest text-white shadow-xl border-2 border-sky-300 bg-gradient-to-r from-sky-700 to-blue-950 flex items-center gap-2 z-20';
        } else if (data.active_role === 'JURY') {
          document.getElementById('vn-speaker-icon').innerText = '⚖️';
          badgeEl.className = 'absolute -top-5 left-6 px-5 py-1.5 rounded-xl font-cinzel font-extrabold text-sm tracking-widest text-white shadow-xl border-2 border-amber-200 bg-gradient-to-r from-amber-600 to-yellow-900 flex items-center gap-2 z-20';
        }

        const vnBox = document.getElementById('vn-dialogue-text');
        vnBox.innerHTML = marked.parse(data.dialogue_text || '');
        vnBox.scrollTop = vnBox.scrollHeight;

        const now = performance.now();
        if (now - lastBlipTime > 75 && !data.is_complete) {
          playSFX('blip');
          lastBlipTime = now;
        }

        document.getElementById('vn-status-indicator').innerText = data.is_complete
          ? '🟢 VERDICT DELIVERED · COURT ADJOURNED'
          : `🟢 LIVE STREAMING · ${data.round_label}`;

        scheduleDrawerRender();

        if (data.is_complete) {
          renderDrawerContent();
          toggleDrawer('verdict');
          if (document.getElementById('auto-tts-toggle').checked) {
            speakLatest();
          }
        }
      };
    }

    async function speakLatest() {
      if (!appState.latest_statement) return;
      document.getElementById('vn-status-indicator').innerText = '🔊 SYNTHESIZING COURTROOM VOICE...';
      const res = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: appState.latest_statement })
      });
      if (res.ok) {
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const player = document.getElementById('tts-player');
        player.src = url;
        player.play();
        document.getElementById('vn-status-indicator').innerText = '🔊 PLAYING COURTROOM AUDIO';
      }
    }
