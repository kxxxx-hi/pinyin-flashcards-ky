# api/index.py
# FastAPI app for Vercel. Serves a single-page game: "Which one are you hearing?"
# Data live in data.json (same repo root). UI in English; only 'text' is Chinese.

from fastapi import FastAPI, Response
from pathlib import Path
import json

app = FastAPI()

HTML = r"""<!doctype html>
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
    <h1 class="text-2xl md:text-3xl font-extrabold">Which one are you hearing?</h1>
    <p class="text-gray-500 mt-1">Click the speaker to play the Chinese word. Choose the correct pinyin.</p>
  </header>

  <main>
    <div class="bg-gray-50 rounded-xl p-6 text-center shadow-inner card">
      <div class="flex items-center justify-center gap-3 mb-4">
        <span class="text-sm text-gray-600">Question</span>
        <span id="counter" class="text-sm font-semibold text-gray-800">0 / 0</span>
      </div>

      <button id="play" class="mb-6 w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 hover:bg-indigo-200 btn" title="Play audio">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
        </svg>
      </button>

      <div id="prompt" class="text-xl text-gray-700 mb-2"></div>

      <div id="choices" class="grid grid-cols-2 gap-4 w-full max-w-md"></div>

      <div id="feedback" class="h-6 text-center font-medium mt-4"></div>

      <div class="mt-6 flex items-center justify-between text-sm text-gray-600 w-full max-w-md">
        <button id="repeat" class="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 btn">Repeat</button>
        <button
