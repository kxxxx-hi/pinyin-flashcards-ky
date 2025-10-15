
# api/index.py
from fastapi import FastAPI, Response
from pathlib import Path
import json

app = FastAPI()

# Homepage HTML
HOMEPAGE_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Mandarin Learning Helper by Kexin</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Inter', sans-serif; }
  .btn { transition: transform .15s ease; }
  .btn:hover { transform: translateY(-1px); }
</style>
</head>
<body class="bg-gray-100 text-gray-800 flex items-center justify-center min-h-screen p-4">
<div class="w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-lg p-8 md:p-12">
  <header class="text-center mb-12">
    <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">Mandarin Learning Helper</h1>
    <p class="text-xl text-gray-600">by Kexin</p>
  </header>

  <main class="space-y-6">
    <div class="grid grid-cols-1 gap-6">
      <!-- Game 1: Pinyin Listening -->
      <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-200">
        <h2 class="text-xl font-bold text-indigo-900 mb-3">🎵 Pinyin Listening Game</h2>
        <p class="text-gray-700 mb-4">Listen to Chinese words and choose the correct pinyin pronunciation.</p>
        <a href="/game/pinyin" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 btn block text-center">
          Play Game
        </a>
      </div>

      <!-- Game 2: HSK Lesson 4-6 -->
      <div class="bg-gradient-to-br from-green-50 to-blue-50 rounded-xl p-6 border border-green-200">
        <h2 class="text-xl font-bold text-green-900 mb-3">📚 HSK 1 Lesson 4-6</h2>
        <p class="text-gray-700 mb-4">Learn vocabulary with English to Chinese flash cards including pinyin.</p>
        <a href="/game/hsk-4-6" class="w-full bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 btn block text-center">
          Play Game
        </a>
      </div>

      <!-- Game 3: HSK Lesson 7-9 -->
      <div class="bg-gradient-to-br from-orange-50 to-pink-50 rounded-xl p-6 border border-orange-200">
        <h2 class="text-xl font-bold text-orange-900 mb-3">📖 HSK 1 Lesson 7-9</h2>
        <p class="text-gray-700 mb-4">Continue learning with more vocabulary flash cards and pinyin practice.</p>
        <a href="/game/hsk-7-9" class="w-full bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-700 btn block text-center">
          Play Game
        </a>
      </div>
    </div>

    <div class="text-center mt-8">
      <p class="text-sm text-gray-500">Choose an exercise to practice Chinese!</p>
    </div>
  </main>
</div>
</body>
</html>"""

# Original Pinyin Game HTML
PINYIN_GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Which one are you hearing?</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Inter', sans-serif; }
  .card { min-height: 18rem; display:flex; flex-direction:column; justify-content:center; align-items:center; }
  .btn { transition: transform .15s ease; }
  .btn:hover { transform: translateY(-1px); }
  .correct { background-color:#10b981 !important; color:#fff !important; border-color:#059669 !important; }
  .incorrect { background-color:#ef4444 !important; color:#fff !important; border-color:#dc2626 !important; }
</style>
</head>
<body class="bg-gray-100 text-gray-800 flex items-center justify-center min-h-screen p-4">
<div class="w-full max-w-xl mx-auto bg-white rounded-2xl shadow-lg p-6 md:p-8">
  <header class="text-center mb-6">
    <div class="flex justify-between items-center mb-4">
      <button onclick="window.location.href='/'" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 btn">← Home</button>
      <div></div>
    </div>
    <h1 class="text-2xl md:text-3xl font-extrabold">Which one are you hearing?</h1>
    <p class="text-gray-500 mt-1">Click the speaker to play the Chinese word. Choose the correct pinyin.</p>
  </header>

  <main>
    <div class="bg-gray-50 rounded-xl p-6 text-center shadow-inner card">
      <div class="flex items-center justify-center gap-3 mb-4">
        <span class="text-sm text-gray-600">Question</span>
        <span id="counter" class="text-sm font-semibold text-gray-800">0 / 0</span>
      </div>

      <button id="play" class="mb-4 w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 hover:bg-indigo-200 btn" title="Play audio">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
        </svg>
      </button>

      <!-- Chinese and constant English meaning -->
      <div id="prompt" class="text-2xl text-gray-900 mb-1"></div>
      <div id="meaning" class="text-sm text-gray-600 mb-6"></div>

      <div id="choices" class="grid grid-cols-2 gap-4 w-full max-w-md"></div>

      <div id="feedback" class="h-6 text-center font-medium mt-4"></div>

      <div class="mt-6 flex items-center justify-between text-sm text-gray-600 w-full max-w-md">
        <button id="repeat" class="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 btn">Repeat</button>
        <button id="next" class="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 btn">Next</button>
      </div>
    </div>

    <p class="text-xs text-gray-500 text-center mt-4">
      Tip: The audio speaks the Chinese word. Match the pinyin with the correct tone.
    </p>
  </main>
</div>

<script>
  const DATA = __DATA__;
  const synth = window.speechSynthesis;

  let items = Array.isArray(DATA?.pinyinPairs) ? DATA.pinyinPairs.slice(0) : [];
  let i = 0;
  let current = null; // {text, en, correct, distractor}

  const playBtn = document.getElementById('play');
  const repeatBtn = document.getElementById('repeat');
  const nextBtn = document.getElementById('next');
  const choicesDiv = document.getElementById('choices');
  const counter = document.getElementById('counter');
  const feedback = document.getElementById('feedback');
  const promptNode = document.getElementById('prompt');
  const meaningNode = document.getElementById('meaning');

  // ---- Pinyin tone mark conversion (display only) ----
  function toToneMarks(pinyinStr){
    if(!pinyinStr) return "";
    // Per-syllable: find trailing tone digit 1-4 (0/5 = neutral), apply to vowel.
    const toneMap = {
      'a': ['ā','á','ǎ','à'], 'e': ['ē','é','ě','è'], 'i': ['ī','í','ǐ','ì'],
      'o': ['ō','ó','ǒ','ò'], 'u': ['ū','ú','ǔ','ù'], 'ü': ['ǖ','ǘ','ǚ','ǜ']
    };
    function convertSyllable(syl){
      if(!syl) return syl;
      // Handle ü written as "u:" or "v"
      syl = syl.replace(/u:/gi,'ü').replace(/v/gi,'ü');
      const m = syl.match(/^([a-zāēīōūǖü]+)([1-5])$/i);
      let base = syl, tone = 0;
      if(m){
        base = m[1];
        tone = parseInt(m[2],10);
      }
      if(tone===0 || tone===5 || !/[aeiouü]/i.test(base)) return base;
      const lower = base.toLowerCase();
      // Priority: a > e > o; for iu/ui mark second vowel
      let idx = -1;
      if(lower.includes('a')) idx = lower.indexOf('a');
      else if(lower.includes('e')) idx = lower.indexOf('e');
      else if(lower.includes('ou')) idx = lower.indexOf('o');
      else if(lower.includes('o')) idx = lower.indexOf('o');
      else if(lower.includes('iu')) idx = lower.indexOf('u'); // second in "iu"
      else if(lower.includes('ui')) idx = lower.indexOf('i'); // second in "ui"
      else {
        // pick last vowel
        const last = Math.max(lower.lastIndexOf('i'), lower.lastIndexOf('u'), lower.lastIndexOf('ü'));
        idx = last;
      }
      if(idx < 0) return base;
      const ch = base[idx];
      const key = ch.toLowerCase();
      const rep = toneMap[key] ? toneMap[key][tone-1] : ch;
      // preserve case
      const repFinal = (ch===ch.toUpperCase()) ? rep.toUpperCase() : rep;
      return base.slice(0,idx) + repFinal + base.slice(idx+1);
    }
    // Split by space to keep multi-syllable spacing intact
    return pinyinStr.split(/\s+/).map(convertSyllable).join(' ');
  }

  function shuffle(arr){
    for(let k=arr.length-1;k>0;k--){
      const j = Math.floor(Math.random()*(k+1));
      [arr[k],arr[j]]=[arr[j],arr[k]];
    }
    return arr;
  }
  function speak(text){
    if(!text) return;
    if(synth.speaking) synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'zh-CN';
    u.rate = 0.95;
    synth.speak(u);
  }
  function setCounter(){
    counter.textContent = `${items.length ? i+1 : 0} / ${items.length}`;
  }
  function render(){
    if(!items.length){
      choicesDiv.innerHTML = '<p class="text-gray-500 col-span-2">No data found. Provide pinyinPairs in data.json.</p>';
      counter.textContent = '0 / 0';
      promptNode.textContent = '';
      meaningNode.textContent = '';
      feedback.textContent = '';
      return;
    }
    feedback.textContent = '';
    feedback.className = 'h-6 text-center font-medium mt-4';

    const q = items[i % items.length];
    current = q;

    promptNode.textContent = q.text || '';
    meaningNode.textContent = q.en || '';

    const opts = shuffle([q.correct, q.distractor]);
    choicesDiv.innerHTML = '';
    opts.forEach(opt => {
      const b = document.createElement('button');
      b.textContent = toToneMarks(opt);       // display with accents
      b.dataset.val = opt;                    // keep original numbered value for checking
      b.className = 'w-full px-4 py-3 border border-gray-300 rounded-lg text-lg font-semibold bg-white text-gray-800 hover:bg-gray-50 btn';
      b.onclick = () => check(b.dataset.val);
      choicesDiv.appendChild(b);
    });

    setTimeout(()=> speak(q.text || ''), 150);
    setCounter();
  }
  function check(selectedVal){
    const buttons = choicesDiv.querySelectorAll('button');
    buttons.forEach(btn => {
      btn.disabled = true;
      const isCorrect = btn.dataset.val === current.correct;
      if(isCorrect) btn.classList.add('correct');
      else if(btn.dataset.val === selectedVal) btn.classList.add('incorrect');
    });
    if(selectedVal === current.correct){
      feedback.textContent = 'Correct';
      feedback.classList.add('text-green-600');
    } else {
      feedback.textContent = 'Incorrect';
      feedback.classList.add('text-red-600');
    }
  }

  playBtn.addEventListener('click', () => speak(current?.text || ''));
  repeatBtn.addEventListener('click', () => speak(current?.text || ''));
  nextBtn.addEventListener('click', () => { i = (i + 1) % (items.length || 1); render(); });

  render();
</script>
</body>
</html>"""

# HSK Flash Cards Game HTML
HSK_GAME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>__LESSON_TITLE__ Flash Cards</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  body { font-family: 'Inter', sans-serif; }
  .card { min-height: 18rem; display:flex; flex-direction:column; justify-content:center; align-items:center; }
  .btn { transition: transform .15s ease; }
  .btn:hover { transform: translateY(-1px); }
  .correct { background-color:#10b981 !important; color:#fff !important; border-color:#059669 !important; }
  .incorrect { background-color:#ef4444 !important; color:#fff !important; border-color:#dc2626 !important; }
</style>
</head>
<body class="bg-gray-100 text-gray-800 flex items-center justify-center min-h-screen p-4">
<div class="w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-lg p-6 md:p-8">
  <header class="text-center mb-6">
    <div class="flex justify-between items-center mb-4">
      <button onclick="window.location.href='/'" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 btn">← Home</button>
      <div></div>
    </div>
    <h1 class="text-2xl md:text-3xl font-extrabold">__LESSON_TITLE__ Flash Cards</h1>
    <p class="text-gray-500 mt-1">Read the English word and choose the correct Chinese translation with pinyin.</p>
  </header>

  <main>
    <div class="bg-gray-50 rounded-xl p-6 text-center shadow-inner card">
      <div class="flex items-center justify-center gap-3 mb-4">
        <span class="text-sm text-gray-600">Question</span>
        <span id="counter" class="text-sm font-semibold text-gray-800">0 / 0</span>
      </div>

      <!-- English word display -->
      <div id="englishWord" class="text-3xl md:text-4xl text-gray-900 mb-6 font-bold"></div>

      <div id="choices" class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl"></div>

      <div id="feedback" class="h-6 text-center font-medium mt-4"></div>

      <div class="mt-6 flex justify-end text-sm text-gray-600 w-full">
        <button id="next" class="px-6 py-2 rounded-lg border bg-white hover:bg-gray-50 btn">Next</button>
      </div>
    </div>

    <p class="text-xs text-gray-500 text-center mt-4">
      Tip: Choose the Chinese character that matches the English word. Pay attention to both the character and pinyin.
    </p>
  </main>
</div>

<script>
  const DATA = __DATA__;

  let items = Array.isArray(DATA?.hskFlashcards) ? DATA.hskFlashcards.slice(0) : [];
  let i = 0;
  let current = null;

  const choicesDiv = document.getElementById('choices');
  const counter = document.getElementById('counter');
  const feedback = document.getElementById('feedback');
  const englishWordNode = document.getElementById('englishWord');
  const nextBtn = document.getElementById('next');

  function shuffle(arr){
    for(let k=arr.length-1;k>0;k--){
      const j = Math.floor(Math.random()*(k+1));
      [arr[k],arr[j]]=[arr[j],arr[k]];
    }
    return arr;
  }

  // ---- Pinyin tone mark conversion (display only) ----
  function toToneMarks(pinyinStr){
    if(!pinyinStr) return "";
    // Per-syllable: find trailing tone digit 1-4 (0/5 = neutral), apply to vowel.
    const toneMap = {
      'a': ['ā','á','ǎ','à'], 'e': ['ē','é','ě','è'], 'i': ['ī','í','ǐ','ì'],
      'o': ['ō','ó','ǒ','ò'], 'u': ['ū','ú','ǔ','ù'], 'ü': ['ǖ','ǘ','ǚ','ǜ']
    };
    function convertSyllable(syl){
      if(!syl) return syl;
      // Handle ü written as "u:" or "v"
      syl = syl.replace(/u:/gi,'ü').replace(/v/gi,'ü');
      const m = syl.match(/^([a-zāēīōūǖü]+)([1-5])$/i);
      let base = syl, tone = 0;
      if(m){
        base = m[1];
        tone = parseInt(m[2],10);
      }
      if(tone===0 || tone===5 || !/[aeiouü]/i.test(base)) return base;
      const lower = base.toLowerCase();
      // Priority: a > e > o; for iu/ui mark second vowel
      let idx = -1;
      if(lower.includes('a')) idx = lower.indexOf('a');
      else if(lower.includes('e')) idx = lower.indexOf('e');
      else if(lower.includes('ou')) idx = lower.indexOf('o');
      else if(lower.includes('o')) idx = lower.indexOf('o');
      else if(lower.includes('iu')) idx = lower.indexOf('u'); // second in "iu"
      else if(lower.includes('ui')) idx = lower.indexOf('i'); // second in "ui"
      else {
        // pick last vowel
        const last = Math.max(lower.lastIndexOf('i'), lower.lastIndexOf('u'), lower.lastIndexOf('ü'));
        idx = last;
      }
      if(idx < 0) return base;
      const ch = base[idx];
      const key = ch.toLowerCase();
      const rep = toneMap[key] ? toneMap[key][tone-1] : ch;
      // preserve case
      const repFinal = (ch===ch.toUpperCase()) ? rep.toUpperCase() : rep;
      return base.slice(0,idx) + repFinal + base.slice(idx+1);
    }
    // Split by space to keep multi-syllable spacing intact
    return pinyinStr.split(/\s+/).map(convertSyllable).join(' ');
  }

  function setCounter(){
    counter.textContent = `${items.length ? i+1 : 0} / ${items.length}`;
  }

  function render(){
    if(!items.length){
      choicesDiv.innerHTML = '<p class="text-gray-500 col-span-2">No data found. Provide hskFlashcards in data.json.</p>';
      counter.textContent = '0 / 0';
      englishWordNode.textContent = '';
      feedback.textContent = '';
      return;
    }
    feedback.textContent = '';
    feedback.className = 'h-6 text-center font-medium mt-4';

    const q = items[i % items.length];
    current = q;

    englishWordNode.textContent = q.english || '';

    // Create all options (correct + distractors)
    const allOptions = [q.correct, ...q.distractors];
    const shuffledOptions = shuffle([...allOptions]);

    choicesDiv.innerHTML = '';
    shuffledOptions.forEach(opt => {
      const button = document.createElement('button');
      button.innerHTML = `
        <div class="text-2xl md:text-3xl font-bold mb-2">${opt.chinese}</div>
        <div class="text-sm text-gray-600">${toToneMarks(opt.pinyin)}</div>
      `;
      button.dataset.chinese = opt.chinese;
      button.dataset.pinyin = opt.pinyin;
      button.className = 'w-full px-6 py-4 border border-gray-300 rounded-lg bg-white text-gray-800 hover:bg-gray-50 btn text-center';
      button.onclick = () => check(opt.chinese);
      choicesDiv.appendChild(button);
    });

    setCounter();
  }

  function check(selectedChinese){
    const buttons = choicesDiv.querySelectorAll('button');
    buttons.forEach(btn => {
      btn.disabled = true;
      const isCorrect = btn.dataset.chinese === current.correct.chinese;
      if(isCorrect) btn.classList.add('correct');
      else if(btn.dataset.chinese === selectedChinese) btn.classList.add('incorrect');
    });
    if(selectedChinese === current.correct.chinese){
      feedback.textContent = 'Correct! 🎉';
      feedback.classList.add('text-green-600');
    } else {
      feedback.textContent = 'Incorrect. The correct answer is ' + current.correct.chinese + ' (' + toToneMarks(current.correct.pinyin) + ')';
      feedback.classList.add('text-red-600');
    }
  }

  nextBtn.addEventListener('click', () => { i = (i + 1) % (items.length || 1); render(); });

  render();
</script>
</body>
</html>"""

@app.get("/")
def homepage() -> Response:
    return Response(content=HOMEPAGE_HTML, media_type="text/html")

@app.get("/game/pinyin")
def pinyin_game() -> Response:
    data_path = Path("data.json")
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except Exception:
        data = {"pinyinPairs": []}
    html = PINYIN_GAME_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    return Response(content=html, media_type="text/html")

@app.get("/game/hsk-4-6")
def hsk_game_4_6() -> Response:
    data_path = Path("data.json")
    try:
        full_data = json.loads(data_path.read_text(encoding="utf-8"))
        data = {"hskFlashcards": full_data.get("hskLesson4to6", [])}
    except Exception:
        data = {"hskFlashcards": []}
    html = HSK_GAME_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    html = html.replace("__LESSON_TITLE__", "HSK 1 Lesson 4-6")
    return Response(content=html, media_type="text/html")

@app.get("/game/hsk-7-9")
def hsk_game_7_9() -> Response:
    data_path = Path("data.json")
    try:
        full_data = json.loads(data_path.read_text(encoding="utf-8"))
        data = {"hskFlashcards": full_data.get("hskLesson7to9", [])}
    except Exception:
        data = {"hskFlashcards": []}
    html = HSK_GAME_HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    html = html.replace("__LESSON_TITLE__", "HSK 1 Lesson 7-9")
    return Response(content=html, media_type="text/html")
