"""
✈️     TRAVELX : An AI Travel Planner for Students
------------------------------------
A friendly, budget-conscious travel planner that feels like
chatting with a well-traveled friend — not a robot.
"""

import random
import time



GREETINGS = [
    "Hey there, future explorer! 🌍",
    "Oh nice, another adventure incoming! 🎒",
    "Ready to plan something amazing? Let's go! ✈️",
]

THINKING_PHRASES = [
    "Let me think about this for a sec...",
    "Hmm, good question — give me a moment...",
    "Checking my mental travel database... 🗺️",
    "Ooh, this is a fun one. One sec...",
]

DESTINATION_DB = {
    "paris": {
        "country": "France",
        "emoji": "🗼",
        "vibe": "romantic, artsy, café culture",
        "budget_per_day": {"hostel": 45, "food": 25, "transport": 10, "activities": 15},
        "student_tips": [
            "Get the Museum Pass — it covers the Louvre AND saves you €€.",
            "Eat a baguette sandwich from a boulangerie instead of restaurants. Same quality, 1/4 the price.",
            "The Eiffel Tower at night is free to stare at from Trocadéro. Skip the paid climb.",
            "Many museums are FREE on the first Sunday of each month!",
        ],
        "hidden_gems": ["Canal Saint-Martin", "Montmartre staircases", "Palais Royal gardens"],
    },
    "tokyo": {
        "country": "Japan",
        "emoji": "🗾",
        "vibe": "futuristic, food heaven, anime & culture",
        "budget_per_day": {"hostel": 35, "food": 20, "transport": 12, "activities": 18},
        "student_tips": [
            "Get a Suica card on day 1 — works on all trains and convenience stores.",
            "7-Eleven and FamilyMart have restaurant-quality food at 500 yen. Seriously.",
            "Harajuku on a Sunday is free entertainment for hours.",
            "JR Pass is only worth it if you're leaving Tokyo often.",
        ],
        "hidden_gems": ["Shimokitazawa", "Yanaka neighborhood", "Inokashira Park"],
    },
    "barcelona": {
        "country": "Spain",
        "emoji": "🏖️",
        "vibe": "beach, tapas, Gaudí, nightlife",
        "budget_per_day": {"hostel": 30, "food": 20, "transport": 8, "activities": 12},
        "student_tips": [
            "La Boqueria market is touristy — eat at Mercat de l'Abaceria instead.",
            "Many Gaudí buildings let you in free on certain evenings. Check ahead!",
            "Bike rental is cheap and the city is surprisingly flat.",
            "Tapas bars near the university area are half the price of tourist zones.",
        ],
        "hidden_gems": ["Bunkers del Carmel viewpoint", "El Born neighborhood", "Barceloneta at sunset"],
    },
    "bangkok": {
        "country": "Thailand",
        "emoji": "🛕",
        "vibe": "street food, temples, chaos (in the best way)",
        "budget_per_day": {"hostel": 12, "food": 8, "transport": 5, "activities": 10},
        "student_tips": [
            "Take the BTS Skytrain — way faster than tuk-tuks and honest pricing.",
            "Street food from carts is safer AND tastier than sit-down tourist restaurants.",
            "Dress modestly near temples — carry a scarf or they'll turn you away.",
            "Negotiate EVERYTHING at markets except 7-Eleven.",
        ],
        "hidden_gems": ["Chinatown at night", "Chatuchak Weekend Market", "Khlong Lat Mayom floating market"],
    },
    "lisbon": {
        "country": "Portugal",
        "emoji": "🌊",
        "vibe": "laid-back, stunning views, cheap & beautiful",
        "budget_per_day": {"hostel": 25, "food": 15, "transport": 7, "activities": 10},
        "student_tips": [
            "Lisbon is hilly — wear good shoes or regret it immediately.",
            "Pastel de nata from a local bakery: €1.20. Tourist area: €3.50. Same pastry.",
            "The tram 28 is a tourist trap. Take the metro and walk instead.",
            "Student discounts are everywhere — always carry your student ID.",
        ],
        "hidden_gems": ["LX Factory on weekends", "Mouraria neighborhood", "Belém at golden hour"],
    },
}

PACKING_ESSENTIALS = {
    "general": [
        "Universal power adapter 🔌",
        "Microfiber travel towel",
        "Reusable water bottle",
        "Offline maps downloaded (Maps.me)",
        "Photocopies of all documents",
        "Small first aid kit",
    ],
    "europe": ["Schengen documents if needed", "Rail pass (if multi-city)", "Warm layer (even in summer)"],
    "asia": ["Stomach meds (just in case 😅)", "Mosquito repellent", "Cash in local currency from day 1"],
    "beach": ["Reef-safe sunscreen", "Flip flops", "Dry bag for electronics"],
}


# ──────────────────────────────────────────────
#  Helper Functions
# ──────────────────────────────────────────────

def slow_print(text: str, delay: float = 0.03) -> None:
    """Print text with a natural typing rhythm."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def thinking_pause() -> None:
    phrase = random.choice(THINKING_PHRASES)
    print(f"\n  {phrase}", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")
    time.sleep(0.3)


def divider(char="─", length=50) -> None:
    print(f"\n{char * length}\n")


def get_budget_breakdown(destination: str, days: int) -> dict:
    data = DESTINATION_DB[destination]["budget_per_day"]
    return {
        "hostel": data["hostel"] * days,
        "food": data["food"] * days,
        "transport": data["transport"] * days,
        "activities": data["activities"] * days,
        "total": sum(data.values()) * days,
    }


# ──────────────────────────────────────────────
#  Core Features
# ──────────────────────────────────────────────

def display_welcome() -> None:
    divider("═")
    slow_print("  ✈️   AI TRAVEL PLANNER FOR STUDENTS")
    slow_print("       Your broke-but-adventurous companion")
    divider("═")
    print(f"  {random.choice(GREETINGS)}")
    print("  I'll help you plan a real trip — with real student budgets.\n")


def show_destinations() -> None:
    print("  Here's where I can help you plan right now:\n")
    for i, (key, val) in enumerate(DESTINATION_DB.items(), 1):
        print(f"  {i}. {val['emoji']}  {key.capitalize()} ({val['country']}) — {val['vibe']}")
    print()


def plan_trip(destination: str, days: int, travel_style: str) -> None:
    info = DESTINATION_DB[destination]
    budget = get_budget_breakdown(destination, days)

    multipliers = {"budget backpacker": 0.85, "balanced": 1.0, "comfort seeker": 1.35}
    multiplier = multipliers.get(travel_style, 1.0)
    adjusted_total = int(budget["total"] * multiplier)

    divider()
    slow_print(f"  🗺️  YOUR {days}-DAY {destination.upper()} ADVENTURE PLAN")
    divider()

    print(f"  📍 Destination : {destination.capitalize()}, {info['country']} {info['emoji']}")
    print(f"  🎨 Vibe        : {info['vibe'].capitalize()}")
    print(f"  🎒 Your style  : {travel_style.capitalize()}")
    print(f"  📅 Duration    : {days} days\n")

    divider("·")
    slow_print("  💰 BUDGET ESTIMATE (USD)")
    divider("·")
    print(f"  🏠 Accommodation : ~${int(budget['hostel'] * multiplier)}")
    print(f"  🍜 Food          : ~${int(budget['food'] * multiplier)}")
    print(f"  🚌 Transport     : ~${int(budget['transport'] * multiplier)}")
    print(f"  🎭 Activities    : ~${int(budget['activities'] * multiplier)}")
    print(f"  ─────────────────────────────")
    print(f"  💵 TOTAL         : ~${adjusted_total}  (flights not included)")
    print(f"\n  Pro tip: Add ~15% buffer for the 'oops' moments. 😅")

    divider("·")
    slow_print("  🤫 LOCAL STUDENT TIPS")
    divider("·")
    for tip in info["student_tips"]:
        slow_print(f"  ✓ {tip}", delay=0.01)
        print()

    divider("·")
    slow_print("  💎 HIDDEN GEMS (skip the tourist traps)")
    divider("·")
    for gem in info["hidden_gems"]:
        print(f"  → {gem}")

    divider("·")
    slow_print("  🧳 WHAT TO PACK")
    divider("·")
    region = "asia" if destination in ["tokyo", "bangkok"] else "europe" if destination in ["paris", "barcelona", "lisbon"] else "general"
    packing_list = PACKING_ESSENTIALS["general"] + PACKING_ESSENTIALS.get(region, [])
    for item in packing_list:
        print(f"  □ {item}")


def money_saving_tips() -> None:
    divider()
    slow_print("  🪙 UNIVERSAL MONEY-SAVING TIPS FOR STUDENTS")
    divider()
    tips = [
        ("✈️  Flights", "Use Google Flights — set price alerts, fly midweek, book 6-8 weeks out."),
        ("🏠 Accommodation", "Hostel dorms > Airbnb for solo travelers. Use Hostelworld + read recent reviews."),
        ("🍽️  Food", "Lunch menus ('menu del día') are the best value in most countries."),
        ("🎫 Activities", "Always ask for student discounts. Many attractions have free days/hours."),
        ("💳 Money", "Get a Revolut or Wise card. Zero foreign transaction fees. Seriously."),
        ("📱 Data", "Buy a local SIM on arrival — way cheaper than roaming. €5-10 for a week."),
        ("🚌 Transport", "Night buses and trains = save on a hostel night AND travel at once."),
        ("🛡️  Insurance", "Don't skip it. SafetyWing is made for students. ~€1.50/day."),
    ]
    for category, tip in tips:
        slow_print(f"  {category}", delay=0.02)
        print(f"  └─ {tip}\n")


# ──────────────────────────────────────────────
#  Main Application Loop
# ──────────────────────────────────────────────

def get_user_input(prompt: str) -> str:
    return input(f"  {prompt} ").strip().lower()


def main() -> None:
    display_welcome()

    while True:
        print("  What would you like to do?\n")
        print("  1. Plan a trip to a destination")
        print("  2. Browse all destinations")
        print("  3. Get money-saving tips")
        print("  4. Exit\n")

        choice = get_user_input("Your choice (1-4):")

        if choice == "1":
            thinking_pause()
            show_destinations()

            destination_input = get_user_input("Which destination? (type the city name):")
            if destination_input not in DESTINATION_DB:
                print(f"\n  Hmm, I don't have '{destination_input}' yet. Try one from the list above!\n")
                continue

            try:
                days = int(get_user_input("How many days are you planning for?"))
                if days < 1 or days > 60:
                    print("\n  Let's keep it between 1 and 60 days, yeah? 😄\n")
                    continue
            except ValueError:
                print("\n  Just type a number like '7'. Let's try again.\n")
                continue

            print("\n  What's your travel style?\n")
            print("  1. Budget backpacker (stretch every dollar)")
            print("  2. Balanced (comfort where it counts)")
            print("  3. Comfort seeker (nice hostels / occasional splurge)\n")
            style_map = {"1": "budget backpacker", "2": "balanced", "3": "comfort seeker"}
            style_choice = get_user_input("Pick 1, 2, or 3:")
            travel_style = style_map.get(style_choice, "balanced")

            thinking_pause()
            plan_trip(destination_input, days, travel_style)

        elif choice == "2":
            thinking_pause()
            show_destinations()

        elif choice == "3":
            thinking_pause()
            money_saving_tips()

        elif choice in ("4", "exit", "quit", "bye"):
            divider()
            slow_print("  Safe travels, adventurer! 🌏")
            slow_print("  The world is big — go see it. ✈️")
            divider()
            break

        else:
            print("\n  Didn't catch that — just type 1, 2, 3, or 4!\n")
            continue

        print("\n" + "─" * 50)
        again = get_user_input("Anything else? (yes/no):")
        if again not in ("yes", "y", "yeah", "yep", "sure"):
            divider()
            slow_print("  Safe travels, adventurer! 🌏")
            slow_print("  The world is big — go see it. ✈️")
            divider()
            break


if __name__ == "__main__":
    main()
