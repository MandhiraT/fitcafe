#!/usr/bin/env python3
"""
FitCafe Image Generator using Google Gemini 2.0 Flash Image API
Direct API call without Kie.ai wrapper
"""

import os
import json
import httpx
import base64
import time

# Configuration
# IMPORTANT: Store API key in environment variable or .env file (NOT in code!)
# export GOOGLE_API_KEY="your-api-key-here"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set. Please set environment variable.")

# Use Nano Banana (Gemini 2.5 Flash Image) - supports generateContent
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

OUTPUT_DIR = "assets"

# Image prompts for FitCafe sales page
IMAGE_PROMPTS = {
    "hero-product-real.jpg": """
    Professional product photography of a premium wellness coffee pouch standing upright on a clean white marble kitchen counter. 
    Soft morning sunlight streaming from a side window creating natural gentle shadows. 
    Minimal lifestyle setting with a single white ceramic coffee cup with steam beside the pouch. 
    Shallow depth of field with blurred background. 
    Warm neutral color palette: cream, beige, soft brown, warm orange tones. 
    Commercial product photography style, high resolution, studio quality lighting. 
    Product label clearly visible showing "FitCafe" brand name in elegant typography. 
    No text overlay on image. 9:16 vertical format (portrait orientation).
    """,
    
    "morning-ritual.jpg": """
    Lifestyle photography of a woman in her 30s sitting at a bright modern kitchen table. 
    She is wearing comfortable casual morning attire: a soft light cardigan in cream or beige color. 
    Holding a white ceramic coffee mug with both hands in a peaceful contemplative pose. 
    Soft natural window light from the side creating a warm glow on her face. 
    Cozy home kitchen background with green plants visible on countertops. 
    Authentic candid moment, genuine relaxed expression. 
    9:16 vertical format. Warm inviting color atmosphere: cream, soft orange, warm beige, light brown tones. 
    No product prominently visible. Wellness lifestyle aesthetic, morning routine vibe.
    """,
    
    "ingredients-visual.jpg": """
    Flat lay ingredient photography showing six small clear glass bowls arranged in a circle on a clean white marble surface. 
    Each bowl contains different natural ingredients: 
    - Green coffee beans (whole beans)
    - Green tea leaves (dried)
    - White L-Theanine powder (fine crystalline)
    - Chromium mineral crystals (metallic grey)
    - L-Carnitine powder (white)
    - Garcinia Cambogia dried fruit pieces (brown-orange)
    
    Overhead shot from directly above. Professional food photography lighting with soft shadows. 
    Clean minimalist aesthetic. 9:16 vertical format. 
    Natural colors: greens, browns, whites, earth tones. 
    Botanical wellness aesthetic. No text overlay.
    """,
    
    "work-from-home.jpg": """
    Lifestyle photography of a professional woman in her 30s working from her home office. 
    She is sitting at a modern wooden desk with a laptop computer open. 
    A white ceramic coffee mug is visible on the desk near the laptop. 
    Natural daylight streaming through a window with sheer white curtains. 
    She is wearing comfortable work-from-home attire: a light blouse or cardigan in neutral colors. 
    Focused but relaxed productive expression. 
    Authentic work-from-home setting with houseplants and books visible on shelves in background. 
    9:16 vertical format. Warm natural lighting with golden hour tones. 
    No overt product placement. Productivity and wellness lifestyle theme.
    """,
    
    "about-story.jpg": """
    Team lifestyle photography showing a diverse group of 3-4 people in a modern bright office kitchen area. 
    They are preparing coffee together and having natural conversation with genuine laughter. 
    Casual professional attire: button-down shirts, blouses, smart casual wear. 
    Warm inviting atmosphere with natural window lighting. 
    Contemporary office setting with modern appliances, green plants, and light wood accents. 
    Authentic team bonding moment, candid smiles and interaction. 
    9:16 vertical format. Warm color palette: creams, soft browns, greens, warm neutrals. 
    No product prominently featured. Wellness company culture aesthetic, team collaboration vibe.
    """,
    
    "testimonials-collage.jpg": """
    Collage-style composite image showing four diverse customer lifestyle moments arranged in a 2x2 grid quadrants:
    
    Top-left: Woman in her 30s in a bright kitchen smiling while holding a coffee mug, natural morning light
    Top-right: Man in his 40s at a home office desk with laptop, focused productive expression
    Bottom-left: Woman in her 30s-40s in activewear post-workout with a towel, satisfied smile
    Bottom-right: Healthcare professional woman in her 50s wearing scrubs on a break, warm trustworthy expression
    
    Each quadrant shows authentic candid moments with warm natural lighting. 
    Diverse representation in age, gender, and ethnicity. 
    9:16 vertical format overall. 
    No product prominently featured in any quadrant. 
    Genuine human emotion, relatable customer stories aesthetic.
    """,
    
    "guarantee-badge.png": """
    Professional trust badge and guarantee seal design. 
    Circular emblem with clean modern typography reading "180-DAY MONEY-BACK GUARANTEE" in bold readable sans-serif font. 
    Shield or ribbon motif incorporated into the design. 
    Color scheme: navy blue (#C05621 warm orange-brown) and gold (#F6E05E warm yellow). 
    White or transparent background. 
    Commercial graphic design style, high resolution vector-style appearance. 
    Clean professional trustworthy aesthetic. 
    Square format suitable for web use. 
    No product visible, just the guarantee badge/seal itself.
    """,
    
    "optin-flatlay.jpg": """
    Minimal flat lay photography of an open notebook or journal on a clean white or light wood desk surface. 
    The notebook shows a handwritten morning routine checklist with items like "meditate", "exercise", "healthy breakfast". 
    A nice pen is placed beside the notebook. 
    A white ceramic coffee cup with visible steam is in the corner of the frame. 
    Soft morning light from the side creating gentle shadows. 
    Clean organized minimalist desk surface. 
    Productivity and wellness theme. 
    9:16 vertical format. 
    Neutral color palette: cream, beige, soft brown, white, light wood tones. 
    No text overlay. Inviting peaceful composition, lifestyle photography style.
    """,
    
    "cta-hero.jpg": """
    Hero product lifestyle shot for call-to-action section. 
    Premium coffee pouch standing on a modern kitchen counter next to a freshly brewed cup of coffee in a white ceramic mug with visible steam rising. 
    Morning sunlight streaming through a large window creating a warm inviting glow throughout the scene. 
    Cozy home atmosphere with green houseplants visible in the background. 
    Warm color tones: oranges, creams, soft browns, warm neutrals. 
    9:16 vertical format. 
    Commercial lifestyle photography style. 
    Product clearly visible but not overly promotional or salesy. 
    Authentic morning ritual aesthetic, warm and inviting mood.
    """,
    
    "benefits-lifestyle.jpg": """
    Lifestyle photography of a woman in her 30s standing by a large kitchen window in warm morning light. 
    She is holding a white ceramic coffee mug with both hands in a relaxed pose. 
    Peaceful satisfied expression with a gentle smile, eyes looking out the window thoughtfully. 
    Comfortable casual attire in soft neutral colors. 
    Green houseplants and natural elements visible in the background. 
    Warm golden hour lighting creating a soft glow. 
    Authentic wellness moment, calm and content mood. 
    9:16 vertical format. 
    Warm inviting atmosphere: cream, soft orange, green, warm beige tones. 
    No product prominently visible. Healthy lifestyle aesthetic, mindfulness and wellbeing theme.
    """
}

def generate_image_with_gemini(prompt_text, output_filename):
    """Generate image using Google Gemini 2.0 Flash Image API"""
    
    print(f"🎨 Generating: {output_filename}")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    # Gemini 2.0 Flash Image generation request
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt_text.strip()
            }]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
        }
    }
    
    params = {"key": GOOGLE_API_KEY}
    
    try:
        response = httpx.post(
            GEMINI_URL,
            headers=headers,
            params=params,
            json=payload,
            timeout=60
        )
        
        result = response.json()
        
        # Check for errors
        if "error" in result:
            error_msg = result["error"].get("message", "Unknown error")
            print(f"  ❌ Error: {error_msg}")
            return None
        
        # Extract image from response
        candidates = result.get("candidates", [])
        if not candidates:
            print(f"  ❌ No candidates in response")
            return None
        
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        
        image_data = None
        for part in parts:
            if "inlineData" in part:
                image_data = part["inlineData"]
                break
        
        if not image_data:
            print(f"  ❌ No image data in response")
            return None
        
        # Decode base64 image
        mime_type = image_data.get("mimeType", "image/jpeg")
        image_base64 = image_data.get("data", "")
        
        if not image_base64:
            print(f"  ❌ Empty image data")
            return None
        
        image_bytes = base64.b64decode(image_base64)
        
        # Save image
        filepath = os.path.join(OUTPUT_DIR, output_filename)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        file_size = len(image_bytes) / (1024 * 1024)  # MB
        print(f"  💾 Saved: {filepath} ({file_size:.2f} MB)")
        return filepath
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def main():
    """Main function to generate all images"""
    
    print("=" * 60)
    print("FitCafe Image Generator - Google Gemini 2.0 Flash")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate each image
    generated = []
    failed = []
    
    for filename, prompt in IMAGE_PROMPTS.items():
        result = generate_image_with_gemini(prompt, filename)
        
        if result:
            generated.append(filename)
        else:
            failed.append(filename)
        
        # Delay between requests to avoid rate limits
        time.sleep(3)
    
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
