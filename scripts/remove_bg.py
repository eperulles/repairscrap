from PIL import Image
import os

def remove_background(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
    
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Si es muy blanco (r, g, b > 240), hacerlo transparente
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Processed: {output_path}")

if __name__ == "__main__":
    assets_dir = "assets"
    remove_background(os.path.join(assets_dir, "pcba_item.png"), os.path.join(assets_dir, "pcba_item.png"))
    remove_background(os.path.join(assets_dir, "medidor_item.png"), os.path.join(assets_dir, "medidor_item.png"))
