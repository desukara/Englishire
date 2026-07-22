#!/usr/bin/env python3
"""Bounded parallel runner for the canonical Japanese site generator."""
from __future__ import annotations

import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import generate_japanese_site as generator
from deep_translator import GoogleTranslator

socket.setdefaulttimeout(20)


def translate_one(source: str) -> tuple[str, str]:
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            translated = GoogleTranslator(source="en", target="ja").translate(source)
            if translated:
                return source, translated
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 + attempt * 1.5)
    raise RuntimeError(f"Unable to translate {source!r}: {last_error}")


def parallel_translate_all(strings: list[str], cache: dict[str, str]) -> None:
    pending = [value for value in strings if value not in cache and value not in generator.FIXED]
    completed = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(translate_one, value): value for value in pending}
        for future in as_completed(futures):
            source = futures[future]
            try:
                key, translated = future.result()
            except Exception as exc:
                for remaining in futures:
                    remaining.cancel()
                raise RuntimeError(f"Translation failed at {source!r}") from exc
            cache[key] = translated
            completed += 1
            if completed % 25 == 0 or completed == len(pending):
                generator.save_cache(cache)
                print(f"translated {completed}/{len(pending)}", flush=True)


generator.translate_all = parallel_translate_all

if __name__ == "__main__":
    generator.main()
