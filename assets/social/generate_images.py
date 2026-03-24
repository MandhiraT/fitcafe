#!/usr/bin/env python3
"""Generate FitCafe social media images using Google Gemini API"""

import httpx
import os
import base64
import time

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
BASE_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={GOOGLE_API_KEY}'
OUTPUT_DIR = '/home/mandhira/.openclaw/workspace-jarvis/projects/WL-FitCafe/website/assets/social'

images = [
    {
        "filename": "instagram-product.jpg",
        "prompt": "Stylish flat lay of FitCafe coffee bag on marble surface with green leaves, morning light, aesthetic coffee cup beside it, warm earth tones, Instagram-worthy product photography, clean minimalist style",
        "size": "1080x1080px",
        "alt": "FitCafe weight loss coffee product flat lay on marble surface with green leaves and morning light"
    },
    {
        "filename": "instagram-morning.jpg",
        "prompt": "Aesthetic morning scene with coffee cup, soft natural light from window, woman's hands holding coffee mug, cozy home atmosphere, warm neutral tones, lifestyle photography for weight loss wellness brand",
        "size": "1080x1080px",
        "alt": "Woman holding FitCafe coffee mug in cozy morning light by window, wellness lifestyle photography"
    },
    {
        "filename": "facebook-lifestyle.jpg",
        "prompt": "Split lifestyle comparison: left side shows stressed tired woman with regular coffee, right side shows relaxed glowing confident woman with wellness coffee, warm professional photography, aspirational lifestyle",
        "size": "1200x630px",
        "alt": "Before and after lifestyle comparison showing transformation with FitCafe wellness coffee"
    },
    {
        "filename": "pinterest-ingredients.jpg",
        "prompt": "Clean infographic-style illustration showing 6 natural ingredients (green coffee bean, green tea, L-Theanine, chromium, L-carnitine, Garcinia Cambogia) arranged beautifully, soft green and brown color palette, health and wellness aesthetic, Pinterest-worthy",
        "size": "1000x1500px",
        "alt": "FitCafe natural ingredients infographic: green coffee bean, green tea, L-Theanine, chromium, L-carnitine, Garcinia Cambogia"
    },
    {
        "filename": "story-cta.jpg",
        "prompt": "Minimalist phone wallpaper style image for weight loss coffee brand, coffee cup with steam, text space at top and bottom, warm brown and cream gradient background, premium wellness brand aesthetic",
        "size": "1080x1920px",
        "alt": "FitCafe weight loss coffee Instagram Story with coffee cup steam on warm brown cream gradient background"
    }
]

results = []

for img in images:
    print(f"\n🎨 Generating: {img['filename']} ({img['size']})...")
    
    payload = {
        'contents': [{'parts': [{'text': img['prompt']}]}],
        'generationConfig': {'responseModalities': ['TEXT', 'IMAGE']}
    }
    
    try:
        r = httpx.post(BASE_URL, json=payload, timeout=120)
        data = r.json()
        
        if r.status_code != 200:
            print(f"  ❌ API error {r.status_code}: {data}")
            results.append({"file": img['filename'], "status": "FAILED", "error": str(data)})
            continue
        
        # Extract image from response
        image_saved = False
        for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
            if 'inlineData' in part:
                img_bytes = base64.b64decode(part['inlineData']['data'])
                filepath = os.path.join(OUTPUT_DIR, img['filename'])
                with open(filepath, 'wb') as f:
                    f.write(img_bytes)
                file_size = len(img_bytes)
                print(f"  ✅ Saved: {img['filename']} ({file_size:,} bytes)")
                results.append({
                    "file": img['filename'],
                    "size": img['size'],
                    "file_size_bytes": file_size,
                    "alt": img['alt'],
                    "status": "OK"
                })
                image_saved = True
                break
        
        if not image_saved:
            # Check for text response
            text_parts = [p.get('text', '') for p in data.get('candidates', [{}])[0].get('content', {}).get('parts', []) if 'text' in p]
            print(f"  ⚠️  No image in response. Text: {' '.join(text_parts)[:200]}")
            results.append({"file": img['filename'], "status": "NO_IMAGE", "response": str(data)[:300]})
        
        # Rate limit: wait between requests
        time.sleep(3)
        
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        results.append({"file": img['filename'], "status": "ERROR", "error": str(e)})

# Print summary
print("\n" + "="*60)
print("📊 GENERATION REPORT")
print("="*60)
for r in results:
    if r['status'] == 'OK':
        print(f"✅ {r['file']}")
        print(f"   Size: {r['size']} | File: {r['file_size_bytes']:,} bytes")
        print(f"   Alt: {r['alt']}")
    else:
        print(f"❌ {r['file']} — {r['status']}")
        if 'error' in r:
            print(f"   Error: {r.get('error', '')[:200]}")

print("\nDone!")
