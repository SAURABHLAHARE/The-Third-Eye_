from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def enhance_caption(caption):
    caption = caption.lower()

    if "stair" in caption or "stairs" in caption:
        return {"object": "stairs", "message": "Stairs ahead. Be careful."}

    elif "chair" in caption:
        return {"object": "chair", "message": "Chair ahead."}

    elif "table" in caption:
        return {"object": "table", "message": "Table ahead."}

    elif "person" in caption:
        return {"object": "person", "message": "Person ahead."}

    elif "car" in caption or "vehicle" in caption:
        return {
            "object": "vehicle",
            "message": "Warning! Vehicle approaching. Stay alert."
        }

    elif "door" in caption:
        return {"object": "door", "message": "Door ahead."}

    else:
        return {"object": "unknown", "message": f"I see {caption}"}


# ===== MAIN FUNCTION =====
def analyze_scene(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=20)

    caption = processor.decode(output[0], skip_special_tokens=True)

    return enhance_caption(caption)