
"""

import os
import sys
import math
import random
import time
import argparse
from pathlib import Path

# ──────────────────────────────────────────────────────────────
#  DATA
# ──────────────────────────────────────────────────────────────

DESTINATIONS = {
    "paris": {
        "country": "France",
        "emoji": "🗼",
        "vibe": "Romantic, artsy, café culture",
        "color": (124, 106, 255),      # violet
        "accent": (179, 157, 219),
        "budget_per_day": {"hostel": 45, "food": 25, "transport": 10, "activities": 15},
        "student_tips": [
            "Get the Museum Pass — covers the Louvre AND saves you €€.",
            "Eat baguette sandwiches from a boulangerie, not restaurants.",
            "Eiffel Tower at night is free to admire from Trocadéro.",
            "Many museums are FREE on the first Sunday of each month!",
        ],
        "hidden_gems": ["Canal Saint-Martin", "Montmartre staircases", "Palais Royal gardens"],
        "highlights": ["Louvre Museum", "Eiffel Tower", "Montmartre", "Seine River Cruise"],
        "best_time": "Apr – Jun, Sep – Oct",
        "language": "French",
        "currency": "EUR €",
    },
    "tokyo": {
        "country": "Japan",
        "emoji": "🗾",
        "vibe": "Futuristic, food heaven, anime & culture",
        "color": (64, 196, 255),       # cyan
        "accent": (100, 220, 255),
        "budget_per_day": {"hostel": 35, "food": 20, "transport": 12, "activities": 18},
        "student_tips": [
            "Get a Suica card on day 1 — works on trains and convenience stores.",
            "7-Eleven & FamilyMart have restaurant-quality food at ¥500.",
            "Harajuku on a Sunday is free entertainment for hours.",
            "JR Pass only worth it if you're leaving Tokyo frequently.",
        ],
        "hidden_gems": ["Shimokitazawa", "Yanaka neighborhood", "Inokashira Park"],
        "highlights": ["Shibuya Crossing", "Senso-ji Temple", "Harajuku", "Akihabara"],
        "best_time": "Mar – May, Sep – Nov",
        "language": "Japanese",
        "currency": "JPY ¥",
    },
    "barcelona": {
        "country": "Spain",
        "emoji": "🏖️",
        "vibe": "Beach, tapas, Gaudí, nightlife",
        "color": (255, 160, 64),       # orange
        "accent": (255, 200, 100),
        "budget_per_day": {"hostel": 30, "food": 20, "transport": 8, "activities": 12},
        "student_tips": [
            "La Boqueria is touristy — eat at Mercat de l'Abaceria instead.",
            "Many Gaudí buildings offer free entry on certain evenings.",
            "Bike rental is cheap and the city is surprisingly flat.",
            "Tapas bars near the university are half the tourist price.",
        ],
        "hidden_gems": ["Bunkers del Carmel viewpoint", "El Born neighborhood", "Barceloneta at sunset"],
        "highlights": ["Sagrada Família", "Park Güell", "La Barceloneta", "Gothic Quarter"],
        "best_time": "May – Jun, Sep – Oct",
        "language": "Spanish / Catalan",
        "currency": "EUR €",
    },
    "bangkok": {
        "country": "Thailand",
        "emoji": "🛕",
        "vibe": "Street food, temples, chaos (in the best way)",
        "color": (255, 215, 64),       # gold
        "accent": (255, 240, 120),
        "budget_per_day": {"hostel": 12, "food": 8, "transport": 5, "activities": 10},
        "student_tips": [
            "Take the BTS Skytrain — faster than tuk-tuks, honest pricing.",
            "Street food from carts is safer AND tastier than tourist restaurants.",
            "Dress modestly near temples — carry a scarf or be turned away.",
            "Negotiate everything at markets except 7-Eleven.",
        ],
        "hidden_gems": ["Chinatown at night", "Chatuchak Weekend Market", "Khlong Lat Mayom floating market"],
        "highlights": ["Wat Arun", "Grand Palace", "Chatuchak Market", "Chao Phraya River"],
        "best_time": "Nov – Feb",
        "language": "Thai",
        "currency": "THB ฿",
    },
    "lisbon": {
        "country": "Portugal",
        "emoji": "🌊",
        "vibe": "Laid-back, stunning views, cheap & beautiful",
        "color": (72, 200, 140),       # teal
        "accent": (120, 230, 170),
        "budget_per_day": {"hostel": 25, "food": 15, "transport": 7, "activities": 10},
        "student_tips": [
            "Lisbon is hilly — wear good shoes or regret it immediately.",
            "Pastel de nata: €1.20 from a local bakery vs €3.50 tourist area.",
            "Tram 28 is a tourist trap. Take the metro and walk instead.",
            "Student discounts are everywhere — always carry your student ID.",
        ],
        "hidden_gems": ["LX Factory on weekends", "Mouraria neighborhood", "Belém at golden hour"],
        "highlights": ["Belém Tower", "Jerónimos Monastery", "Alfama District", "LX Factory"],
        "best_time": "Mar – May, Sep – Oct",
        "language": "Portuguese",
        "currency": "EUR €",
    },
}

PACKING_LISTS = {
    "general": [
        "Universal power adapter 🔌",
        "Microfiber travel towel",
        "Reusable water bottle",
        "Offline maps downloaded (Maps.me)",
        "Photocopies of all documents",
        "Small first aid kit",
    ],
    "europe": ["Schengen documents if needed", "Rail pass (if multi-city)", "Warm layer (even in summer)", "Student ID card"],
    "asia":   ["Stomach meds (just in case 😅)", "Mosquito repellent", "Cash in local currency from day 1", "Translation app downloaded offline"],
    "beach":  ["Reef-safe sunscreen", "Flip flops", "Dry bag for electronics", "Rash guard for water sports"],
}

MONEY_TIPS = [
    ("✈️  Flights",       "Use Google Flights — set price alerts, fly midweek, book 6-8 weeks out."),
    ("🏠  Accommodation", "Hostel dorms beat Airbnb for solo travelers. Use Hostelworld + recent reviews."),
    ("🍽️  Food",          "Lunch menus ('menu del día') are best value in most countries — often 3 courses."),
    ("🎫  Activities",    "Always ask for student discounts. Many attractions have free days/hours."),
    ("💳  Money",         "Get a Revolut or Wise card — zero foreign transaction fees. Game-changer."),
    ("📱  Data & SIM",    "Buy a local SIM on arrival — way cheaper than roaming. €5-10 for a week."),
    ("🚌  Transport",     "Night buses/trains = save on accommodation AND travel at the same time."),
    ("🛡️  Insurance",     "Don't skip it. SafetyWing is built for students at ~€1.50/day."),
]

MULTIPLIERS = {
    "budget backpacker": 0.85,
    "balanced":          1.0,
    "comfort seeker":    1.35,
}

# ──────────────────────────────────────────────────────────────
#  CLI HELPERS
# ──────────────────────────────────────────────────────────────

GREETINGS = [
    "Hey there, future explorer! 🌍",
    "Oh nice, another adventure incoming! 🎒",
    "Ready to plan something amazing? Let's go! ✈️",
]

THINKING = [
    "Let me think about this for a sec...",
    "Hmm, good question — give me a moment...",
    "Checking my mental travel database... 🗺️",
    "Ooh, this is a fun one. One sec...",
]


def slow_print(text: str, delay: float = 0.025) -> None:
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def thinking_pause() -> None:
    phrase = random.choice(THINKING)
    print(f"\n  {phrase}", end="")
    for _ in range(3):
        time.sleep(0.45)
        print(".", end="", flush=True)
    print("\n")
    time.sleep(0.2)


def divider(char: str = "─", length: int = 52) -> None:
    print(f"\n{char * length}\n")


def prompt(text: str) -> str:
    return input(f"  {text} ").strip().lower()


def get_budget(dest: str, days: int, style: str) -> dict:
    b = DESTINATIONS[dest]["budget_per_day"]
    m = MULTIPLIERS.get(style, 1.0)
    return {
        "hostel":     round(b["hostel"]     * days * m),
        "food":       round(b["food"]       * days * m),
        "transport":  round(b["transport"]  * days * m),
        "activities": round(b["activities"] * days * m),
        "total":      round(sum(b.values()) * days * m),
    }


# ──────────────────────────────────────────────────────────────
#  CLI PLANNER
# ──────────────────────────────────────────────────────────────

def cli_welcome() -> None:
    divider("═")
    slow_print("  🌌  TRAVELX — YOUR TRAVEL PLANNER")
    slow_print("       Space-Themed Student Budget Companion")
    divider("═")
    print(f"  {random.choice(GREETINGS)}")
    print("  Real destinations. Real student budgets. No fluff.\n")


def cli_show_destinations() -> None:
    print("  Available destinations:\n")
    for i, (key, d) in enumerate(DESTINATIONS.items(), 1):
        daily = sum(d["budget_per_day"].values())
        print(f"  {i}. {d['emoji']}  {key.capitalize()} ({d['country']})  |  ~${daily}/day  |  {d['vibe']}")
    print()


def cli_plan_trip(dest: str, days: int, style: str) -> None:
    info = DESTINATIONS[dest]
    b    = get_budget(dest, days, style)

    divider()
    slow_print(f"  🗺️  YOUR {days}-DAY {dest.upper()} PLAN  {info['emoji']}")
    divider()

    print(f"  📍 Destination : {dest.capitalize()}, {info['country']}")
    print(f"  🎨 Vibe        : {info['vibe']}")
    print(f"  🎒 Style       : {style.capitalize()}")
    print(f"  📅 Duration    : {days} days")
    print(f"  🗓️  Best time   : {info['best_time']}")
    print(f"  🗣️  Language    : {info['language']}")
    print(f"  💱 Currency    : {info['currency']}\n")

    divider("·")
    slow_print("  💰 BUDGET ESTIMATE (USD, flights not included)")
    divider("·")
    print(f"  🏠 Accommodation : ~${b['hostel']}")
    print(f"  🍜 Food          : ~${b['food']}")
    print(f"  🚌 Transport     : ~${b['transport']}")
    print(f"  🎭 Activities    : ~${b['activities']}")
    print(f"  {'─'*35}")
    print(f"  💵 TOTAL         : ~${b['total']}")
    print(f"\n  💡 Add ~15% buffer for unexpected 'oops' moments 😅")

    divider("·")
    slow_print("  🤫 LOCAL STUDENT TIPS")
    divider("·")
    for tip in info["student_tips"]:
        slow_print(f"  ✓  {tip}", delay=0.012)
        print()

    divider("·")
    slow_print("  💎 HIDDEN GEMS")
    divider("·")
    for gem in info["hidden_gems"]:
        print(f"  →  {gem}")

    divider("·")
    slow_print("  🌟 TOP HIGHLIGHTS")
    divider("·")
    for hl in info["highlights"]:
        print(f"  ★  {hl}")

    region = "asia" if dest in ("tokyo", "bangkok") else "europe" if dest in ("paris", "barcelona", "lisbon") else "general"
    packing = PACKING_LISTS["general"] + PACKING_LISTS.get(region, [])
    divider("·")
    slow_print("  🧳 WHAT TO PACK")
    divider("·")
    for item in packing:
        print(f"  □  {item}")


def run_cli() -> None:
    cli_welcome()
    while True:
        print("  What would you like to do?\n")
        print("  1. Plan a trip")
        print("  2. Browse all destinations")
        print("  3. Universal money-saving tips")
        print("  4. Generate the website (HTML + images)")
        print("  5. Exit\n")

        choice = prompt("Your choice (1-5):")

        if choice == "1":
            thinking_pause()
            cli_show_destinations()
            dest = prompt("Which destination? (type city name):")
            if dest not in DESTINATIONS:
                print(f"\n  ⚠️  '{dest}' not found. Try one from the list above!\n")
                continue
            try:
                days = int(prompt("How many days?"))
                if not 1 <= days <= 60:
                    print("\n  Please enter between 1 and 60 days.\n")
                    continue
            except ValueError:
                print("\n  Just type a number like '7'.\n")
                continue
            print("\n  Travel style?\n")
            print("  1. Budget backpacker")
            print("  2. Balanced")
            print("  3. Comfort seeker\n")
            sm = {"1": "budget backpacker", "2": "balanced", "3": "comfort seeker"}
            style = sm.get(prompt("Pick 1, 2, or 3:"), "balanced")
            thinking_pause()
            cli_plan_trip(dest, days, style)

        elif choice == "2":
            thinking_pause()
            cli_show_destinations()

        elif choice == "3":
            thinking_pause()
            divider()
            slow_print("  🪙 UNIVERSAL MONEY-SAVING TIPS")
            divider()
            for cat, tip in MONEY_TIPS:
                slow_print(f"  {cat}", delay=0.018)
                print(f"  └─ {tip}\n")

        elif choice == "4":
            thinking_pause()
            output_dir = Path("travelx_output")
            generate_all(output_dir)
            print(f"\n  ✅ Generated in: {output_dir.resolve()}\n")

        elif choice in ("5", "exit", "quit", "bye"):
            divider()
            slow_print("  Safe travels, adventurer! 🌏")
            slow_print("  The world is big — go see it. ✈️")
            divider()
            break

        else:
            print("\n  Type 1, 2, 3, 4, or 5 please!\n")
            continue

        print("\n" + "─" * 52)
        again = prompt("Anything else? (yes/no):")
        if again not in ("yes", "y", "yeah", "yep", "sure"):
            divider()
            slow_print("  Safe travels, adventurer! 🌏")
            slow_print("  The world is big — go see it. ✈️")
            divider()
            break


# ──────────────────────────────────────────────────────────────
#  IMAGE CARD GENERATOR  (Pillow)
# ──────────────────────────────────────────────────────────────

def _try_import_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        print("  ⚠️  Pillow not installed. Run: pip install Pillow")
        print("      Skipping image generation.\n")
        return None, None, None


def draw_star(draw, cx, cy, r, color, alpha_img=None):
    """Draw a simple 4-point star / glow dot."""
    from PIL import ImageDraw as ID
    points = []
    for i in range(8):
        angle = math.radians(i * 45)
        radius = r if i % 2 == 0 else r * 0.38
        points.append((cx + radius * math.sin(angle), cy - radius * math.cos(angle)))
    draw.polygon(points, fill=color)


def generate_destination_card(dest_key: str, output_path: Path, Image, ImageDraw, ImageFont) -> None:
    """Generate a stylised reference card image for a destination."""
    from PIL import Image as PILImage

    W, H = 900, 520
    info  = DESTINATIONS[dest_key]
    base_color  = info["color"]
    accent_color = info["accent"]

    # ── Background: deep space gradient ──
    img = PILImage.new("RGB", (W, H), (6, 6, 15))
    draw = ImageDraw.Draw(img)

    # Subtle grid
    grid_color = (20, 20, 40)
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=grid_color, width=1)

    # Nebula glow (right side)
    for radius in range(280, 0, -4):
        alpha = int(80 * (1 - radius / 280))
        r = min(255, base_color[0] + alpha // 4)
        g = min(255, base_color[1] + alpha // 4)
        b = min(255, base_color[2] + alpha // 4)
        draw.ellipse(
            [W - radius + 40, H // 2 - radius, W + radius - 40 + 80, H // 2 + radius],
            fill=(r // 6, g // 6, b // 6)
        )

    # Stars
    rng = random.Random(hash(dest_key))
    for _ in range(220):
        sx, sy = rng.randint(0, W), rng.randint(0, H)
        sr = rng.uniform(0.5, 2.2)
        brightness = rng.randint(100, 220)
        star_col = (brightness, brightness, min(255, brightness + 30))
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=star_col)

    # Accent line left edge
    for i in range(6):
        alpha_val = 255 - i * 35
        c = tuple(min(255, int(v * alpha_val / 255)) for v in base_color)
        draw.rectangle([i, 0, i, H], fill=c)

    # ── Destination name block ──
    pad = 52

    # Try to load a font; fall back gracefully
    def get_font(size):
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except Exception:
            try:
                return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
            except Exception:
                return ImageFont.load_default()

    font_huge  = get_font(72)
    font_large = get_font(26)
    font_med   = get_font(18)
    font_small = get_font(14)

    # Country label (small, muted)
    draw.text((pad, 44), info["country"].upper(), font=font_small,
              fill=(150, 150, 180))

    # City name
    city_name = dest_key.upper()
    draw.text((pad, 68), city_name, font=font_huge,
              fill=(232, 234, 246))

    # Accent glow under city name (simulate text shadow)
    bbox = draw.textbbox((pad, 68), city_name, font=font_huge)
    for gx in range(-2, 3):
        for gy in range(-2, 3):
            draw.text((pad + gx, 68 + gy), city_name, font=font_huge,
                      fill=(*base_color, 30))
    draw.text((pad, 68), city_name, font=font_huge, fill=(232, 234, 246))

    # Vibe tag
    tag_y = 158
    tag_text = f"  {info['vibe']}  "
    tag_bbox = draw.textbbox((pad, tag_y), tag_text, font=font_small)
    draw.rectangle([pad - 2, tag_y - 4, tag_bbox[2] + 4, tag_bbox[3] + 4],
                   fill=(*base_color, 30), outline=(*base_color, 80))
    draw.text((pad, tag_y), tag_text, font=font_small, fill=accent_color)

    # ── Budget strip ──
    budget = info["budget_per_day"]
    daily  = sum(budget.values())
    bstrip_y = 210

    draw.rectangle([pad, bstrip_y, W - pad, bstrip_y + 64],
                   fill=(13, 13, 31), outline=(*base_color, 60))
    draw.text((pad + 18, bstrip_y + 10), "EST. DAILY BUDGET",
              font=font_small, fill=(120, 120, 160))
    draw.text((pad + 18, bstrip_y + 28), f"~${daily} / day",
              font=font_large, fill=(*base_color,))

    cats = [("🏠", f"${budget['hostel']}"), ("🍜", f"${budget['food']}"),
            ("🚌", f"${budget['transport']}"), ("🎭", f"${budget['activities']}")]
    for ci, (icon, amt) in enumerate(cats):
        cx = W - pad - 340 + ci * 88
        draw.text((cx, bstrip_y + 10), icon, font=font_med,  fill=(200, 200, 220))
        draw.text((cx, bstrip_y + 34), amt,  font=font_small, fill=(180, 180, 210))

    # ── Tips section ──
    tips_y = 300
    draw.text((pad, tips_y), "STUDENT TIPS", font=font_small, fill=(*base_color,))
    draw.line([(pad, tips_y + 18), (W - pad, tips_y + 18)],
              fill=(*base_color, 50), width=1)

    for i, tip in enumerate(info["student_tips"][:3]):
        ty = tips_y + 28 + i * 28
        draw.ellipse([pad, ty + 5, pad + 6, ty + 11], fill=(*base_color,))
        short_tip = tip[:80] + ("…" if len(tip) > 80 else "")
        draw.text((pad + 14, ty), short_tip, font=font_small, fill=(180, 180, 210))

    # ── Hidden gems ──
    gems_x = W // 2 + 20
    gems_y = tips_y
    draw.text((gems_x, gems_y), "HIDDEN GEMS", font=font_small, fill=(*accent_color,))
    draw.line([(gems_x, gems_y + 18), (W - pad, gems_y + 18)],
              fill=(*accent_color, 50), width=1)
    for i, gem in enumerate(info["hidden_gems"]):
        gy = gems_y + 28 + i * 28
        draw.text((gems_x, gy), f"→  {gem}", font=font_small, fill=(180, 180, 210))

    # ── Best time + language strip ──
    meta_y = H - 68
    draw.rectangle([0, meta_y, W, H], fill=(8, 8, 22))
    draw.line([(0, meta_y), (W, meta_y)], fill=(*base_color, 60), width=1)

    meta_items = [
        ("BEST TIME TO VISIT", info["best_time"]),
        ("LANGUAGE", info["language"]),
        ("CURRENCY", info["currency"]),
    ]
    for mi, (label, value) in enumerate(meta_items):
        mx = pad + mi * 260
        draw.text((mx, meta_y + 10), label, font=font_small, fill=(100, 100, 140))
        draw.text((mx, meta_y + 28), value, font=font_med,   fill=(220, 220, 240))

    # ── TravelX watermark ──
    draw.text((W - pad - 60, 44), "TravelX", font=font_med, fill=(*base_color, 160))

    img.save(output_path, "PNG", quality=95)
    print(f"  ✅  Saved: {output_path.name}")


def generate_all_images(output_dir: Path) -> None:
    Image, ImageDraw, ImageFont = _try_import_pillow()
    if Image is None:
        return

    img_dir = output_dir / "reference_images"
    img_dir.mkdir(parents=True, exist_ok=True)

    print("\n  🎨 Generating reference destination images...\n")
    for key in DESTINATIONS:
        out_path = img_dir / f"{key}_card.png"
        generate_destination_card(key, out_path, Image, ImageDraw, ImageFont)

    # Also generate a combined overview sheet
    generate_overview_sheet(img_dir, Image, ImageDraw, ImageFont)
    print(f"\n  📁 All images saved to: {img_dir.resolve()}\n")


def generate_overview_sheet(img_dir: Path, Image, ImageDraw, ImageFont) -> None:
    """Generate a single overview sheet showing all 5 destinations side by side."""
    COLS, ROWS   = 3, 2
    CARD_W, CARD_H = 300, 200
    MARGIN       = 12
    BG           = (6, 6, 15)

    sheet_w = COLS * CARD_W + (COLS + 1) * MARGIN
    sheet_h = ROWS * CARD_H + (ROWS + 1) * MARGIN + 60  # header

    sheet = Image.new("RGB", (sheet_w, sheet_h), BG)
    draw  = ImageDraw.Draw(sheet)

    def get_font(size):
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except Exception:
            return ImageFont.load_default()

    fn_title = get_font(22)
    fn_small = get_font(13)

    # Title
    draw.text((MARGIN, MARGIN), "TRAVELX — DESTINATION OVERVIEW",
              font=fn_title, fill=(180, 160, 255))
    draw.text((MARGIN, MARGIN + 30), "5 student-tested destinations · budget-friendly travel planner",
              font=fn_small, fill=(100, 100, 140))

    keys   = list(DESTINATIONS.keys())
    rng    = random.Random(42)

    for idx, key in enumerate(keys):
        info = DESTINATIONS[key]
        col  = idx % COLS
        row  = idx // COLS
        x    = MARGIN + col * (CARD_W + MARGIN)
        y    = 60 + MARGIN + row * (CARD_H + MARGIN)

        # Card background
        base = info["color"]
        draw.rectangle([x, y, x + CARD_W, y + CARD_H],
                       fill=(10, 10, 24), outline=(*base, 80), width=1)

        # Mini nebula
        for r in range(80, 0, -3):
            ex0 = x + CARD_W - r
            ey0 = y + CARD_H // 2 - r
            ex1 = x + CARD_W + max(1, r - 40)
            ey1 = y + CARD_H // 2 + r
            if ex1 > ex0 and ey1 > ey0:
                draw.ellipse([ex0, ey0, ex1, ey1],
                             fill=(base[0] // 10, base[1] // 10, base[2] // 10))

        # Mini stars
        for _ in range(30):
            sx, sy = rng.randint(x, x + CARD_W), rng.randint(y, y + CARD_H)
            sr = rng.uniform(0.5, 1.5)
            b  = rng.randint(100, 200)
            draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(b, b, b))

        # Left color bar
        draw.rectangle([x, y, x + 3, y + CARD_H], fill=base)

        # Text
        draw.text((x + 12, y + 12), info["country"].upper(), font=fn_small, fill=(120, 120, 160))
        draw.text((x + 12, y + 28), key.upper(), font=get_font(28), fill=(232, 234, 246))
        daily = sum(info["budget_per_day"].values())
        draw.text((x + 12, y + 66), f"~${daily}/day", font=fn_small, fill=(*base,))
        # Vibe (truncated)
        vibe = info["vibe"][:34] + ("…" if len(info["vibe"]) > 34 else "")
        draw.text((x + 12, y + 84), vibe, font=fn_small, fill=(140, 140, 170))

        # Best time
        draw.text((x + 12, y + CARD_H - 36), "BEST TIME:", font=fn_small, fill=(90, 90, 120))
        draw.text((x + 12, y + CARD_H - 20), info["best_time"], font=fn_small, fill=(180, 180, 210))

    out_path = img_dir / "overview_all_destinations.png"
    sheet.save(out_path, "PNG")
    print(f"  ✅  Saved: {out_path.name}")


# ──────────────────────────────────────────────────────────────
#  HTML GENERATOR
# ──────────────────────────────────────────────────────────────

def build_html() -> str:
    """Return the full TravelX HTML as a Python string."""

    dest_js_entries = []
    for key, d in DESTINATIONS.items():
        tips_js  = "[" + ",".join(f'"{t}"' for t in d["student_tips"]) + "]"
        gems_js  = "[" + ",".join(f'"{g}"' for g in d["hidden_gems"])  + "]"
        b        = d["budget_per_day"]
        entry = (
            f'  {key}: {{\n'
            f'    country:"{d["country"]}",emoji:"{d["emoji"]}",\n'
            f'    vibe:"{d["vibe"]}",\n'
            f'    budget:{{hostel:{b["hostel"]},food:{b["food"]},transport:{b["transport"]},activities:{b["activities"]}}},\n'
            f'    tips:{tips_js},\n'
            f'    gems:{gems_js}\n'
            f'  }}'
        )
        dest_js_entries.append(entry)

    dest_js = "const DB = {\n" + ",\n".join(dest_js_entries) + "\n};"

    dest_options = "\n".join(
        f'          <option value="{k}">{d["emoji"]} {k.capitalize()}, {d["country"]}</option>'
        for k, d in DESTINATIONS.items()
    )

    money_tip_cards = "\n".join(
        f'  {{ cat: "{cat}", text: "{tip}" }}'
        for cat, tip in MONEY_TIPS
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TravelX — Your Travel Planner</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
  :root{{
    --ink:#e8eaf6;--paper:#06060f;--cream:#0d0d1f;
    --accent:#7c6aff;--accent2:#40c4ff;--gold:#b39ddb;--muted:#8888aa;
  }}
  html{{scroll-behavior:smooth;}}
  body{{font-family:'DM Sans',sans-serif;background:var(--paper);color:var(--ink);overflow-x:hidden;cursor:none;}}
  #starfield{{position:fixed;inset:0;z-index:0;pointer-events:none;}}
  .cursor{{width:12px;height:12px;background:var(--accent);border-radius:50%;position:fixed;pointer-events:none;z-index:9999;transform:translate(-50%,-50%);transition:width .2s,height .2s;mix-blend-mode:screen;}}
  .cursor-ring{{width:36px;height:36px;border:1.5px solid var(--accent);border-radius:50%;position:fixed;pointer-events:none;z-index:9998;transform:translate(-50%,-50%);transition:left .12s ease-out,top .12s ease-out,width .3s,height .3s;}}
  header{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:20px 48px;background:rgba(6,6,15,.75);backdrop-filter:blur(16px);border-bottom:1px solid rgba(124,106,255,.15);}}
  .logo{{font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:.06em;color:var(--ink);display:flex;align-items:center;gap:8px;}}
  .logo span{{color:var(--accent);}}
  nav{{display:flex;gap:32px;}}
  nav a{{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:rgba(232,234,246,.45);text-decoration:none;transition:color .2s;}}
  nav a:hover{{color:var(--accent);}}
  .hero{{min-height:100vh;display:flex;align-items:center;padding:120px 48px 80px;position:relative;overflow:hidden;z-index:1;}}
  .hero-bg{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 75% 40%,rgba(124,106,255,.18) 0%,transparent 65%),radial-gradient(ellipse 50% 50% at 20% 65%,rgba(64,196,255,.10) 0%,transparent 60%);}}
  .hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(124,106,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(124,106,255,.06) 1px,transparent 1px);background-size:60px 60px;mask-image:linear-gradient(to bottom,transparent 0%,black 30%,black 70%,transparent 100%);}}
  .hero-content{{position:relative;max-width:700px;}}
  .hero-tag{{display:inline-flex;align-items:center;gap:8px;font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:var(--accent2);background:rgba(64,196,255,.08);padding:6px 14px;border-radius:2px;margin-bottom:28px;border:1px solid rgba(64,196,255,.2);}}
  .hero-tag::before{{content:'🌌';}}
  h1{{font-family:'Bebas Neue',sans-serif;font-size:clamp(72px,10vw,130px);line-height:.92;letter-spacing:.01em;color:var(--ink);margin-bottom:28px;}}
  h1 em{{color:var(--accent);font-style:normal;text-shadow:0 0 40px rgba(124,106,255,.5);}}
  .hero-sub{{font-size:18px;line-height:1.65;color:var(--muted);font-weight:300;max-width:480px;margin-bottom:44px;}}
  .hero-actions{{display:flex;gap:16px;flex-wrap:wrap;}}
  .btn-primary{{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;background:var(--accent);color:#fff;padding:16px 36px;border:none;border-radius:2px;cursor:none;transition:all .2s;position:relative;overflow:hidden;box-shadow:0 0 24px rgba(124,106,255,.4);}}
  .btn-primary::after{{content:'';position:absolute;inset:0;background:var(--accent2);transform:translateX(-100%);transition:transform .3s ease;}}
  .btn-primary:hover::after{{transform:translateX(0);}}
  .btn-primary span{{position:relative;z-index:1;}}
  .btn-secondary{{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;background:transparent;color:var(--ink);padding:16px 36px;border:1.5px solid rgba(124,106,255,.4);border-radius:2px;cursor:none;transition:all .2s;}}
  .btn-secondary:hover{{background:rgba(124,106,255,.15);border-color:var(--accent);}}
  .hero-float{{position:absolute;right:48px;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:12px;animation:float 6s ease-in-out infinite;}}
  @keyframes float{{0%,100%{{transform:translateY(-50%) translateX(0)}}50%{{transform:translateY(-50%) translateX(-12px)}}}}
  .stat-pill{{background:rgba(13,13,31,.9);border-radius:8px;padding:16px 24px;box-shadow:0 4px 24px rgba(0,0,0,.4),0 0 0 1px rgba(124,106,255,.15);display:flex;gap:14px;align-items:center;backdrop-filter:blur(10px);}}
  .stat-pill .num{{font-family:'Bebas Neue',sans-serif;font-size:32px;color:var(--accent);line-height:1;text-shadow:0 0 16px rgba(124,106,255,.5);}}
  .stat-pill .label{{font-size:12px;color:var(--muted);line-height:1.4;}}
  .stat-pill .icon{{font-size:24px;}}
  section{{padding:100px 48px;position:relative;z-index:1;}}
  .section-label{{font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin-bottom:20px;}}
  h2{{font-family:'Bebas Neue',sans-serif;font-size:clamp(42px,5vw,72px);line-height:1;letter-spacing:.02em;margin-bottom:16px;}}
  #destinations{{background:#08081a;color:var(--paper);}}
  #destinations .section-label{{color:var(--accent);}}
  #destinations h2{{color:var(--paper);}}
  .dest-intro{{color:rgba(245,240,232,.6);font-size:16px;max-width:500px;margin-bottom:60px;}}
  .dest-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:2px;}}
  .dest-card{{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);padding:32px;cursor:none;transition:all .3s;position:relative;overflow:hidden;}}
  .dest-card::before{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,var(--accent),var(--accent2));transform:scaleY(0);transform-origin:bottom;transition:transform .4s cubic-bezier(.16,1,.3,1);z-index:0;}}
  .dest-card:hover::before{{transform:scaleY(1);}}
  .dest-card *{{position:relative;z-index:1;}}
  .dest-card:hover{{color:#fff;}}
  .dest-emoji{{font-size:40px;margin-bottom:16px;display:block;}}
  .dest-name{{font-family:'Bebas Neue',sans-serif;font-size:32px;letter-spacing:.04em;margin-bottom:4px;}}
  .dest-country{{font-size:12px;color:rgba(245,240,232,.5);margin-bottom:12px;}}
  .dest-vibe{{font-size:13px;line-height:1.5;color:rgba(245,240,232,.55);}}
  .dest-card:hover .dest-country,.dest-card:hover .dest-vibe{{color:rgba(255,255,255,.8);}}
  .dest-budget{{margin-top:20px;padding-top:20px;border-top:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:space-between;}}
  .dest-card:hover .dest-budget{{border-top-color:rgba(255,255,255,.3);}}
  .dest-budget-num{{font-family:'Space Mono',monospace;font-size:20px;font-weight:700;}}
  .dest-budget-label{{font-size:11px;color:rgba(245,240,232,.4);}}
  .dest-select-btn{{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.1em;background:rgba(255,255,255,.1);border:none;color:var(--paper);padding:8px 16px;cursor:none;transition:background .2s;}}
  .dest-card:hover .dest-select-btn{{background:rgba(255,255,255,.25);}}
  #planner{{background:var(--cream);}}
  .planner-wrap{{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;max-width:1100px;}}
  .planner-form{{background:#0d0d22;padding:44px;border-radius:4px;box-shadow:0 2px 32px rgba(0,0,0,.4),0 0 0 1px rgba(124,106,255,.12);}}
  .form-group{{margin-bottom:28px;}}
  label{{display:block;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;}}
  select,input[type=number]{{width:100%;padding:14px 16px;border:1.5px solid rgba(124,106,255,.15);border-radius:2px;font-family:'DM Sans',sans-serif;font-size:15px;background:rgba(255,255,255,.04);color:var(--ink);cursor:none;transition:border-color .2s;appearance:none;}}
  select:focus,input[type=number]:focus{{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,106,255,.12);}}
  select option{{background:#0d0d22;}}
  .style-options{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}}
  .style-opt{{border:1.5px solid rgba(124,106,255,.15);border-radius:2px;padding:14px 10px;text-align:center;cursor:none;transition:all .2s;}}
  .style-opt:hover,.style-opt.active{{border-color:var(--accent);background:rgba(124,106,255,.12);box-shadow:0 0 16px rgba(124,106,255,.2);}}
  .style-icon{{font-size:22px;display:block;margin-bottom:6px;}}
  .style-label{{font-size:11px;color:var(--muted);}}
  .days-wrap{{position:relative;}}
  .days-wrap input{{padding-right:60px;}}
  .days-unit{{position:absolute;right:16px;top:50%;transform:translateY(-50%);font-family:'Space Mono',monospace;font-size:11px;color:var(--muted);}}
  #plan-btn{{width:100%;font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:.08em;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;padding:18px;cursor:none;transition:all .2s;border-radius:2px;margin-top:8px;box-shadow:0 0 28px rgba(124,106,255,.4);}}
  #plan-btn:hover{{opacity:.9;transform:translateY(-1px);box-shadow:0 0 40px rgba(124,106,255,.6);}}
  .planner-result{{background:#08081a;color:var(--paper);border-radius:4px;padding:44px;min-height:400px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(124,106,255,.1);box-shadow:inset 0 0 60px rgba(124,106,255,.04);}}
  .result-placeholder{{text-align:center;color:rgba(245,240,232,.25);}}
  .placeholder-icon{{font-size:56px;display:block;margin-bottom:16px;}}
  .result-placeholder p{{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;}}
  .result-content{{width:100%;}}
  .result-dest{{font-family:'Bebas Neue',sans-serif;font-size:48px;letter-spacing:.04em;color:var(--accent);line-height:1;}}
  .result-meta{{font-size:13px;color:rgba(245,240,232,.5);margin-top:6px;margin-bottom:28px;}}
  .budget-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(255,255,255,.06);margin-bottom:20px;border-radius:2px;overflow:hidden;}}
  .budget-item{{background:rgba(255,255,255,.03);padding:18px 20px;}}
  .b-icon{{font-size:18px;margin-bottom:6px;}}
  .b-cat{{font-size:10px;font-family:'Space Mono',monospace;color:rgba(245,240,232,.4);text-transform:uppercase;letter-spacing:.1em;}}
  .b-amt{{font-family:'Bebas Neue',sans-serif;font-size:28px;color:var(--paper);}}
  .budget-total{{background:linear-gradient(135deg,var(--accent),var(--accent2));padding:20px 24px;display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;border-radius:2px;box-shadow:0 0 30px rgba(124,106,255,.3);}}
  .t-label{{font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.12em;}}
  .t-amt{{font-family:'Bebas Neue',sans-serif;font-size:44px;line-height:1;}}
  .result-section{{margin-bottom:20px;}}
  .result-section-title{{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:var(--gold);margin-bottom:12px;display:flex;align-items:center;gap:8px;}}
  .result-section-title::after{{content:'';flex:1;height:1px;background:rgba(255,255,255,.08);}}
  .tip-item{{font-size:13px;line-height:1.6;color:rgba(245,240,232,.75);padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05);display:flex;gap:10px;}}
  .tip-item::before{{content:'→';color:var(--accent);flex-shrink:0;}}
  .gem-item{{display:inline-block;margin:4px;padding:6px 14px;background:rgba(179,157,219,.12);border:1px solid rgba(179,157,219,.2);border-radius:2px;font-size:12px;color:var(--gold);font-family:'Space Mono',monospace;}}
  #tips{{background:var(--cream);}}
  .tips-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;margin-top:56px;}}
  .tip-card{{background:#0d0d22;padding:32px;border-radius:4px;border:1px solid rgba(124,106,255,.1);transition:all .3s;position:relative;}}
  .tip-card::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));transform:scaleX(0);transform-origin:left;transition:transform .3s;}}
  .tip-card:hover{{transform:translateY(-4px);box-shadow:0 12px 40px rgba(124,106,255,.15),0 0 0 1px rgba(124,106,255,.2);}}
  .tip-card:hover::after{{transform:scaleX(1);}}
  .tip-cat{{font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:.06em;margin-bottom:10px;}}
  .tip-text{{font-size:14px;line-height:1.65;color:var(--muted);}}
  #packing{{background:#06060f;color:var(--paper);}}
  #packing h2{{color:var(--paper);}}
  #packing .section-label{{color:var(--accent);}}
  .packing-intro{{color:rgba(232,234,246,.45);font-size:15px;max-width:480px;margin-bottom:48px;}}
  .pack-tabs{{display:flex;gap:2px;margin-bottom:36px;flex-wrap:wrap;}}
  .pack-tab{{font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.12em;padding:10px 20px;background:rgba(124,106,255,.06);border:1px solid rgba(124,106,255,.12);color:rgba(232,234,246,.4);cursor:none;transition:all .2s;}}
  .pack-tab.active,.pack-tab:hover{{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 0 16px rgba(124,106,255,.4);}}
  .pack-list{{display:flex;flex-direction:column;gap:12px;}}
  .pack-item{{display:flex;align-items:center;gap:14px;padding:16px 20px;background:rgba(124,106,255,.04);border:1px solid rgba(124,106,255,.08);border-radius:2px;cursor:none;transition:all .2s;}}
  .pack-item:hover{{background:rgba(124,106,255,.08);border-color:rgba(124,106,255,.2);}}
  .pack-check{{width:20px;height:20px;border:1.5px solid rgba(124,106,255,.3);border-radius:2px;flex-shrink:0;transition:all .2s;display:flex;align-items:center;justify-content:center;}}
  .pack-item.checked .pack-check{{background:var(--accent);border-color:var(--accent);box-shadow:0 0 10px rgba(124,106,255,.5);}}
  .pack-item.checked .pack-check::after{{content:'✓';font-size:12px;color:#fff;}}
  .pack-item.checked span{{text-decoration:line-through;color:rgba(232,234,246,.25);}}
  .pack-item span{{font-size:14px;color:rgba(232,234,246,.75);}}
  footer{{background:#04040c;color:rgba(232,234,246,.3);padding:48px;text-align:center;border-top:1px solid rgba(124,106,255,.1);}}
  .footer-logo{{font-family:'Bebas Neue',sans-serif;font-size:36px;letter-spacing:.06em;color:var(--paper);margin-bottom:12px;}}
  .footer-logo span{{color:var(--accent);}}
  .toast{{position:fixed;bottom:32px;right:32px;z-index:1000;background:#0d0d22;color:var(--paper);padding:14px 24px;border-radius:4px;font-size:13px;border-left:3px solid var(--accent);transform:translateX(120%);transition:transform .4s cubic-bezier(.16,1,.3,1);font-family:'Space Mono',monospace;}}
  .toast.show{{transform:translateX(0);}}
  @keyframes fadeUp{{from{{opacity:0;transform:translateY(24px)}}to{{opacity:1;transform:translateY(0)}}}}
  .fade-up{{animation:fadeUp .7s ease forwards;}}
  .fade-up-2{{animation:fadeUp .7s .15s ease both;}}
  .fade-up-3{{animation:fadeUp .7s .3s ease both;}}
  .fade-up-4{{animation:fadeUp .7s .45s ease both;}}
  @media(max-width:900px){{
    header{{padding:16px 24px;}}
    nav{{display:none;}}
    section{{padding:72px 24px;}}
    .hero{{padding:100px 24px 60px;}}
    .hero-float{{display:none;}}
    .planner-wrap{{grid-template-columns:1fr;}}
    h1{{font-size:60px;}}
  }}
</style>
</head>
<body>
<canvas id="starfield"></canvas>
<div class="cursor" id="cursor"></div>
<div class="cursor-ring" id="cursorRing"></div>
<div class="toast" id="toast"></div>

<header>
  <div class="logo">Travel<span>X</span></div>
  <nav>
    <a href="#destinations">Destinations</a>
    <a href="#planner">Plan Trip</a>
    <a href="#tips">Save Money</a>
    <a href="#packing">Packing</a>
  </nav>
</header>

<!-- HERO -->
<section class="hero" id="home">
  <div class="hero-bg"></div>
  <div class="hero-grid"></div>
  <div class="hero-content">
    <div class="hero-tag fade-up">Student-Friendly Travel</div>
    <h1 class="fade-up-2">YOUR<br><em>WORLD</em><br>AWAITS</h1>
    <p class="hero-sub fade-up-3">Smart budget planning for student explorers. Real destinations, real prices — no illusions, just adventure.</p>
    <div class="hero-actions fade-up-4">
      <button class="btn-primary" onclick="document.getElementById('planner').scrollIntoView({{behavior:'smooth'}})">
        <span>Plan My Trip →</span>
      </button>
      <button class="btn-secondary" onclick="document.getElementById('destinations').scrollIntoView({{behavior:'smooth'}})">
        Browse Destinations
      </button>
    </div>
  </div>
  <div class="hero-float">
    <div class="stat-pill"><span class="icon">✈️</span><div><div class="num">5</div><div class="label">Top Student<br>Destinations</div></div></div>
    <div class="stat-pill"><span class="icon">💵</span><div><div class="num">$8</div><div class="label">Min budget<br>per day</div></div></div>
    <div class="stat-pill"><span class="icon">🗺️</span><div><div class="num">∞</div><div class="label">Hidden gems<br>discovered</div></div></div>
  </div>
</section>

<!-- DESTINATIONS -->
<section id="destinations">
  <div class="section-label">Where to go</div>
  <h2>PICK YOUR<br>NEXT ADVENTURE</h2>
  <p class="dest-intro">Five student-tested destinations with real budget breakdowns and insider knowledge.</p>
  <div class="dest-grid" id="destGrid"></div>
</section>

<!-- PLANNER -->
<section id="planner">
  <div class="section-label">Build your budget</div>
  <h2>PLAN YOUR TRIP</h2>
  <div class="planner-wrap" style="margin-top:52px">
    <div class="planner-form">
      <div class="form-group">
        <label>Destination</label>
        <select id="destSelect">
          <option value="">— Select a city —</option>
{dest_options}
        </select>
      </div>
      <div class="form-group">
        <label>Duration</label>
        <div class="days-wrap">
          <input type="number" id="daysInput" min="1" max="60" placeholder="7" value="7">
          <span class="days-unit">days</span>
        </div>
      </div>
      <div class="form-group">
        <label>Travel Style</label>
        <div class="style-options">
          <div class="style-opt active" data-style="budget backpacker" onclick="selectStyle(this)">
            <span class="style-icon">🎒</span><div class="style-label">Budget</div>
          </div>
          <div class="style-opt" data-style="balanced" onclick="selectStyle(this)">
            <span class="style-icon">⚖️</span><div class="style-label">Balanced</div>
          </div>
          <div class="style-opt" data-style="comfort seeker" onclick="selectStyle(this)">
            <span class="style-icon">🌟</span><div class="style-label">Comfort</div>
          </div>
        </div>
      </div>
      <button id="plan-btn" onclick="generatePlan()">GENERATE MY PLAN →</button>
    </div>
    <div class="planner-result" id="planResult">
      <div class="result-placeholder">
        <span class="placeholder-icon">🗺️</span>
        <p>Your plan will appear here</p>
      </div>
    </div>
  </div>
</section>

<!-- MONEY TIPS -->
<section id="tips">
  <div class="section-label">Stretch your budget</div>
  <h2>UNIVERSAL<br>MONEY TIPS</h2>
  <div class="tips-grid" id="tipsGrid"></div>
</section>

<!-- PACKING -->
<section id="packing">
  <div class="section-label">Don't forget</div>
  <h2>PACKING<br>CHECKLIST</h2>
  <p class="packing-intro">Tap items to check them off. Filter by region.</p>
  <div class="pack-tabs" id="packTabs">
    <button class="pack-tab active" data-region="general" onclick="switchPack(this)">General</button>
    <button class="pack-tab" data-region="europe" onclick="switchPack(this)">Europe</button>
    <button class="pack-tab" data-region="asia" onclick="switchPack(this)">Asia</button>
    <button class="pack-tab" data-region="beach" onclick="switchPack(this)">Beach</button>
  </div>
  <div class="pack-list" id="packList"></div>
</section>

<footer>
  <div class="footer-logo">Travel<span>X</span></div>
  <p>Your broke-but-adventurous companion. The world is big — go see it. ✈️</p>
</footer>

<!-- STARFIELD -->
<script>
(function(){{
  const canvas=document.getElementById('starfield');
  const ctx=canvas.getContext('2d');
  let W,H,stars=[],shootingStars=[];
  function resize(){{W=canvas.width=window.innerWidth;H=canvas.height=document.body.scrollHeight;}}
  function initStars(){{
    stars=[];
    const count=Math.floor((W*H)/4000);
    for(let i=0;i<count;i++){{
      stars.push({{
        x:Math.random()*W,y:Math.random()*H,
        r:Math.random()*1.4+0.2,
        alpha:Math.random()*0.7+0.2,
        twinkleSpeed:Math.random()*0.02+0.005,
        twinklePhase:Math.random()*Math.PI*2,
        color:Math.random()<0.15?'#b39ddb':Math.random()<0.1?'#40c4ff':'#e8eaf6'
      }});
    }}
  }}
  function addShootingStar(){{
    if(Math.random()>0.003)return;
    shootingStars.push({{x:Math.random()*W,y:Math.random()*H*0.4,len:Math.random()*120+60,speed:Math.random()*6+4,alpha:1,angle:Math.PI/4+(Math.random()-0.5)*0.3,life:1}});
  }}
  let t=0;
  function draw(){{
    ctx.clearRect(0,0,W,H);
    const nb=[
      {{x:W*0.75,y:H*0.1,r:320,c:'rgba(124,106,255,0.055)'}},
      {{x:W*0.15,y:H*0.25,r:250,c:'rgba(64,196,255,0.04)'}},
      {{x:W*0.5,y:H*0.5,r:400,c:'rgba(179,157,219,0.03)'}},
    ];
    nb.forEach(n=>{{
      const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r);
      g.addColorStop(0,n.c);g.addColorStop(1,'transparent');
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,Math.PI*2);ctx.fill();
    }});
    stars.forEach(s=>{{
      const tw=Math.sin(t*s.twinkleSpeed+s.twinklePhase)*0.3+0.7;
      ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx.fillStyle=s.color;ctx.globalAlpha=s.alpha*tw;ctx.fill();ctx.globalAlpha=1;
    }});
    addShootingStar();
    shootingStars=shootingStars.filter(s=>s.life>0);
    shootingStars.forEach(s=>{{
      ctx.save();ctx.translate(s.x,s.y);ctx.rotate(s.angle);
      const g=ctx.createLinearGradient(-s.len,0,0,0);
      g.addColorStop(0,'transparent');g.addColorStop(1,`rgba(255,255,255,${{s.life*0.9}})`);
      ctx.strokeStyle=g;ctx.lineWidth=1.5;ctx.globalAlpha=s.alpha;
      ctx.beginPath();ctx.moveTo(-s.len,0);ctx.lineTo(0,0);ctx.stroke();
      ctx.globalAlpha=1;ctx.restore();
      s.x+=Math.cos(s.angle)*s.speed;s.y+=Math.sin(s.angle)*s.speed;
      s.life-=0.018;s.alpha=s.life;
    }});
    t++;requestAnimationFrame(draw);
  }}
  window.addEventListener('resize',()=>{{resize();initStars();}});
  setTimeout(()=>{{resize();initStars();draw();}},100);
}})();
</script>

<script>
{dest_js}

const PACKING={{
  general:["Universal power adapter 🔌","Microfiber travel towel","Reusable water bottle","Offline maps downloaded","Photocopies of all documents","Small first aid kit"],
  europe:["Schengen documents if needed","Rail pass (if multi-city)","Warm layer (even in summer)","Student ID card"],
  asia:["Stomach meds (just in case 😅)","Mosquito repellent","Cash in local currency from day 1","Translation app downloaded offline"],
  beach:["Reef-safe sunscreen","Flip flops","Dry bag for electronics","Rash guard for water sports"]
}};

const TIPS=[
{money_tip_cards}
];

const MULTIPLIERS={{"budget backpacker":0.85,"balanced":1.0,"comfort seeker":1.35}};
let selectedStyle="budget backpacker";

const cursor=document.getElementById('cursor');
const ring=document.getElementById('cursorRing');
document.addEventListener('mousemove',e=>{{
  cursor.style.left=e.clientX+'px';cursor.style.top=e.clientY+'px';
  ring.style.left=e.clientX+'px';ring.style.top=e.clientY+'px';
}});
document.querySelectorAll('button,a,select,input,.dest-card,.tip-card,.pack-item,.style-opt,.pack-tab').forEach(el=>{{
  el.addEventListener('mouseenter',()=>{{cursor.style.width='18px';cursor.style.height='18px';ring.style.width='52px';ring.style.height='52px';}});
  el.addEventListener('mouseleave',()=>{{cursor.style.width='12px';cursor.style.height='12px';ring.style.width='36px';ring.style.height='36px';}});
}});

function showToast(msg){{
  const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),3000);
}}

function renderDests(){{
  const grid=document.getElementById('destGrid');
  for(const [key,d] of Object.entries(DB)){{
    const daily=Object.values(d.budget).reduce((a,b)=>a+b,0);
    const card=document.createElement('div');card.className='dest-card';
    card.innerHTML=`<span class="dest-emoji">${{d.emoji}}</span>
      <div class="dest-name">${{key.charAt(0).toUpperCase()+key.slice(1)}}</div>
      <div class="dest-country">${{d.country}}</div>
      <div class="dest-vibe">${{d.vibe}}</div>
      <div class="dest-budget">
        <div><div class="dest-budget-num">~$${{daily}}/day</div><div class="dest-budget-label">estimated budget</div></div>
        <button class="dest-select-btn" onclick="selectDest('${{key}}')">Plan This →</button>
      </div>`;
    grid.appendChild(card);
  }}
}}

function selectDest(key){{
  document.getElementById('destSelect').value=key;
  document.getElementById('planner').scrollIntoView({{behavior:'smooth'}});
  showToast(`${{key.charAt(0).toUpperCase()+key.slice(1)}} selected! Fill in the details below.`);
}}

function selectStyle(el){{
  document.querySelectorAll('.style-opt').forEach(o=>o.classList.remove('active'));
  el.classList.add('active');selectedStyle=el.dataset.style;
}}

function generatePlan(){{
  const dest=document.getElementById('destSelect').value;
  const days=parseInt(document.getElementById('daysInput').value)||7;
  if(!dest){{showToast('⚠️ Please select a destination first!');return;}}
  if(days<1||days>60){{showToast('⚠️ Days must be between 1 and 60.');return;}}
  const d=DB[dest];const m=MULTIPLIERS[selectedStyle];const b=d.budget;
  const hostel=Math.round(b.hostel*days*m),food=Math.round(b.food*days*m);
  const transport=Math.round(b.transport*days*m),activities=Math.round(b.activities*days*m);
  const total=hostel+food+transport+activities;
  document.getElementById('planResult').innerHTML=`<div class="result-content">
    <div class="result-dest">${{dest.toUpperCase()}} ${{d.emoji}}</div>
    <div class="result-meta">${{days}} days · ${{selectedStyle}} · ${{d.country}}</div>
    <div class="budget-grid">
      <div class="budget-item"><div class="b-icon">🏠</div><div class="b-cat">Accommodation</div><div class="b-amt">$${{hostel}}</div></div>
      <div class="budget-item"><div class="b-icon">🍜</div><div class="b-cat">Food</div><div class="b-amt">$${{food}}</div></div>
      <div class="budget-item"><div class="b-icon">🚌</div><div class="b-cat">Transport</div><div class="b-amt">$${{transport}}</div></div>
      <div class="budget-item"><div class="b-icon">🎭</div><div class="b-cat">Activities</div><div class="b-amt">$${{activities}}</div></div>
    </div>
    <div class="budget-total">
      <div><div class="t-label">Total Estimate</div><div style="font-size:11px;opacity:.7;font-family:monospace">Flights not included</div></div>
      <div class="t-amt">$${{total}}</div>
    </div>
    <div class="result-section">
      <div class="result-section-title">✦ Local Student Tips</div>
      ${{d.tips.map(t=>`<div class="tip-item">${{t}}</div>`).join('')}}
    </div>
    <div class="result-section">
      <div class="result-section-title">💎 Hidden Gems</div>
      <div>${{d.gems.map(g=>`<span class="gem-item">${{g}}</span>`).join('')}}</div>
    </div>
    <p style="font-size:11px;color:rgba(245,240,232,.3);font-family:'Space Mono',monospace;margin-top:20px">
      Pro tip: Add ~15% buffer for the 'oops' moments 😅
    </p>
  </div>`;
  showToast(`Plan ready for ${{dest.charAt(0).toUpperCase()+dest.slice(1)}}!`);
}}

function renderTips(){{
  const grid=document.getElementById('tipsGrid');
  TIPS.forEach(t=>{{
    const c=document.createElement('div');c.className='tip-card';
    c.innerHTML=`<div class="tip-cat">${{t.cat}}</div><p class="tip-text">${{t.text}}</p>`;
    grid.appendChild(c);
  }});
}}

let checkedItems=new Set();
function switchPack(btn){{
  document.querySelectorAll('.pack-tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');renderPack(btn.dataset.region);
}}
function renderPack(region){{
  const list=document.getElementById('packList');list.innerHTML='';
  (PACKING[region]||[]).forEach((item,i)=>{{
    const id=`${{region}}-${{i}}`;
    const el=document.createElement('div');
    el.className='pack-item'+(checkedItems.has(id)?' checked':'');
    el.innerHTML=`<div class="pack-check"></div><span>${{item}}</span>`;
    el.onclick=()=>{{
      if(checkedItems.has(id))checkedItems.delete(id);else checkedItems.add(id);
      el.classList.toggle('checked');
    }};
    list.appendChild(el);
  }});
}}

renderDests();renderTips();renderPack('general');

const io=new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{if(e.isIntersecting){{e.target.style.opacity='1';e.target.style.transform='translateY(0)';}}}}
  );
}},{{threshold:0.1}});
document.querySelectorAll('.dest-card,.tip-card').forEach(el=>{{
  el.style.opacity='0';el.style.transform='translateY(20px)';
  el.style.transition='opacity .5s ease,transform .5s ease';io.observe(el);
}});
</script>
</body>
</html>"""


# ──────────────────────────────────────────────────────────────
#  ORCHESTRATOR
# ──────────────────────────────────────────────────────────────

def generate_all(output_dir: Path = Path("travelx_output")) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. HTML
    print("\n  📄 Generating travelx.html …")
    html_path = output_dir / "travelx.html"
    html_path.write_text(build_html(), encoding="utf-8")
    print(f"  ✅  Saved: {html_path}")

    # 2. Images
    generate_all_images(output_dir)

    print(f"\n  🚀 All done! Open {output_dir / 'travelx.html'} in your browser.\n")


# ──────────────────────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TravelX — Space-Themed Student Travel Planner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python travelx.py                 # Generate website + reference images
  python travelx.py --cli           # Interactive CLI travel planner
  python travelx.py --html-only     # Generate HTML only
  python travelx.py --images-only   # Generate Pillow image cards only
  python travelx.py --output ./out  # Custom output directory
        """
    )
    parser.add_argument("--cli",         action="store_true", help="Run interactive CLI planner")
    parser.add_argument("--html-only",   action="store_true", help="Generate HTML only")
    parser.add_argument("--images-only", action="store_true", help="Generate image cards only")
    parser.add_argument("--output",      default="travelx_output", help="Output directory (default: travelx_output)")

    args = parser.parse_args()
    output_dir = Path(args.output)

    if args.cli:
        run_cli()
    elif args.html_only:
        output_dir.mkdir(parents=True, exist_ok=True)
        html_path = output_dir / "travelx.html"
        html_path.write_text(build_html(), encoding="utf-8")
        print(f"\n  ✅ HTML generated: {html_path.resolve()}\n")
    elif args.images_only:
        generate_all_images(output_dir)
    else:
        # Default: generate everything
        print("\n  🌌 TravelX — Generating website & reference images...\n")
        generate_all(output_dir)


if __name__ == "__main__":
    main()
