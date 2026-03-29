import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime, timedelta
from utils.audio_utils import generate_audio


# ─────────────────────────────────────────────
#  SPACED REPETITION HELPERS
# ─────────────────────────────────────────────

# How many minutes until a card is eligible to be shown again
REVIEW_INTERVALS = {
    "new":      0,    # always show
    "review":   1,    # re-show after 1 min  (very soon)
    "mastered": 60,   # re-show after 60 min (much later)
}

def _now_str() -> str:
    return datetime.utcnow().isoformat()


def _is_due(card: dict) -> bool:
    """Return True when the card should surface in the current session."""
    last_seen = card.get("last_seen")
    status    = card.get("status", "new")

    if last_seen is None:
        return True                                      # never seen → always due

    interval_minutes = REVIEW_INTERVALS.get(status, 0)
    due_at = datetime.fromisoformat(last_seen) + timedelta(minutes=interval_minutes)
    return datetime.utcnow() >= due_at


def _mark_seen(card: dict) -> None:
    """Stamp the card with the current time."""
    card["last_seen"] = _now_str()


def _sr_sort_key(card: dict):
    """
    Sorting priority (lower = shown first):
      0 – review cards that are due         ← highest priority
      1 – new cards                          ← second
      2 – mastered cards that are due        ← third
      3 – anything else (not yet due)        ← last
    """
    status = card.get("status", "new")
    due    = _is_due(card)

    if status == "review"   and due:  return 0
    if status == "new":               return 1
    if status == "mastered" and due:  return 2
    return 3


def apply_spaced_repetition(cards: list) -> list:
    """
    Return a re-ordered copy of *cards* according to the SR priority.
    'review' cards bubble to the top; 'mastered' cards sink to the bottom.
    """
    return sorted(cards, key=_sr_sort_key)


# ─────────────────────────────────────────────
#  AUDIO
# ─────────────────────────────────────────────

def play_audio(text, key):
    temp_file = f"temp_card_{key}.mp3"
    try:
        audio_path = generate_audio(text, temp_file)
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except Exception as e:
        st.error(f"Audio Error: {e}")


# ─────────────────────────────────────────────
#  FLASHCARD HTML
# ─────────────────────────────────────────────

def get_flashcard_html(front, back, status, key):
    colors = {
        "new":      "linear-gradient(135deg, #2196F3 0%, #1976D2 100%)",
        "mastered": "linear-gradient(135deg, #4CAF50 0%, #388E3C 100%)",
        "review":   "linear-gradient(135deg, #f44336 0%, #d32f2f 100%)",
    }
    bg_color = colors.get(status, colors["new"])

    # Small badge shown on the front face
    badge_labels = {"new": "🆕 New", "mastered": "✅ Mastered", "review": "🔁 Review"}
    badge = badge_labels.get(status, "")

    html = f"""
    <style>
    .flashcard-{key} {{
        background-color: transparent;
        width: 100%;
        height: 200px;
        perspective: 1000px;
        cursor: pointer;
        margin-bottom: 10px;
    }}
    .flashcard-inner-{key} {{
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }}
    .flashcard-{key}:hover .flashcard-inner-{key} {{
        transform: rotateY(180deg);
    }}
    .flashcard-front-{key}, .flashcard-back-{key} {{
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 12px;
        padding: 20px;
        backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        color: white;
    }}
    .flashcard-front-{key} {{
        background: {bg_color};
    }}
    .flashcard-back-{key} {{
        background: linear-gradient(135deg, #7b1fa2 0%, #4a148c 100%);
        transform: rotateY(180deg);
    }}
    .badge-{key} {{
        font-size: 11px;
        font-weight: 700;
        opacity: 0.85;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }}
    </style>
    <div class="flashcard-{key}">
        <div class="flashcard-inner-{key}">
            <div class="flashcard-front-{key}">
                <span class="badge-{key}">{badge}</span>
                {front}
            </div>
            <div class="flashcard-back-{key}">
                {back}
            </div>
        </div>
    </div>
    """
    return html


# ─────────────────────────────────────────────
#  MAIN DISPLAY FUNCTION
# ─────────────────────────────────────────────

def display_flashcards(cards):
    if not cards:
        st.info("No flashcards generated.")
        return

    # ── Initialise card fields ──────────────────
    for card in cards:
        card.setdefault("status",    "new")
        card.setdefault("last_seen", None)
        card.setdefault("review_count", 0)

    # ── Header + filter ────────────────────────
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        st.subheader("Knowledge Flashcards")
    with filter_col2:
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "New", "Mastered", "Need Review"],
            index=0,
        )

    # ── Spaced-repetition info banner ──────────
    review_due = [c for c in cards if c.get("status") == "review" and _is_due(c)]
    if review_due:
        st.warning(
            f"🔁 **{len(review_due)} card(s) need review** — they appear at the top of the list.",
            icon="⚠️",
        )

    # ── Filter ─────────────────────────────────
    status_map = {
        "New":         "new",
        "Mastered":    "mastered",
        "Need Review": "review",
    }

    for i, card in enumerate(cards):
        card["original_index"] = i

    if filter_status == "All":
        filtered_cards = list(cards)
    else:
        target = status_map[filter_status]
        filtered_cards = [c for c in cards if c["status"] == target]

    if not filtered_cards:
        st.info(f"No cards with status '{filter_status}' found.")
        return

    # ── Apply spaced-repetition ordering ───────
    filtered_cards = apply_spaced_repetition(filtered_cards)

    # ── Render grid ────────────────────────────
    cols = st.columns(3)
    for idx, card in enumerate(filtered_cards):
        col_idx = idx % 3
        orig_i  = card["original_index"]

        with cols[col_idx]:
            # Mark the card as seen (for interval tracking)
            _mark_seen(card)

            card_html = get_flashcard_html(
                card.get("front", "Concept"),
                card.get("back",  "Definition"),
                card["status"],
                orig_i,
            )
            components.html(card_html, height=220)

            # ── Status buttons ──────────────────
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("✅ Mastered", key=f"master_{orig_i}"):
                    card["status"]       = "mastered"
                    card["review_count"] = 0          # reset on mastery
                    _mark_seen(card)
                    st.rerun()
            with btn_col2:
                if st.button("🔁 Review", key=f"review_{orig_i}"):
                    card["status"]        = "review"
                    card["review_count"]  = card.get("review_count", 0) + 1
                    _mark_seen(card)
                    st.rerun()

            # Small review-count indicator
            rc = card.get("review_count", 0)
            if rc:
                st.caption(f"Reviewed {rc}×")

            # ── Audio ───────────────────────────
            if st.button("🔊 Play Audio", key=f"audio_{orig_i}"):
                play_audio(
                    f"{card.get('front', '')}. {card.get('back', '')}",
                    orig_i,
                )

    # ── Progress stats ─────────────────────────
    st.divider()
    total    = len(cards)
    mastered = sum(1 for c in cards if c["status"] == "mastered")
    review   = sum(1 for c in cards if c["status"] == "review")
    new      = sum(1 for c in cards if c["status"] == "new")

    st.write("### Your Progress")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    p_col1.metric("Total Cards", total)
    p_col2.metric("New",         new)
    p_col3.metric("Mastered ✅", mastered)
    p_col4.metric("Need Review 🔁", review)

    if total > 0:
        progress = mastered / total
        st.progress(progress, text=f"Mastery: {int(progress * 100)}%")