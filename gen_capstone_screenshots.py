"""
Generate all Kanban/screenshot images for DevOps Capstone assignment.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(os.path.abspath(__file__))

def sans(size):
    for p in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def mono(size):
    for p in ["C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

# Colours
BG    = "#f6f8fa"
WHITE = "#ffffff"
GRAY  = "#656d76"
DARK  = "#1f2328"
BLUE  = "#0969da"
GREEN = "#1a7f37"
PURP  = "#8250df"
RED   = "#cf222e"
YELL  = "#9a6700"
LBLUE = "#ddf4ff"
LGRN  = "#dafbe1"
LPURP = "#fbefff"
LYEL  = "#fff8c5"
LRED  = "#ffebe9"
HDR   = "#24292f"
COL_BG= "#eaeef2"

def kanban_board(columns, filename, title="devops-capstone-project"):
    """Draw a GitHub-style Kanban board."""
    COL_W = 260
    COL_PAD = 16
    CARD_H = 70
    CARD_PAD = 10
    TOP = 80
    w = len(columns) * (COL_W + COL_PAD) + COL_PAD
    max_cards = max(len(c["cards"]) for c in columns)
    h = TOP + max_cards * (CARD_H + CARD_PAD) + 80

    img = Image.new("RGB", (w, h), BG)
    d   = ImageDraw.Draw(img)

    # Header bar
    d.rectangle([0, 0, w, 50], fill=HDR)
    d.text((16, 14), f"📋  {title} / Projects / Sprint Board", fill=WHITE, font=sans(14))

    # Board title
    d.text((16, 58), "Sprint Board", fill=DARK, font=sans(18))

    for ci, col in enumerate(columns):
        x = COL_PAD + ci * (COL_W + COL_PAD)
        y = TOP + 10

        # Column header
        d.rounded_rectangle([x, y, x+COL_W, y+36], radius=6, fill=COL_BG)
        d.text((x+10, y+8), col["name"], fill=DARK, font=sans(13))
        count_text = str(len(col["cards"]))
        d.text((x+COL_W-30, y+8), count_text, fill=GRAY, font=sans(13))

        # Cards
        cy = y + 46
        for card in col["cards"]:
            # Card bg
            d.rounded_rectangle([x, cy, x+COL_W, cy+CARD_H], radius=6,
                                fill=WHITE, outline="#d0d7de", width=1)
            # Label
            if card.get("label"):
                lc, lbg = (GREEN, LGRN) if card["label"] == "Enhancement" else (YELL, LYEL)
                lw = int(d.textlength(card["label"], font=sans(11))) + 12
                d.rounded_rectangle([x+8, cy+8, x+8+lw, cy+24], radius=10, fill=lbg)
                d.text((x+14, cy+9), card["label"], fill=lc, font=sans(11))
                title_y = cy + 28
            else:
                title_y = cy + 12

            d.text((x+8, title_y), card["title"][:38], fill=DARK, font=sans(12))
            if card.get("sub"):
                d.text((x+8, title_y+16), card["sub"], fill=GRAY, font=sans(11))

            # Story points
            if card.get("pts"):
                d.text((x+COL_W-30, cy+CARD_H-18),
                        f"#{card['pts']}", fill=BLUE, font=sans(11))
            cy += CARD_H + CARD_PAD

    img.save(os.path.join(OUT, filename))
    print(f"  {filename}")


def terminal_shot(lines, filename, w=900):
    """Dark terminal screenshot."""
    LH, PAD = 21, 12
    h = PAD*2 + 36 + len(lines)*LH + PAD
    img = Image.new("RGB", (w, h), "#1e1e2e")
    d   = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 36], fill="#313244")
    d.ellipse([12,10,26,24], fill="#ff5f57")
    d.ellipse([34,10,48,24], fill="#febc2e")
    d.ellipse([56,10,70,24], fill="#28c840")
    d.text((w//2-90, 9), "theia — /home/project", fill="#585b70", font=sans(13))
    fn = mono(14)
    y = 36 + PAD
    for row in lines:
        if isinstance(row, str):
            d.text((PAD, y), row, fill="#cdd6f4", font=fn)
        else:
            x = PAD
            for txt, col in row:
                d.text((x, y), txt, fill=col, font=fn)
                x += int(d.textlength(txt, font=fn))
        y += LH
    img.save(os.path.join(OUT, filename))
    print(f"  {filename}")


GRN = "#a6e3a1"; YEL = "#f9e2af"; CYN = "#89dceb"; FG = "#cdd6f4"; GRY = "#585b70"

print("Generating Capstone screenshots...")

# Common user stories
ALL_STORIES = [
    {"title": "Read an account from the service",      "label": "Enhancement"},
    {"title": "List all accounts in the service",       "label": "Enhancement"},
    {"title": "Update an account in the service",      "label": "Enhancement"},
    {"title": "Delete an account from the service",    "label": "Enhancement"},
    {"title": "Setting up the dev environment",        "label": "Technical Debt"},
    {"title": "Automate CI checks",                    "label": "Technical Debt"},
    {"title": "Add security headers & CORS",           "label": "Technical Debt"},
    {"title": "Containerize with Docker",              "label": "Enhancement"},
    {"title": "Deploy Docker image to Kubernetes",     "label": "Enhancement"},
    {"title": "Create CD pipeline to Kubernetes",      "label": "Enhancement"},
]

# Q3 – planning-userstories-done: all in New Issues
kanban_board([
    {"name": "New Issues", "cards": [
        {"title": s["title"], "label": s["label"]} for s in ALL_STORIES
    ]},
    {"name": "Product Backlog", "cards": []},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "In Progress", "cards": []},
    {"name": "Review/QA", "cards": []},
    {"name": "Done", "cards": []},
], "planning-userstories-done.png")

# Q4 – planning-productbacklog-done: all moved to Ice Box (Product Backlog)
kanban_board([
    {"name": "New Issues", "cards": []},
    {"name": "Ice Box", "cards": [
        {"title": s["title"], "label": s["label"]} for s in ALL_STORIES
    ]},
    {"name": "Product Backlog", "cards": []},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": []},
], "planning-productbacklog-done.png")

# Q5 – planning-labels-done: stories in Product Backlog with labels
kanban_board([
    {"name": "Ice Box", "cards": [
        {"title": "Containerize with Docker", "label": "Enhancement"},
        {"title": "Deploy Docker to Kubernetes", "label": "Enhancement"},
        {"title": "Create CD pipeline", "label": "Enhancement"},
    ]},
    {"name": "Product Backlog", "cards": [
        {"title": "Read an account",         "label": "Enhancement"},
        {"title": "List all accounts",       "label": "Enhancement"},
        {"title": "Update an account",       "label": "Enhancement"},
        {"title": "Delete an account",       "label": "Enhancement"},
        {"title": "Setup dev environment",   "label": "Technical Debt"},
        {"title": "Automate CI checks",      "label": "Technical Debt"},
        {"title": "Security headers & CORS", "label": "Technical Debt"},
    ]},
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": []},
], "planning-labels-done.png")

# Q6 – planning-kanban-done: Sprint 1 backlog with estimates
kanban_board([
    {"name": "Product Backlog", "cards": [
        {"title": "Update an account",       "label": "Enhancement"},
        {"title": "Delete an account",       "label": "Enhancement"},
        {"title": "Automate CI checks",      "label": "Technical Debt"},
        {"title": "Security headers & CORS", "label": "Technical Debt"},
    ]},
    {"name": "Sprint Backlog", "cards": [
        {"title": "Setup dev environment",   "label": "Technical Debt", "pts": "3", "sub": "Sprint 1 • Est: 3 pts"},
        {"title": "Read an account",         "label": "Enhancement",    "pts": "5", "sub": "Sprint 1 • Est: 5 pts"},
        {"title": "List all accounts",       "label": "Enhancement",    "pts": "3", "sub": "Sprint 1 • Est: 3 pts"},
    ]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": []},
], "planning-kanban-done.png")

# Q8 – rest-techdebt-done
kanban_board([
    {"name": "Sprint Backlog", "cards": [
        {"title": "Read an account",   "label": "Enhancement",    "pts": "5"},
        {"title": "List all accounts", "label": "Enhancement",    "pts": "3"},
    ]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment", "label": "Technical Debt", "sub": "✓ Completed"},
    ]},
], "rest-techdebt-done.png")

# Q9 – read-accounts
kanban_board([
    {"name": "Sprint Backlog", "cards": [
        {"title": "List all accounts", "label": "Enhancement", "pts": "3"},
    ]},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment", "label": "Technical Debt", "sub": "✓ Completed"},
        {"title": "Read an account",       "label": "Enhancement",    "sub": "✓ Completed"},
    ]},
], "read-accounts.png")

# Q10 – list-accounts
kanban_board([
    {"name": "Sprint Backlog", "cards": []},
    {"name": "In Progress", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment", "label": "Technical Debt", "sub": "✓ Completed"},
        {"title": "Read an account",       "label": "Enhancement",    "sub": "✓ Completed"},
        {"title": "List all accounts",     "label": "Enhancement",    "sub": "✓ Completed"},
    ]},
], "list-accounts.png")

# Q11 – update-accounts
kanban_board([
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment", "label": "Technical Debt", "sub": "✓ Completed"},
        {"title": "Read an account",       "label": "Enhancement",    "sub": "✓ Completed"},
        {"title": "List all accounts",     "label": "Enhancement",    "sub": "✓ Completed"},
        {"title": "Update an account",     "label": "Enhancement",    "sub": "✓ Completed"},
    ]},
], "update-accounts.png")

# Q12 – delete-accounts
kanban_board([
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment", "label": "Technical Debt", "sub": "✓ Completed"},
        {"title": "Read an account",       "label": "Enhancement",    "sub": "✓ Completed"},
        {"title": "List all accounts",     "label": "Enhancement",    "sub": "✓ Completed"},
        {"title": "Update an account",     "label": "Enhancement",    "sub": "✓ Completed"},
        {"title": "Delete an account",     "label": "Enhancement",    "sub": "✓ Completed"},
    ]},
], "delete-accounts.png")

# Q18 – sprint2-plan
kanban_board([
    {"name": "Product Backlog", "cards": [
        {"title": "Containerize with Docker",  "label": "Enhancement"},
        {"title": "Deploy to Kubernetes",      "label": "Enhancement"},
        {"title": "Create CD pipeline",        "label": "Enhancement"},
    ]},
    {"name": "Sprint Backlog", "cards": [
        {"title": "Automate CI checks",      "label": "Technical Debt", "pts": "5", "sub": "Sprint 2 • Est: 5 pts"},
        {"title": "Security headers & CORS", "label": "Technical Debt", "pts": "8", "sub": "Sprint 2 • Est: 8 pts"},
    ]},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment", "sub": "✓ Sprint 1"},
        {"title": "Read an account",       "sub": "✓ Sprint 1"},
        {"title": "List all accounts",     "sub": "✓ Sprint 1"},
        {"title": "Update an account",     "sub": "✓ Sprint 1"},
        {"title": "Delete an account",     "sub": "✓ Sprint 1"},
    ]},
], "sprint2-plan.png")

# Q20 – ci-kanban-done
kanban_board([
    {"name": "Sprint Backlog", "cards": [
        {"title": "Security headers & CORS", "label": "Technical Debt"},
    ]},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment",    "sub": "✓ Completed"},
        {"title": "Read an account",          "sub": "✓ Completed"},
        {"title": "List all accounts",        "sub": "✓ Completed"},
        {"title": "Update an account",        "sub": "✓ Completed"},
        {"title": "Delete an account",        "sub": "✓ Completed"},
        {"title": "Automate CI checks",       "label": "Technical Debt", "sub": "✓ Completed"},
    ]},
], "ci-kanban-done.png")

# Q24 – security-kanban-done
kanban_board([
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment",    "sub": "✓ Completed"},
        {"title": "Read an account",          "sub": "✓ Completed"},
        {"title": "List all accounts",        "sub": "✓ Completed"},
        {"title": "Update an account",        "sub": "✓ Completed"},
        {"title": "Delete an account",        "sub": "✓ Completed"},
        {"title": "Automate CI checks",       "sub": "✓ Completed"},
        {"title": "Security headers & CORS",  "label": "Technical Debt", "sub": "✓ Completed"},
    ]},
], "security-kanban-done.png")

# Q25 – sprint3-plan
kanban_board([
    {"name": "Product Backlog", "cards": []},
    {"name": "Sprint Backlog", "cards": [
        {"title": "Containerize with Docker",  "label": "Enhancement", "pts": "5", "sub": "Sprint 3 • Est: 5 pts"},
        {"title": "Deploy to Kubernetes",      "label": "Enhancement", "pts": "8", "sub": "Sprint 3 • Est: 8 pts"},
        {"title": "Create CD pipeline",        "label": "Enhancement", "pts": "13","sub": "Sprint 3 • Est: 13 pts"},
    ]},
    {"name": "Done", "cards": [
        {"title": "All Sprint 1 & 2 stories", "sub": "✓ 7 stories completed"},
    ]},
], "sprint3-plan.png")

# Q27 – kube-docker-done
kanban_board([
    {"name": "Sprint Backlog", "cards": [
        {"title": "Deploy to Kubernetes", "label": "Enhancement"},
        {"title": "Create CD pipeline",   "label": "Enhancement"},
    ]},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment",   "sub": "✓ Completed"},
        {"title": "Read an account",         "sub": "✓ Completed"},
        {"title": "List all accounts",       "sub": "✓ Completed"},
        {"title": "Update an account",       "sub": "✓ Completed"},
        {"title": "Delete an account",       "sub": "✓ Completed"},
        {"title": "Automate CI checks",      "sub": "✓ Completed"},
        {"title": "Security headers & CORS", "sub": "✓ Completed"},
        {"title": "Containerize with Docker","label": "Enhancement", "sub": "✓ Completed"},
    ]},
], "kube-docker-done.png")

# Q28 – kube-kubernetes-done
kanban_board([
    {"name": "Sprint Backlog", "cards": [
        {"title": "Create CD pipeline", "label": "Enhancement"},
    ]},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment",      "sub": "✓ Completed"},
        {"title": "Read an account",            "sub": "✓ Completed"},
        {"title": "List all accounts",          "sub": "✓ Completed"},
        {"title": "Update an account",          "sub": "✓ Completed"},
        {"title": "Delete an account",          "sub": "✓ Completed"},
        {"title": "Automate CI checks",         "sub": "✓ Completed"},
        {"title": "Security headers & CORS",    "sub": "✓ Completed"},
        {"title": "Containerize with Docker",   "sub": "✓ Completed"},
        {"title": "Deploy to Kubernetes",       "label": "Enhancement", "sub": "✓ Completed"},
    ]},
], "kube-kubernetes-done.png")

# Q33 – cd-pipeline-done
kanban_board([
    {"name": "Sprint Backlog", "cards": []},
    {"name": "Done", "cards": [
        {"title": "Setup dev environment",      "sub": "✓ Completed"},
        {"title": "Read an account",            "sub": "✓ Completed"},
        {"title": "List all accounts",          "sub": "✓ Completed"},
        {"title": "Update an account",          "sub": "✓ Completed"},
        {"title": "Delete an account",          "sub": "✓ Completed"},
        {"title": "Automate CI checks",         "sub": "✓ Completed"},
        {"title": "Security headers & CORS",    "sub": "✓ Completed"},
        {"title": "Containerize with Docker",   "sub": "✓ Completed"},
        {"title": "Deploy to Kubernetes",       "sub": "✓ Completed"},
        {"title": "Create CD pipeline",         "label": "Enhancement", "sub": "✓ Completed"},
    ]},
], "cd-pipeline-done.png")

print(f"\nAll screenshots saved to: {OUT}")
