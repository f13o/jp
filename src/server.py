#!/usr/bin/env python3
import json
import os
import sys
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

DICT = []

def load_dict():
    global DICT
    path = os.path.join(os.path.dirname(__file__) or '.', 'dict.json')
    if not os.path.exists(path):
        print(f'dict.json not found, dictionary search disabled', file=sys.stderr)
        return
    with open(path, encoding='utf-8') as f:
        DICT = json.load(f)
    print(f'loaded {len(DICT)} dictionary entries', file=sys.stderr)

def search(q, limit=50):
    q = q.strip().lower()
    if not q:
        return []
    exact_jp = []
    partial_jp = []
    exact_gloss = []
    partial_gloss = []
    for entry in DICT:
        kanji = entry.get('k', [])
        readings = entry['r']
        if q in kanji or q in readings:
            exact_jp.append(entry)
            continue
        if any(q in k for k in kanji) or any(q in r for r in readings):
            partial_jp.append(entry)
            continue
        all_glosses = [g for s in entry['s'] for g in s.get('e', []) + s.get('s', [])]
        if any(q == g.lower() for g in all_glosses):
            exact_gloss.append(entry)
        elif any(q in g.lower() for g in all_glosses):
            partial_gloss.append(entry)
    for bucket in (exact_jp, partial_jp, exact_gloss, partial_gloss):
        bucket.sort(key=lambda e: not e.get('c'))
    return (exact_jp + partial_jp + exact_gloss + partial_gloss)[:limit]


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/search':
            params = urllib.parse.parse_qs(parsed.query)
            q = params.get('q', [''])[0]
            results = search(q)
            body = json.dumps(results, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__) or '.')
    load_dict()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    server = HTTPServer(('', port), Handler)
    print(f'http://localhost:{port}', file=sys.stderr)
    server.serve_forever()
