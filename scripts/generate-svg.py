#!/usr/bin/env python3
# ⒸAngelaMos | 2025 | CertGames.com

import sys
import json
from pathlib import Path

def format_number(num):
    """
    Format number with commas
    """
    return f"{num:,}"

def generate_svg(loc_data):
    """
    Generate SVG card with LOC stats
    """
    total_code = int(loc_data.get('Total', {}).get('code', 0))
    total_lines = int(loc_data.get('Total', {}).get('lines', 0))

    # Count total files - try multiple methods
    total_files = 0
    languages = {}

    # Method 1: Try to get from Total stats (most reliable)
    if 'Total' in loc_data and isinstance(loc_data['Total'], dict):
        total_files = int(loc_data['Total'].get('files', 0))

    # Method 2: If that's 0, count from individual language reports
    if total_files == 0:
        for lang, stats in loc_data.items():
            if lang != 'Total' and isinstance(stats, dict):
                reports = stats.get('reports', [])
                if reports:
                    total_files += len(reports)

    # Second pass: aggregate language stats and merge variants
    for lang, stats in loc_data.items():
        if lang != 'Total' and isinstance(stats, dict):
            code_lines = int(stats.get('code', 0))

            if code_lines > 0:
                # Combine TSX with TypeScript, JSX with JavaScript
                if lang == 'TSX':
                    lang = 'TypeScript'
                elif lang == 'JSX':
                    lang = 'JavaScript'

                # Merge counts if language already exists
                if lang in languages:
                    languages[lang]['code'] += code_lines
                else:
                    languages[lang] = {'code': code_lines}

    # Sort by code count and get top 6
    top_languages = sorted(languages.items(), key=lambda x: x[1]['code'], reverse=True)[:6]

    language_colors = {
        'Python': '#3572A5',
        'JavaScript': '#f1e05a',
        'TypeScript': '#2b7489',
        'Rust': '#dea584',
        'Go': '#00ADD8',
        'Java': '#b07219',
        'Ruby': '#701516',
        'C': '#555555',
        'C++': '#f34b7d',
        'C#': '#178600',
        'PHP': '#4F5D95',
        'Swift': '#ffac45',
        'Kotlin': '#F18E33',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'Sass': '#a53b70',
        'SCSS': '#c6538c',
        'Shell': '#89e051',
        'Haskell': '#5e5086',
        'Vue': '#41b883',
        'JSON': '#b30000',
    }

    svg_width = 800
    svg_height = 320

    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#161b22;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accent-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#b30000;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ff0000;stop-opacity:0.8" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="{svg_width}" height="{svg_height}" fill="url(#bg-gradient)" rx="10"/>

  <rect x="10" y="10" width="{svg_width - 20}" height="3" fill="url(#accent-gradient)" rx="1.5"/>

  <text x="40" y="55" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="32" font-weight="700" fill="#c9d1d9">
    {format_number(total_code)}
  </text>
  <text x="40" y="80" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="14" fill="#8b949e">
    LINES OF CODE
  </text>

  <text x="{svg_width - 40}" y="55" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="24" font-weight="600" fill="#c9d1d9" text-anchor="end">
    {format_number(total_files)}
  </text>
  <text x="{svg_width - 40}" y="75" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="12" fill="#8b949e" text-anchor="end">
    FILES
  </text>

  <line x1="30" y1="100" x2="{svg_width - 30}" y2="100" stroke="#30363d" stroke-width="1"/>

  <text x="40" y="130" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="16" font-weight="600" fill="#b30000">
    TOP LANGUAGES
  </text>
'''

    y_offset = 160
    max_bar_width = svg_width - 350
    max_code = top_languages[0][1]['code'] if top_languages else 1

    for idx, (lang, lang_data) in enumerate(top_languages):
        code_lines = lang_data['code']
        color = language_colors.get(lang, '#58a6ff')
        bar_width = (code_lines / max_code) * max_bar_width
        percentage = (code_lines / total_code) * 100

        svg += f'''
  <text x="40" y="{y_offset}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="13" fill="#c9d1d9">
    {lang}
  </text>
  <rect x="180" y="{y_offset - 12}" width="{max_bar_width}" height="16" fill="#21262d" rx="4"/>
  <rect x="180" y="{y_offset - 12}" width="{bar_width}" height="16" fill="{color}" rx="4" opacity="0.8"/>
  <text x="{180 + max_bar_width + 20}" y="{y_offset}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="12" fill="#8b949e">
    {format_number(code_lines)}
  </text>
  <text x="{svg_width - 40}" y="{y_offset}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="12" fill="#8b949e" text-anchor="end">
    {percentage:.1f}%
  </text>
'''
        y_offset += 25

    svg += '''
  <text x="{}" y="{}" font-family="'SF Mono', 'Monaco', 'Courier New', monospace" font-size="10" fill="#484f58" text-anchor="end">
    Updated automatically via GitHub Actions
  </text>
</svg>'''.format(svg_width - 20, svg_height - 10)

    return svg

def main():
    loc_file = Path('loc-data.json')

    if not loc_file.exists():
        print("Error: loc-data.json not found!", file=sys.stderr)
        sys.exit(1)

    with open(loc_file, 'r') as f:
        loc_data = json.load(f)

    svg_content = generate_svg(loc_data)

    output_path = Path('loc-stats.svg')
    with open(output_path, 'w') as f:
        f.write(svg_content)

    print(f"SVG generated successfully: {output_path}")

if __name__ == '__main__':
    main()
