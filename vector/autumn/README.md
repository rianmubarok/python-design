# 🍂 Vector Autumn — Pattern Collection

Abstract seamless vector patterns with an **autumn / fall / harvest** theme.  
Each pattern uses the **glyph silhouette** style: solid black shapes with white detail lines on a white background.

---

## Specs

| Property | Value |
|---|---|
| Canvas size | 4000 × 4000 px |
| Resolution | 300 DPI |
| Color mode | Black & White |
| Style | Glyph / Silhouette |
| Formats | JPG · SVG · EPS |
| Total patterns | 28 |
| Date created | 23 September 2026 |

---

## Pattern List

### Single Object Patterns

| # | Pattern Name | Object | Grid Layout |
|---|---|---|---|
| 01 | abstract autumn acorn glyph solid checkerboard grid | Acorn | Checkerboard |
| 02 | abstract autumn apple glyph solid polka dot grid | Apple | Polka Dot |
| 03 | abstract autumn campfire glyph solid checkerboard grid | Campfire | Checkerboard |
| 04 | abstract autumn chestnut nut glyph solid offset grid | Chestnut | Offset |
| 05 | abstract autumn corncob glyph solid basketweave grid | Corncob | Basketweave |
| 06 | abstract autumn ginkgo leaf glyph solid scallop grid | Ginkgo Leaf | Scallop |
| 07 | abstract autumn kite glyph solid alternate rotate grid | Kite | Alternate Rotate |
| 08 | abstract autumn maple leaf glyph solid grid rotate | Maple Leaf | Rotate |
| 09 | abstract autumn mushroom glyph solid half drop grid | Mushroom | Half Drop |
| 10 | abstract autumn oak leaf glyph solid hex grid | Oak Leaf | Hexagonal |
| 11 | abstract autumn owl glyph solid half drop grid | Owl | Half Drop |
| 12 | abstract autumn pear fruit glyph solid staggered grid | Pear | Staggered |
| 13 | abstract autumn pie slice glyph solid hex grid | Pie Slice | Hexagonal |
| 14 | abstract autumn pinecone glyph solid brick layout grid | Pinecone | Brick |
| 15 | abstract autumn pomegranate glyph solid hex grid | Pomegranate | Hexagonal |
| 16 | abstract autumn pumpkin glyph solid diamond grid | Pumpkin | Diamond |
| 17 | abstract autumn scarecrow glyph solid square grid | Scarecrow | Square |
| 18 | abstract autumn simple leaf glyph solid vertical stripe grid | Simple Leaf | Vertical Stripe |
| 19 | abstract autumn sunflower glyph solid square grid | Sunflower | Square |
| 20 | abstract autumn sweater knitwear glyph solid brick grid | Sweater (Knitwear) | Brick |
| 21 | abstract autumn umbrella glyph solid offset drop grid | Umbrella | Offset Drop |
| 22 | abstract autumn wheat stalk glyph solid herringbone grid | Wheat Stalk | Herringbone |

### Composite / Multi-Object Patterns

| # | Pattern Name | Objects Combined | Grid Layout |
|---|---|---|---|
| 23 | abstract autumn ginkgo apple glyph solid checkerboard grid | Ginkgo Leaf + Apple | Checkerboard |
| 24 | abstract autumn owl pinecone glyph solid staggered grid | Owl + Pinecone | Staggered |
| 25 | abstract autumn pie pomegranate chestnut glyph solid staggered row grid | Pie + Pomegranate + Chestnut | Staggered Row |
| 26 | abstract autumn pumpkin wheat glyph solid checkerboard grid | Pumpkin + Wheat | Checkerboard |
| 27 | abstract autumn scarecrow sunflower corncob glyph solid alternating row grid | Scarecrow + Sunflower + Corncob | Alternating Row |
| 28 | abstract autumn sweater umbrella glyph solid half drop grid | Sweater + Umbrella | Half Drop |

---

## File Structure

```
autumn/
├── code/                        # Python generation scripts (matplotlib)
│   └── abstract autumn *.py
├── output/
│   ├── jpg/                     # 4000×4000px JPG previews
│   ├── svg/                     # Scalable Vector Graphics
│   └── eps/                     # EPS (PostScript) for print/submission
├── submitted/                   # Files already uploaded to marketplaces
├── trash/                       # Rejected/replaced drafts
├── convert_svg_to_eps.py        # SVG → EPS batch converter (cairosvg)
└── README.md                    # This file
```

---

## Grid Layout Types Used

| Layout | Description |
|---|---|
| Square | Regular grid, uniform spacing |
| Checkerboard | Alternating positions in diagonal offset |
| Brick / Offset | Every other row shifted by half spacing |
| Half Drop | Every other column shifted by half spacing |
| Diamond | 45° rotated square grid |
| Hexagonal | Honeycomb-style tessellation |
| Herringbone | Zigzag brick arrangement |
| Scallop | Fan/arc-staggered arrangement |
| Basketweave | Alternating 90° rotations in grid |
| Staggered | Random-offset rows for organic feel |
| Alternating Row | Objects alternate per row |
| Vertical Stripe | Vertical column arrangement |
| Polka Dot | Loose scattered circle-like placement |
| Rotate / Alternate Rotate | Objects rotated at each position |

---

## Object Glossary

| Object | Description |
|---|---|
| Acorn | Oak acorn with cap and ribbing |
| Apple | Round apple with leaf and stem |
| Campfire | Crossed logs, flame tongues, stone ring, sparks |
| Chestnut | Spiky chestnut burr nut |
| Corncob | Corn ear with husk leaves and kernel rows |
| Ginkgo Leaf | Fan-shaped ginkgo with veins |
| Kite | Diamond kite with tail and bows |
| Maple Leaf | 5-lobed maple leaf with veins |
| Mushroom | Cap mushroom with gills |
| Oak Leaf | Lobed oak leaf with veins |
| Owl | Stylized owl with feather detail and eyebrows |
| Pear | Rounded pear with stem and leaf |
| Pie Slice | Wedge-shaped pie slice with crust lines |
| Pinecone | Oval pinecone with scale layers |
| Pomegranate | Round pomegranate with crown and seeds |
| Pumpkin | Ribbed pumpkin with stem |
| Scarecrow | Hat, flannel patches, stick arms |
| Simple Leaf | Single oval leaf with central vein |
| Sunflower | Round flower with petal ring and seed center |
| Sweater | Turtleneck sweater with cable-knit detail |
| Umbrella | Canopy umbrella with ribs and handle |
| Wheat Stalk | Wheat ear with grain rows and awns |

---

## Tools & Dependencies

```
Python 3.x
matplotlib
numpy
cairosvg        # SVG → EPS conversion
```

---

## Generation

Each pattern is generated by running its corresponding Python script:

```bash
python "abstract autumn [object] glyph solid [grid] pattern black white texture.py"
```

To convert all SVGs to EPS:

```bash
python convert_svg_to_eps.py
```
