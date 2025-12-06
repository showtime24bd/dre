
#!/usr/bin/env python3
"""
Script to automatically add image URLs to all emotes in index.html
using data from emotes_full.json
"""

import json
import re

# Load emotes_full.json
with open('emotes_full.json', 'r') as f:
    emotes_data = json.load(f)

# Create a mapping of emote ID to image URL
emote_id_to_url = {}
for emote in emotes_data['emotes']:
    emote_id_to_url[emote['id']] = emote['url']

print(f"✅ Loaded {len(emote_id_to_url)} emote image URLs")

# Now you can manually add these to your emoteMapping
# Or use this reference:
print("\n📋 Sample mappings you can copy:")
print("\nExample for AK47 (ID: 909000063):")
ak_url = emote_id_to_url.get('909000063', 'Not found')
print(f"  img: '{ak_url}'")

print("\nExample for Level 100 (ID: 909042007):")
l100_url = emote_id_to_url.get('909042007', 'Not found')
print(f"  img: '{l100_url}'")

print("\n💡 Quick Reference - All Weapon Emotes:")
weapon_ids = {
    'ak': '909000063',
    'm10': '909000081', 
    'scar': '909000068',
    'xm8': '909000085',
    'famas': '909000090',
    'ump': '909000098',
    'mp5': '909033002',
    'm4a1': '909033001',
}

for name, emote_id in weapon_ids.items():
    url = emote_id_to_url.get(emote_id, 'Not found')
    print(f"  '{name}': img: '{url}'")

print("\n🎯 To add images to your HTML:")
print("1. Open templates/index.html")
print("2. Find each emote definition")
print("3. Add: img: 'URL_FROM_ABOVE'")
print("\nExample:")
print("  'ak': { id: '909000063', icon: '🔫', name: 'AK47', img: 'https://...' }")
