
import streamlit as st
import streamlit.components.v1 as components

from html import escape

from app.services.story_engine import StoryEngine
from app.services.player_manager import PlayerManager
from app.services.combat_manager import CombatManager
from app.services.memory_manager import MemoryManager
from app.agents.orchestrator import GameOrchestrator
from app.schemas.player import PlayerState
from app.schemas.story import TurnResponse


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="WorldForge AI | Fantasy RPG",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# CUSTOM GAME THEME
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --gold: #e8c27e;
    --gold-light: #ffe3a6;
    --purple: #7b5aa6;
    --panel: #171624;
    --panel-light: #242035;
    --muted: #aaa0b7;
}

.stApp {
    background:
        radial-gradient(ellipse at 50% -10%, #48305d 0%, transparent 40%),
        linear-gradient(145deg, #10101b, #171323 55%, #090c16);
    color: #eee8f0;
    font-family: 'Rajdhani', sans-serif;
}

header, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--gold) !important;
}

p, label, span {
    font-family: 'Rajdhani', sans-serif;
}

hr {
    border-color: #554267;
}

.game-logo {
    text-align: center;
    font-family: 'Cinzel', serif;
    font-weight: 900;
    font-size: 34px;
    letter-spacing: 6px;
    color: var(--gold-light);
    text-shadow: 0 0 22px #c18b55;
}

.game-subtitle {
    text-align: center;
    color: #aa9bbd;
    letter-spacing: 5px;
    font-size: 11px;
    margin-bottom: 22px;
}

.game-panel {
    background: linear-gradient(145deg, #252036, #14131f);
    border: 1px solid #59466c;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 10px 35px #0006;
}

.panel-heading {
    color: var(--gold);
    font-family: 'Cinzel', serif;
    font-size: 14px;
    letter-spacing: 2px;
    border-bottom: 1px solid #5b496b;
    padding-bottom: 12px;
    margin-bottom: 15px;
}

.hero-name {
    color: #f6dcaa;
    font-family: 'Cinzel', serif;
    font-size: 21px;
    font-weight: 700;
}

.hero-level {
    color: #b7a5d1;
    font-size: 13px;
    letter-spacing: 2px;
}

.stat-number {
    color: var(--gold-light);
    font-family: 'Cinzel', serif;
    font-size: 23px;
    font-weight: 700;
}

.stat-label {
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.scene-panel {
    background:
        linear-gradient(135deg, #292139, #191725);
    border: 1px solid #876747;
    border-radius: 16px;
    padding: 25px;
    box-shadow: inset 0 0 40px #ad8a4210, 0 10px 35px #0005;
}

.scene-heading {
    font-family: 'Cinzel', serif;
    font-size: 13px;
    letter-spacing: 4px;
    color: var(--gold);
    margin-bottom: 14px;
}

.scene-text {
    color: #e8dfeb;
    font-size: 18px;
    line-height: 1.8;
}

.choice-label {
    font-family: 'Cinzel', serif;
    color: var(--gold);
    letter-spacing: 2px;
    font-size: 14px;
    margin-top: 20px;
    margin-bottom: 12px;
}

div.stButton > button {
    width: 100%;
    min-height: 48px;
    background: linear-gradient(110deg, #49365d, #29213d);
    border: 1px solid #a07b53;
    border-radius: 9px;
    color: #f8e8cd;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 16px;
    transition: all .25s ease;
}

div.stButton > button:hover {
    background: linear-gradient(110deg, #79543d, #59416d);
    border-color: #ffe0a0;
    color: white;
    box-shadow: 0 0 20px #b28a5c55;
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background: #211c30;
    border: 1px solid #59466c;
    border-radius: 10px;
    padding: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #b7a5c6;
}

div[data-testid="stMetricValue"] {
    color: var(--gold-light);
    font-family: 'Cinzel', serif;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #a33350, #e6bd75);
}

div[data-testid="stExpander"] {
    border: 1px solid #59466c;
    border-radius: 10px;
    background: #191725;
}

input {
    background: #211c30 !important;
}

.battle-title {
    text-align: center;
    font-family: 'Cinzel', serif;
    font-size: 28px;
    color: #ffb1a8;
    letter-spacing: 4px;
}

.small-caption {
    color: #a99bb9;
    font-size: 12px;
    letter-spacing: 2px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# BACKEND SERVICES
# =====================================================

@st.cache_resource
def get_services():
    return (
        StoryEngine(),
        MemoryManager(),
        GameOrchestrator()
    )


engine, memory, orchestrator = get_services()


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "started": False,
    "player": None,
    "story": None,
    "world": "",
    "enemy": None,
    "in_combat": False,
    "events": [],
    "quest": "Discover the secrets of Aethelgard"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def add_event(message):
    st.session_state.events.insert(0, message)
    st.session_state.events = st.session_state.events[:8]


# =====================================================
# HERO ILLUSTRATION
# =====================================================

def render_hero():

    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * { box-sizing: border-box; }
    body {
        margin: 0;
        overflow: hidden;
        background: transparent;
    }

    .hero {
        width: 100%;
        height: 350px;
        position: relative;
        overflow: hidden;
        border-radius: 16px;
        border: 1px solid #765b79;
        background:
            radial-gradient(ellipse at 72% 38%, #8c5b8d 0%, transparent 27%),
            radial-gradient(ellipse at 30% 10%, #46365d 0%, transparent 45%),
            linear-gradient(120deg, #131423, #392742 58%, #192b43);
    }

    .hero:before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(0deg, #10101b 0%, transparent 70%),
            repeating-linear-gradient(
                115deg,
                transparent 0 100px,
                #ffffff08 101px 102px
            );
    }

    .castle {
        position: absolute;
        right: 4%;
        bottom: 0;
        width: 65%;
        height: 95%;
        opacity: .8;
    }

    .character {
        position: absolute;
        right: 25%;
        bottom: -8px;
        width: 230px;
        height: 310px;
        filter: drop-shadow(0 0 22px #c5a4ef55);
    }

    .hero-copy {
        position: absolute;
        z-index: 5;
        left: 5%;
        top: 23%;
        width: 45%;
    }

    .eyebrow {
        color: #e8c27e;
        letter-spacing: 5px;
        font: 12px Georgia, serif;
    }

    .hero-title {
        font: bold 36px Georgia, serif;
        color: #ffe3ac;
        margin: 15px 0;
        text-shadow: 0 0 20px #9a6c9b;
    }

    .hero-description {
        color: #d8cadd;
        font: 16px Arial;
        line-height: 1.7;
    }

    .orb {
        position: absolute;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #f5d68e;
        box-shadow: 0 0 15px #f5d68e;
        animation: float 3s infinite alternate;
    }

    @keyframes float {
        from { transform: translateY(0); opacity: .4; }
        to { transform: translateY(-25px); opacity: 1; }
    }

    </style>
    </head>

    <body>
    <div class="hero">

      <svg class="castle" viewBox="0 0 600 350"
           preserveAspectRatio="xMidYMax meet">

        <g fill="#151321" stroke="#b18b9c" stroke-width="2">

          <path d="M70 350V180H145V350Z"/>
          <path d="M90 180V90L110 55L130 90V180Z"/>

          <path d="M180 350V115H260V350Z"/>
          <path d="M190 115V35L220 5L250 35V115Z"/>

          <path d="M300 350V165H370V350Z"/>
          <path d="M310 165V75L335 40L360 75V165Z"/>

          <path d="M420 350V120H510V350Z"/>
          <path d="M430 120V35L465 0L500 35V120Z"/>

          <path d="M220 230H460V350H220Z"/>

        </g>

        <g fill="#e7b875" opacity=".8">
          <rect x="107" y="120" width="7" height="18"/>
          <rect x="218" y="70" width="8" height="22"/>
          <rect x="333" y="105" width="7" height="18"/>
          <rect x="461" y="70" width="8" height="22"/>
          <rect x="275" y="270" width="10" height="20"/>
          <rect x="390" y="270" width="10" height="20"/>
        </g>

        <path d="M0 350L120 270L220 320L340 255L460 320L600 250V350Z"
              fill="#111321"/>

      </svg>

      <svg class="character" viewBox="0 0 250 340"
           preserveAspectRatio="xMidYMax meet">

        <defs>
          <linearGradient id="cape" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#b19bc9"/>
            <stop offset="50%" stop-color="#554268"/>
            <stop offset="100%" stop-color="#181727"/>
          </linearGradient>
        </defs>

        <!-- cloak -->
        <path d="M80 125 Q25 170 10 335 H240 Q220 175 170 125
                 Q130 150 80 125"
              fill="url(#cape)" stroke="#c2a27b" stroke-width="2"/>

        <!-- shoulders -->
        <path d="M70 145 L45 235 L125 280 L205 235 L180 145
                 Q125 115 70 145"
              fill="#4e4965" stroke="#d4b985" stroke-width="3"/>

        <!-- body armor -->
        <path d="M80 150 L125 205 L170 150 L185 260
                 L125 285 L65 260Z"
              fill="#a18b9c" stroke="#e4c99c" stroke-width="2"/>

        <!-- neck -->
        <rect x="105" y="90" width="40" height="40" fill="#d9bba6"/>

        <!-- head -->
        <path d="M77 100 Q55 30 125 20 Q195 30 173 105
                 L155 135 L95 135Z"
              fill="#dfc0ad" stroke="#b99b8a" stroke-width="2"/>

        <!-- hair -->
        <path d="M70 90 Q48 15 125 10 Q205 15 180 105
                 L160 80 L140 95 L130 55 L105 110 L90 75Z"
              fill="#242033"/>

        <!-- eye shadow -->
        <path d="M85 91 L112 95 M140 95 L165 91"
              stroke="#39263d" stroke-width="6"/>

        <!-- sword -->
        <path d="M195 230 L230 55"
              stroke="#d6d9ec" stroke-width="5"/>
        <path d="M230 55 L242 28 L247 63Z"
              fill="#e5c98c"/>
        <path d="M183 237 L211 243"
              stroke="#d8b879" stroke-width="7"/>

      </svg>

      <div class="hero-copy">
        <div class="eyebrow">THE AGE OF LOST KINGDOMS</div>
        <div class="hero-title">YOUR LEGEND BEGINS</div>
        <div class="hero-description">
          Ancient magic awakens. Forgotten kingdoms call.
          Your choices will shape the fate of the world.
        </div>
      </div>

      <div class="orb" style="left:50%;top:30%"></div>
      <div class="orb" style="left:72%;top:20%;animation-delay:1s"></div>
      <div class="orb" style="left:88%;top:50%;animation-delay:2s"></div>

    </div>
    </body>
    </html>
    """, height=365, scrolling=False)


# =====================================================
# GAME FUNCTIONS
# =====================================================

def start_new_game(name):

    player = PlayerManager(name)
    story = engine.generate_world(name)

    player.update_location(story.world_name)

    st.session_state.player = player
    st.session_state.story = story
    st.session_state.world = story.world_name
    st.session_state.started = True
    st.session_state.events = []

    add_event("Adventure started")


def load_game(name):

    saved = memory.load_game(name)

    if not saved:
        return False

    player = PlayerManager(name)
    player.player = PlayerState.model_validate(saved["player"])

    game = saved["game_state"]

    story = TurnResponse(
        scene=game["scene"],
        atmosphere=game["atmosphere"],
        choices=game["choices"],
        story_summary=game["summary"]
    )

    st.session_state.player = player
    st.session_state.story = story
    st.session_state.world = game["world"]
    st.session_state.started = True

    add_event("Previous adventure restored")

    return True


def save_game():

    player = st.session_state.player
    story = st.session_state.story

    game_state = {
        "world": st.session_state.world,
        "scene": story.scene,
        "summary": story.story_summary,
        "atmosphere": story.atmosphere,
        "choices": story.choices
    }

    memory.save_game(player, game_state)
    add_event("Game progress saved")


def process_story_action(action):

    player = st.session_state.player

    result = orchestrator.process_action(
        action,
        player.player.model_dump()
    )

    if result["decision"] != "STORY":
        st.warning(
            f"AI classified this action as {result['decision']}."
        )
        return

    updated = engine.process_action(
        player.player.name,
        st.session_state.world,
        st.session_state.story.scene,
        st.session_state.story.story_summary,
        action
    )

    st.session_state.story = updated

    player.add_xp(10)

    add_event(f"Action completed: {action[:45]}")


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="game-logo">⚔ WORLDFORGE AI ⚔</div>
<div class="game-subtitle">
A WORLD FORGED BY YOUR CHOICES
</div>
""", unsafe_allow_html=True)


# =====================================================
# TITLE SCREEN
# =====================================================

if not st.session_state.started:

    render_hero()

    st.markdown("<br>", unsafe_allow_html=True)

    left, middle, right = st.columns([1, 1.5, 1])

    with middle:

        st.markdown(
            '<div class="game-panel">'
            '<div class="panel-heading">✦ CREATE YOUR LEGEND ✦</div>',
            unsafe_allow_html=True
        )

        name = st.text_input(
            "HERO NAME",
            placeholder="Enter your character name..."
        )

        if st.button("⚔ BEGIN NEW ADVENTURE",
                     use_container_width=True):

            if name.strip():

                with st.spinner("The world is being forged..."):
                    start_new_game(name.strip())

                st.rerun()

            else:
                st.warning("Enter your character name.")

        if st.button("📜 CONTINUE ADVENTURE",
                     use_container_width=True):

            if name.strip():

                if load_game(name.strip()):
                    st.rerun()

                else:
                    st.warning("No saved adventure found.")

            else:
                st.warning("Enter your character name.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# =====================================================
# ACTIVE GAME
# =====================================================

player = st.session_state.player
story = st.session_state.story
combat = CombatManager(player)

st.markdown(
    f"""
    <div style="text-align:center;padding:10px">
      <div class="small-caption">CURRENT REALM</div>
      <h2>✦ {escape(st.session_state.world)} ✦</h2>
      <div style="color:#b6a3c5">
        Welcome, {escape(player.player.name)}
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Player HUD
st.markdown('<div class="game-panel">', unsafe_allow_html=True)

st.markdown('<div class="panel-heading">⚔ CHARACTER HUD</div>',
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

c1.metric("❤️ HEALTH",
          f"{player.player.health}/{player.player.max_health}")

c2.metric("⭐ LEVEL", player.player.level)

c3.metric("🪙 GOLD", player.player.gold)

c4.metric("✨ EXPERIENCE", player.player.xp)

st.progress(
    max(0, min(1, player.player.health / player.player.max_health))
)

st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# MAIN GAME LAYOUT
# =====================================================

left, center, right = st.columns(
    [1, 2.3, 1],
    gap="medium"
)


# LEFT: CHARACTER AND INVENTORY
with left:

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)

    st.markdown('<div class="panel-heading">YOUR HERO</div>',
                unsafe_allow_html=True)

    st.markdown(
        f'<div class="hero-name">{escape(player.player.name)}</div>'
        f'<div class="hero-level">LEVEL {player.player.level} ADVENTURER</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("**Health**")
    st.progress(
        max(0, min(1, player.player.health / player.player.max_health))
    )

    st.caption(
        f"{player.player.health} / {player.player.max_health} HP"
    )

    st.markdown("**Experience**")
    st.caption(f"{player.player.xp} XP")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)

    st.markdown('<div class="panel-heading">🎒 INVENTORY</div>',
                unsafe_allow_html=True)

    for item in player.player.inventory:
        st.write("◆", item)

    st.markdown('</div>', unsafe_allow_html=True)


# CENTER: STORY
with center:

    st.markdown('<div class="scene-panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="scene-heading">✦ THE STORY UNFOLDS ✦</div>',
        unsafe_allow_html=True
    )

    st.markdown("### The next chapter")

    st.markdown(f"*{story.atmosphere}*")

    st.write(story.scene)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="choice-label">CHOOSE YOUR DESTINY</div>',
        unsafe_allow_html=True
    )

    for index, choice in enumerate(story.choices):

        if st.button(
            f"✧  {choice}",
            key=f"choice_{index}_{story.story_summary[:20]}",
            use_container_width=True
        ):

            with st.spinner("Your destiny is being written..."):
                process_story_action(choice)

            st.rerun()


# RIGHT: QUEST AND CONTROLS
with right:

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)

    st.markdown('<div class="panel-heading">📜 QUEST JOURNAL</div>',
                unsafe_allow_html=True)

    st.write("**MAIN QUEST**")

    st.write(st.session_state.quest)

    st.caption("Your choices will determine the outcome.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)

    st.markdown('<div class="panel-heading">GAME ACTIONS</div>',
                unsafe_allow_html=True)

    if st.button("⚔ ENTER BATTLE", use_container_width=True):

        st.session_state.enemy = combat.create_enemy()
        st.session_state.in_combat = True

        st.rerun()

    if st.button("🧪 USE HEALTH POTION", use_container_width=True):

        old_health = player.player.health
        combat.use_potion()

        if player.player.health > old_health:
            add_event("Used a health potion")

        st.rerun()

    if st.button("💾 SAVE ADVENTURE", use_container_width=True):

        save_game()
        st.success("Adventure saved!")

    if st.button("🏰 RETURN TO TITLE", use_container_width=True):

        st.session_state.started = False
        st.session_state.player = None
        st.session_state.story = None
        st.session_state.in_combat = False
        st.session_state.enemy = None

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="game-panel">', unsafe_allow_html=True)

    st.markdown('<div class="panel-heading">RECENT EVENTS</div>',
                unsafe_allow_html=True)

    if st.session_state.events:

        for event in st.session_state.events[:5]:
            st.caption("◆ " + event)

    else:
        st.caption("Your journey is just beginning.")

    st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# COMBAT ARENA
# =====================================================

if st.session_state.in_combat:

    enemy = st.session_state.enemy

    st.divider()

    st.markdown(
        '<div class="battle-title">⚔ BATTLE ARENA ⚔</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="small-caption" style="text-align:center">'
        'A DANGEROUS ENEMY APPROACHES'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    hero_col, enemy_col = st.columns(2)

    with hero_col:

        st.markdown('<div class="game-panel">', unsafe_allow_html=True)

        st.markdown("### 🧙 YOUR HERO")

        st.metric(
            "HEALTH",
            f"{player.player.health}/{player.player.max_health}"
        )

        st.progress(
            max(0, min(1,
                player.player.health / player.player.max_health))
        )

        st.markdown('</div>', unsafe_allow_html=True)

    with enemy_col:

        st.markdown('<div class="game-panel">', unsafe_allow_html=True)

        st.markdown("### 👹 SHADOW BEAST")

        st.metric(
            "ENEMY HEALTH",
            f"{enemy.health}/{enemy.max_health}"
        )

        st.progress(
            max(0, min(1, enemy.health / enemy.max_health))
        )

        st.markdown('</div>', unsafe_allow_html=True)

    if enemy.health > 0 and player.player.health > 0:

        if st.button("⚔ ATTACK SHADOW BEAST",
                     use_container_width=True):

            result = combat.player_attack(enemy)

            if result == "VICTORY":

                add_event("Defeated Shadow Beast")

                st.success("Victory! Enemy defeated.")

                st.session_state.in_combat = False

            else:

                combat.enemy_attack(enemy)

                if player.player.health <= 0:
                    st.session_state.in_combat = False

            st.rerun()

        if st.button("🏃 ESCAPE BATTLE",
                     use_container_width=True):

            st.session_state.in_combat = False
            st.rerun()

    elif enemy.health <= 0:

        st.success("Victory! Shadow Beast defeated.")

        st.session_state.in_combat = False

    else:

        st.error("Your hero has fallen.")
        st.session_state.in_combat = False
