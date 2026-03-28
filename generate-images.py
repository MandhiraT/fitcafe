#!/usr/bin/env python3
"""
FitCafe Image Generator using Kie.ai Nano Banana 2 API
Generates product and lifestyle images for sales page
"""

import os
import json
import httpx
import base64

# Configuration
KIE_API_KEY = "17bf4cbcc84d27e4667187e3ab4f40a7"
KIE_BASE_URL = "https://api.kie.ai"
OUTPUT_DIR = "assets"

# Image generation prompts for FitCafe sales page
IMAGE_PROMPTS = {
    "hero-product-real.jpg": """
    Professional product photography of premium coffee pouch standing upright on clean marble kitchen counter, 
    soft morning sunlight from side window creating natural shadows, minimal lifestyle setting with single white 
    ceramic coffee cup beside pouch, shallow depth of field, warm neutral color palette (cream, beige, soft brown), 
    commercial product photography style, 9:16 vertical format, high resolution, no text overlay, product label 
    clearly visible and legible, premium wellness coffee packaging
    """,
    
    "morning-ritual.jpg": """
    Lifestyle photography of woman in her 30s sitting at kitchen table in comfortable casual morning attire 
    (light cardigan, soft colors), holding coffee mug with both hands, peaceful contemplative expression, 
    soft natural window light, cozy home kitchen background with plants visible, authentic candid moment, 
    9:16 vertical format, warm inviting atmosphere (cream, soft orange, warm beige tones), no product 
    prominently visible, genuine human emotion, wellness lifestyle aesthetic
    """,
    
    "ingredients-visual.jpg": """
    Flat lay ingredient photography showing six small glass bowls arranged in circle on white marble surface, 
    each containing different natural ingredients: green coffee beans, green tea leaves, white L-Theanine 
    powder, chromium mineral crystals, L-Carnitine powder, Garcinia Cambogia fruit pieces, clean white 
    marble background, overhead shot, professional food photography lighting, 9:16 vertical format, 
    educational style, no text overlay, natural colors (greens, browns, whites), botanical aesthetic
    """,
    
    "work-from-home.jpg": """
    Lifestyle photography of professional woman in her 30s working from home office, sitting at desk with 
    laptop, coffee mug visible on desk (white ceramic), natural daylight from window with sheer curtains, 
    comfortable casual attire (blouse, cardigan), focused productive expression, authentic work-from-home 
    setting with plants and books visible, 9:16 vertical format, warm natural lighting (golden hour), 
    no overt product placement, productivity and wellness theme
    """,
    
    "about-story.jpg": """
    Team lifestyle photography showing diverse group of 3-4 people in modern bright office kitchen preparing 
    coffee together, natural laughter and conversation, casual professional attire, warm inviting atmosphere, 
    natural window lighting, contemporary office setting with plants and modern appliances, authentic 
    team moment, 9:16 vertical format, warm color palette (creams, soft browns, greens), wellness 
    company culture aesthetic, no product prominently featured
    """,
    
    "testimonials-collage.jpg": """
    Collage-style image showing four diverse customer lifestyle moments in quadrants: woman in kitchen 
    smiling with coffee mug (30s), man at home office desk with laptop (40s), woman in activewear 
    post-workout with towel (30s-40s), healthcare professional in scrubs on break (50s), authentic 
    candid moments, warm natural lighting in each quadrant, 9:16 vertical format, no product 
    prominently featured, genuine human emotion, diverse representation
    """,
    
    "guarantee-badge.png": """
    Trust badge and guarantee seal design, circular emblem with "180-Day Money-Back Guarantee" text 
    in bold readable font, clean professional graphic design, shield or ribbon motif, navy blue and 
    gold color scheme (#C05621, #F6E05E), white background, commercial graphic design style, 
    transparent background (PNG), high resolution, no product visible, premium trustworthy aesthetic
    """,
    
    "optin-flatlay.jpg": """
    Minimal flat lay of open notebook with morning routine checklist written, pen beside, coffee cup 
    in corner (white ceramic with steam), soft morning light from side, clean organized desk surface 
    (white or light wood), productivity and wellness theme, 9:16 vertical format, neutral color 
    palette (cream, beige, soft brown), no text overlay, inviting peaceful composition, lifestyle 
    photography style
    """,
    
    "cta-hero.jpg": """
    Hero product lifestyle shot of premium coffee pouch on kitchen counter next to freshly brewed 
    cup of coffee (white ceramic, steam rising), morning sunlight streaming through window creating 
    warm glow, cozy inviting home atmosphere with plants visible, warm color tones (oranges, 
    creams, soft browns), 9:16 vertical format, commercial lifestyle photography, product clearly 
    visible but not overly promotional, authentic morning ritual aesthetic
    """,
    
    "benefits-lifestyle.jpg": """
    Lifestyle photography of woman in her 30s standing by kitchen window in morning light, holding 
    coffee mug, peaceful satisfied expression, comfortable casual attire, plants and natural elements 
    visible, warm golden hour lighting, authentic wellness moment, 9:16 vertical format, warm 
    inviting atmosphere (cream, soft orange, green tones), no product prominently visible, 
    healthy lifestyle aesthetic, genuine contentment
    """
}

def generate_image(prompt_text, output_filename):
    """Generate image using Kie.ai Nano Banana 2 API"""
    
    print(f"🎨 Generating: {output_filename}")
    
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/nano-banana-2",
        "prompt": prompt_text.strip(),
        "aspect_ratio": "9:16",
        "output_format": "png" if output_filename.endswith(".png") else "jpeg",
        "num_images": 1
    }
    
    try:
        response = httpx.post(
            f"{KIE_BASE_URL}/api/v1/jobs/createTask",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        result = response.json()
        
        if result.get("code") == 200:
            task_id = result["data"]["taskId"]
            print(f"  ✅ Task submitted: {task_id}")
            
            # Poll for completion
            return poll_task(task_id, output_filename)
        else:
            print(f"  ❌ Error: {result.get('msg', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def poll_task(task_id, output_filename, max_attempts=60):
    """Poll task status until complete"""
    
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}"
    }
    
    for attempt in range(max_attempts):
        try:
            status_response = httpx.get(
                f"{KIE_BASE_URL}/api/v1/jobs/recordInfo",
                headers=headers,
                params={"taskId": task_id},
                timeout=30
            )
            
            status_result = status_response.json()
            
            if status_result.get("code") == 200:
                state = status_result["data"].get("state", "processing")
                
                if attempt % 10 == 0:
                    print(f"  ⏳ Attempt {attempt + 1}: {state}")
                
                if state == "success":
                    # Extract image URL
                    result_json = status_result["data"].get("resultJson", "{}")
                    if isinstance(result_json, str):
                        result_json = json.loads(result_json)
                    
                    image_urls = result_json.get("resultUrls", [])
                    if image_urls:
                        image_url = image_urls[0]
                        print(f"  ✅ Success! Downloading...")
                        
                        # Download image
                        return download_image(image_url, output_filename)
                    else:
                        print(f"  ❌ No image URLs in response")
                        return None
                elif state == "failed":
                    print(f"  ❌ Failed: {status_result['data'].get('msg', 'Unknown error')}")
                    return None
            else:
                print(f"  ❌ Status check failed: {status_result.get('msg', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error checking status: {e}")
        
        import time
        time.sleep(5)
    
    print(f"  ❌ Timeout after {max_attempts} attempts")
    return None

def download_image(image_url, output_filename):
    """Download image and save to assets folder"""
    
    try:
        response = httpx.get(image_url, timeout=60)
        
        if response.status_code == 200:
            filepath = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content) / (1024 * 1024)  # MB
            print(f"  💾 Saved: {filepath} ({file_size:.2f} MB)")
            return filepath
        else:
            print(f"  ❌ Download failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error downloading: {e}")
        return None

def main():
    """Main function to generate all images"""
    
    print("=" * 60)
    print("FitCafe Image Generator - Nano Banana 2 API")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate each image
    generated = []
    failed = []
    
    for filename, prompt in IMAGE_PROMPTS.items():
        result = generate_image(prompt, filename)
        
        if result:
            generated.append(filename)
        else:
            failed.append(filename)
        
        # Small delay between requests
        import time
        time.sleep(2)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"✅ Generated: {len(generated)}/{len(IMAGE_PROMPTS)}")
    print(f"❌ Failed: {len(failed)}/{len(IMAGE_PROMPTS)}")
    
    if failed:
        print(f"\nFailed images:")
        for f in failed:
            print(f"  - {f}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
