import os
import json
import xml.etree.ElementTree as ET
import re
from PIL import Image

NS = {"pc": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"}

XML_RE = re.compile(r"(.+)_P(\d+)\.xml$", re.IGNORECASE)

def parse_points(points_str):
    return [[int(x), int(y)] for x, y in
            (p.split(",") for p in points_str.split())]

def parse_text_equiv(element):
    text_equiv = element.find("pc:TextEquiv", NS)
    if text_equiv is not None:
        unicode_el = text_equiv.find("pc:Unicode", NS)
        if unicode_el is not None and unicode_el.text:
            return unicode_el.text
    return ""

def parse_text_line(line_el, scale_x=1.0, scale_y=1.0):
    coords = line_el.find("pc:Coords", NS)
    if coords is None:
        return None
    points = parse_points(coords.attrib["points"])
    scaled_points = [[int(x * scale_x), int(y * scale_y)] for x, y in points]
    return {
        "id": line_el.attrib.get("id", ""),
        "type": "TextLine",
        "points": scaled_points,
        "text": parse_text_equiv(line_el)
    }

def parse_text_region(region_el, scale_x=1.0, scale_y=1.0):
    coords = region_el.find("pc:Coords", NS)
    if coords is None:
        return None
    points = parse_points(coords.attrib["points"])
    scaled_points = [[int(x * scale_x), int(y * scale_y)] for x, y in points]
    region = {
        "id": region_el.attrib.get("id", ""),
        "type": "TextRegion",
        "points": scaled_points,
        "text": parse_text_equiv(region_el),
        "textLines": []
    }
    for line_el in region_el.findall("pc:TextLine", NS):
        line = parse_text_line(line_el, scale_x, scale_y)
        if line:
            region["textLines"].append(line)
    return region

def parse_page_xml(xml_path, image_path, page_number, actual_img_width=None, actual_img_height=None):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    page_el = root.find(".//pc:Page", NS)
    if page_el is None:
        raise ValueError(f"No Page element found in {xml_path}")

    xml_width = int(page_el.attrib["imageWidth"])
    xml_height = int(page_el.attrib["imageHeight"])
    scale_x = actual_img_width / xml_width if actual_img_width else 1.0
    scale_y = actual_img_height / xml_height if actual_img_height else 1.0

    page = {
        "page": page_number,
        "width": actual_img_width or xml_width,
        "height": actual_img_height or xml_height,
        "image": image_path,
        "textRegions": []
    }
    for region_el in page_el.findall("pc:TextRegion", NS):
        region = parse_text_region(region_el, scale_x, scale_y)
        if region:
            page["textRegions"].append(region)
    return page

def process_date_folder(date_folder_path, newspaper_name, date_folder):
    files = os.listdir(date_folder_path)

    # images/ está dentro de la carpeta de fecha
    images_folder = os.path.join(date_folder_path, "images")

    xmls = {}

    for f in files:
        xml_match = XML_RE.match(f)
        if xml_match:
            base = xml_match.group(1)
            page = int(xml_match.group(2))
            xmls.setdefault(base, []).append((page, f))

    for base, pages_list in xmls.items():
        out_path = os.path.join(date_folder_path, f"{base}.json")
        if os.path.exists(out_path):
            print(f"Ya existe: {base}.json, saltando...")
            continue

        pages = []
        osd_tiles = []

        for page_num, xml_file in sorted(pages_list):
            xml_path = os.path.join(date_folder_path, xml_file)
            image_filename = os.path.splitext(xml_file)[0] + ".jpg"

            # Ruta relativa actualizada
            image_path = f"objects/newspapers/{newspaper_name}/{date_folder}/images/{image_filename}"
            full_image_path = os.path.join(images_folder, image_filename)

            actual_width, actual_height = None, None
            try:
                img = Image.open(full_image_path)
                actual_width, actual_height = img.width, img.height
                print(f"  Imagen: {image_filename} ({actual_width}x{actual_height})")
            except Exception as e:
                print(f"  No se pudo abrir {full_image_path}: {e}")

            try:
                page_data = parse_page_xml(xml_path, image_path, page_num, actual_width, actual_height)
                pages.append(page_data)
                osd_tiles.append({"type": "image", "url": image_path, "buildPyramid": True})
            except Exception as e:
                print(f"  Error parseando {xml_file}: {e}")
                continue

        if not pages:
            print(f"  No se generaron páginas para {base}")
            continue

        output = {
            "id": base,
            "pages": pages,
            "tileSources": osd_tiles
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"  Generado: {out_path}")


def main():
    ROOT = r"./objects/newspapers"

    print("=" * 60)
    print("PAGE XML to JSON Converter")
    print("=" * 60)

    for newspaper_name in os.listdir(ROOT):
        newspaper_path = os.path.join(ROOT, newspaper_name)
        if not os.path.isdir(newspaper_path):
            continue

        print(f"\nCabecera: {newspaper_name}")

        for date_folder in os.listdir(newspaper_path):
            date_folder_path = os.path.join(newspaper_path, date_folder)
            if not os.path.isdir(date_folder_path):
                continue

            print(f"  Fecha: {date_folder}")
            process_date_folder(date_folder_path, newspaper_name, date_folder)

if __name__ == "__main__":
    main()