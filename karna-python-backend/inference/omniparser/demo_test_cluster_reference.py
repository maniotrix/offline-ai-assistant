
import json
import csv
import statistics
import numpy as np # type: ignore
from sklearn.cluster import DBSCAN
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io
import base64




# ----------------------------------------------------------------------------
# 1. LOAD THE IMAGE EARLY (to obtain dimensions)
# ----------------------------------------------------------------------------
image = Image.open("test.png").convert("RGB")
img_width, img_height = image.size

# ----------------------------------------------------------------------------
# 2. LOAD YOLO DATA
# ----------------------------------------------------------------------------
with open("inference.json", "r", encoding="utf-8") as f:
    yolo_data = json.load(f)
yolo_boxes = yolo_data.get("boundingBoxes", [])
# Compute center coordinates for YOLO boxes
for box in yolo_boxes:
    box["x_center"] = box["x"] + box["width"] / 2
    box["y_center"] = box["y"] + box["height"] / 2
    box["source"] = "yolo"
    # Use the YOLO "class" as text label for visualization.
    box["text"] = box.get("class", "")

# ----------------------------------------------------------------------------
# 3. LOAD Tesseract OCR DATA
# ----------------------------------------------------------------------------
ocr_boxes = []
with open("out.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        txt = row.get("text", "").strip()
        if not txt:
            continue
        try:
            left = float(row["left"])
            top = float(row["top"])
            w = float(row["width"])
            h = float(row["height"])
        except:
            continue
        cx = left + w / 2
        cy = top + h / 2
        ocr_boxes.append({
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "x_center": cx,
            "y_center": cy,
            "text": txt,
            "source": "ocr",
            "is_search": ("search" in txt.lower())
        })

# ----------------------------------------------------------------------------
# 4. COMBINE BOXES INTO A COMMON LIST (Normalization)
# ----------------------------------------------------------------------------
all_boxes = []
# Normalize YOLO boxes into common format.
for b in yolo_boxes:
    all_boxes.append({
        "left": b["x"],
        "top": b["y"],
        "width": b["width"],
        "height": b["height"],
        "x_center": b["x_center"],
        "y_center": b["y_center"],
        "source": "yolo",
        "text": b.get("text", ""),
        "is_search": False
    })
# Add OCR boxes as they are.
for b in ocr_boxes:
    all_boxes.append(b)

# ----------------------------------------------------------------------------
# 5. VERTICAL CLUSTERING (Group elements into rows based on y_center)
# ----------------------------------------------------------------------------
Y = np.array([[box["y_center"]] for box in all_boxes])
heights = [box["height"] for box in all_boxes]
median_height = statistics.median(heights) if heights else 50
vertical_eps = median_height * 1.5  # dynamic threshold for vertical clustering
dbscan_vert = DBSCAN(eps=vertical_eps, min_samples=1)  # allow isolated boxes
vert_labels = dbscan_vert.fit_predict(Y)
for i, box in enumerate(all_boxes):
    box["vert_cluster"] = int(vert_labels[i])

# Group boxes by vertical cluster ID
vert_clusters = {}
for box in all_boxes:
    cid = box["vert_cluster"]
    vert_clusters.setdefault(cid, []).append(box)

# For each vertical cluster, compute its overall bounding box and average y_center.
cluster_info = []
for cid, boxes in vert_clusters.items():
    xs = [b["left"] for b in boxes]
    ys = [b["top"] for b in boxes]
    xs2 = [b["left"] + b["width"] for b in boxes]
    ys2 = [b["top"] + b["height"] for b in boxes]
    cluster_bbox = {
        "left": min(xs),
        "top": min(ys),
        "right": max(xs2),
        "bottom": max(ys2)
    }
    avg_y = statistics.mean([b["y_center"] for b in boxes])
    cluster_info.append((cid, avg_y, cluster_bbox, boxes))
# Sort clusters top-to-bottom
cluster_info = sorted(cluster_info, key=lambda x: x[1])

# ----------------------------------------------------------------------------
# 6. ASSIGN VERTICAL REGION LABELS (HEADER, FOOTER, MIDDLE)
# ----------------------------------------------------------------------------
num_vclusters = len(cluster_info)
for idx, (cid, avg_y, bbox, boxes) in enumerate(cluster_info):
    # If only one vertical cluster, call it "middle".
    if num_vclusters == 1:
        v_label = "middle"
    else:
        # Top cluster as header, bottom cluster as footer.
        if idx == 0:
            v_label = "header"
        elif idx == num_vclusters - 1:
            v_label = "footer"
        else:
            v_label = "middle"
    for b in boxes:
        b["vert_region"] = v_label
    # Update cluster_info with vertical label.
    cluster_info[idx] = (cid, avg_y, bbox, boxes, v_label)

# ----------------------------------------------------------------------------
# 7. HORIZONTAL CLUSTERING WITHIN EACH VERTICAL CLUSTER
# ----------------------------------------------------------------------------
# For each vertical cluster, cluster by x_center.
for cluster_tuple in cluster_info:
    cid, avg_y, bbox, boxes, v_label = cluster_tuple
    X = np.array([[b["x_center"]] for b in boxes])
    widths = [b["width"] for b in boxes]
    median_width = statistics.median(widths) if widths else 50
    horizontal_eps = median_width * 1.5
    dbscan_horiz = DBSCAN(eps=horizontal_eps, min_samples=1)
    horiz_labels = dbscan_horiz.fit_predict(X)
    for i, b in enumerate(boxes):
        b["horiz_cluster"] = int(horiz_labels[i])
    # Group by horizontal cluster
    horiz_groups = {}
    for b in boxes:
        hcid = b["horiz_cluster"]
        horiz_groups.setdefault(hcid, []).append(b)
    # For each horizontal group, compute average x_center.
    horiz_info = []
    for hcid, hboxes in horiz_groups.items():
        avg_x = statistics.mean([b["x_center"] for b in hboxes])
        horiz_info.append((hcid, avg_x, hboxes))
    # Sort horizontal groups from left to right.
    horiz_info = sorted(horiz_info, key=lambda x: x[1])
    num_hgroups = len(horiz_info)
    for j, (hcid, avg_x, hboxes) in enumerate(horiz_info):
        # Default assignment: leftmost is "left", rightmost "right", others "center".
        if num_hgroups == 1:
            h_label = "center"
        else:
            if j == 0:
                h_label = "left"
            elif j == num_hgroups - 1:
                h_label = "right"
            else:
                h_label = "center"
        # *** NEW CHECK: For vertical 'middle' clusters, only assign 'left' if the group
        # actually touches the left image boundary.
        if h_label == "left" and v_label == "middle":
            group_min_x = min(b["left"] for b in hboxes)
            if group_min_x > 0.05 * img_width:
                # If the left group's minimum x is not very close to the left edge,
                # then reassign this horizontal group as 'center'.
                h_label = "center"
        # Save the horizontal region and combined region for each box.
        for b in hboxes:
            b["horiz_region"] = h_label
            b["combined_region"] = f"{b['vert_region']} {h_label}"
            # ----------------------------------------------------------------------------
            # 8. ASSIGN FINAL LAYOUT CLASS BASED ON VERTICAL & HORIZONTAL GROUPS
            # ----------------------------------------------------------------------------
            # If the vertical region is header or footer, that takes precedence.
            if b["vert_region"] in ["header", "footer"]:
                layout = b["vert_region"]
            else:
                # Otherwise, map horizontal region.
                if h_label == "left":
                    layout = "navigation/menu"
                elif h_label == "right":
                    layout = "sidebar"
                else:
                    layout = "main content"
            # Override if OCR text includes "search".
            if b.get("is_search", False):
                layout = "search area"
            b["layout_class"] = layout

# ----------------------------------------------------------------------------
# 9. VISUALIZATION: DRAW BOXES ON THE IMAGE
# ----------------------------------------------------------------------------
draw = ImageDraw.Draw(image)
# Define colors for each layout class.
layout_colors = {
    "header": "red",
    "footer": "blue",
    "navigation/menu": "green",
    "sidebar": "orange",
    "main content": "yellow",
    "search area": "black"
}
# Try to load a font.
try:
    font = ImageFont.truetype("arial.ttf", 12)
except:
    font = None

# Draw each box with a label showing its combined region and final layout class.
for b in all_boxes:
    x, y, w, h = b["left"], b["top"], b["width"], b["height"]
    layout = b.get("layout_class", "main content")
    color = layout_colors.get(layout, "white")
    draw.rectangle([x, y, x+w, y+h], outline=color, width=2)
    label = f"{b.get('text','')}\n[{b.get('combined_region','')}] -> {layout}"
    draw.text((x, max(y-15, 0)), label, fill=color, font=font)

# ----------------------------------------------------------------------------
# 10. DISPLAY AND OUTPUT THE FINAL IMAGE
# ----------------------------------------------------------------------------
plt.figure(figsize=(12, 8))
plt.imshow(image)
plt.axis("off")
plt.title("Robust UI Layout Classification")
plt.show()

# Output a base64 preview (truncated) for inline display.
buffered = io.BytesIO()
image.save(buffered, format="PNG")
img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
preview_len = 800  # truncate for brevity
truncated_b64 = img_base64[:preview_len] + "..." if len(img_base64) > preview_len else img_base64
print("\n=== Base64-Encoded Preview (Truncated) ===")
print("data:image/png;base64," + truncated_b64)



