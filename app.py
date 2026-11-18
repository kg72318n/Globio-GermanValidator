"""A1 German exam readiness check (Streamlit version).

Scoring is plain Python (no LLM, RAG or agents): the answer key is fixed, so the
verdict is instant, free, repeatable and easy to explain and change.
"""
import altair as alt
import pandas as pd
import streamlit as st

# ---- Tunable settings (change these to change what "ready" means) ----
CONFIG = {
    "PASS": 60,         # real exam pass mark (%): below this overall = "Not yet"
    "READY": 75,        # overall % needed for "Ready" (buffer: 14 questions is a noisy sample)
    "WEAK_SKILL": 60,   # any skill below this blocks "Ready"
    "WEIGHTS": {1: 1.0, 2: 1.5},  # difficulty 1 = easy, 2 = medium/hard
    "MAX_TIPS": 3,
}

SKILLS = {"vocab": "Vocabulary", "grammar": "Grammar", "reading": "Reading"}

LABELS = {
    "greetings": "Everyday phrases", "places": "Place words", "numbers": "Numbers",
    "time": "Telling the time", "family": "Family words", "verbs": "Verb endings",
    "articles": "Articles (ein / einen / eine)", "modals": "Modal verbs",
    "wordorder": "Word order", "messages": "Reading messages", "notices": "Reading signs and notices",
}

TIPS = {
    "greetings": "Learn the 30 most common everyday phrases (Danke, Bitte, Entschuldigung, Tschüss) with flashcards.",
    "places": "Learn 25 place nouns together with their article, e.g. der Bahnhof, die Bäckerei, das Café.",
    "numbers": "Say numbers 1–100 out loud, and drill the tricky pairs like siebzehn (17) vs siebzig (70).",
    "time": "Practise telling the time: halb drei is 2:30, Viertel nach and Viertel vor. Do 10 clock faces a day.",
    "family": "Build a small family tree in German (Mutter, Vater, Tante, Onkel, Cousine) and describe it aloud.",
    "verbs": "Drill present-tense endings (ich komme, du kommst, er kommt) and sein/haben until they are automatic.",
    "articles": "Practise ein/einen/eine after “haben” and “brauchen”: the masculine form changes (Ich habe einen Bruder).",
    "modals": "Practise können, müssen, wollen: write 10 sentences where the second verb goes to the end.",
    "wordorder": "Practise verb-in-second-position: start sentences with a time word (Heute gehe ich…) and write 10.",
    "messages": "Read 5 short A1 messages or emails and underline who, where and when before answering questions.",
    "notices": "Practise reading signs, opening hours and timetables: days, times, von/bis, geschlossen.",
}

TOM = ("Hallo Anna,\nich bin Tom. Ich wohne in Berlin und arbeite in einem Café. Am Samstag habe ich frei. "
       "Dann spiele ich Fußball mit meinem Bruder. Am Sonntag besuche ich meine Eltern in Hamburg.\nTschüss, Tom")
BAKERY = "Bäckerei Müller\nÖffnungszeiten:\nMo–Fr: 7:00–18:00 Uhr\nSa: 7:00–13:00 Uhr\nSonntag: geschlossen"

QUESTIONS = [
    # Vocabulary
    {"s": "vocab", "t": "greetings", "d": 1, "q": "How do you say “thank you” in German?", "o": ["Bitte", "Tschüss", "Danke", "Entschuldigung"], "a": 2},
    {"s": "vocab", "t": "places", "d": 1, "q": "What does “der Bahnhof” mean?", "o": ["airport", "train station", "bus", "bakery"], "a": 1},
    {"s": "vocab", "t": "numbers", "d": 2, "q": "Which number is “siebzehn”?", "o": ["7", "27", "70", "17"], "a": 3},
    {"s": "vocab", "t": "time", "d": 2, "q": "It is “halb drei”. What time is it?", "o": ["2:30", "3:30", "2:15", "3:00"], "a": 0},
    {"s": "vocab", "t": "family", "d": 2, "q": "“Die Schwester meiner Mutter” is my …", "o": ["Oma", "Cousine", "Tante", "Nichte"], "a": 2},
    # Grammar
    {"s": "grammar", "t": "verbs", "d": 1, "q": "Ich ___ aus Indien.", "o": ["kommst", "komme", "kommt", "kommen"], "a": 1},
    {"s": "grammar", "t": "verbs", "d": 1, "q": "Wir ___ Studenten.", "o": ["bin", "ist", "seid", "sind"], "a": 3},
    {"s": "grammar", "t": "articles", "d": 2, "q": "Ich habe ___ Bruder.", "o": ["einen", "ein", "eine", "einem"], "a": 0},
    {"s": "grammar", "t": "modals", "d": 2, "q": "Ich ___ gut Deutsch sprechen.", "o": ["können", "kannst", "kann", "könnt"], "a": 2},
    {"s": "grammar", "t": "wordorder", "d": 2, "q": "Which sentence is correct?",
     "o": ["Heute ich gehe ins Kino.", "Heute gehe ich ins Kino.", "Ich heute gehe ins Kino.", "Gehe heute ich ins Kino."], "a": 1},
    # Reading
    {"s": "reading", "t": "messages", "d": 1, "p": TOM, "q": "Where does Tom work?", "o": ["In an office", "In a café", "In a school", "In a hotel"], "a": 1},
    {"s": "reading", "t": "messages", "d": 2, "p": TOM, "q": "What does Tom do on Saturday?", "o": ["He works", "He plays football", "He visits his parents", "He sleeps"], "a": 1},
    {"s": "reading", "t": "notices", "d": 2, "p": BAKERY, "q": "Until when is the bakery open on Saturday?", "o": ["Until 18:00", "Until 7:00", "Until 13:00", "It is closed"], "a": 2},
    {"s": "reading", "t": "notices", "d": 1, "p": BAKERY, "q": "You want bread on Sunday. What is true?",
     "o": ["Open until 13:00", "The bakery is closed", "It opens at 7:00", "It opens at 18:00"], "a": 1},
]
N = len(QUESTIONS)


# ---- Scoring (pure functions, easy to test and change) ----
def skill_scores(answers):
    out = {k: {"got": 0.0, "max": 0.0} for k in SKILLS}
    for q, ans in zip(QUESTIONS, answers):
        w = CONFIG["WEIGHTS"][q["d"]]
        out[q["s"]]["max"] += w
        if ans == q["a"]:
            out[q["s"]]["got"] += w
    for v in out.values():
        v["pct"] = round(100 * v["got"] / v["max"])
    return out


def verdict(scores):
    pcts = [v["pct"] for v in scores.values()]
    overall = round(sum(pcts) / len(pcts))  # each skill counts equally
    weakest = min(pcts)
    if overall < CONFIG["PASS"]:
        level = "notyet"
    elif overall >= CONFIG["READY"] and weakest >= CONFIG["WEAK_SKILL"]:
        level = "ready"
    else:
        level = "almost"
    return {"overall": overall, "weakest": weakest, "level": level}


def top_priorities(answers):
    loss = {}
    for q, ans in zip(QUESTIONS, answers):
        if ans != q["a"]:
            loss[q["t"]] = loss.get(q["t"], 0) + CONFIG["WEIGHTS"][q["d"]]
    ranked = sorted(loss.items(), key=lambda kv: kv[1], reverse=True)
    return [t for t, _ in ranked[: CONFIG["MAX_TIPS"]]]


# ---- UI helpers ----
def color(p):
    if p >= CONFIG["READY"]:
        return "#16825d"
    if p >= CONFIG["WEAK_SKILL"]:
        return "#b9770e"
    return "#c53030"


def donut(pct):
    df = pd.DataFrame({"part": ["score", "rest"], "value": [pct, 100 - pct], "order": [0, 1]})
    return (
        alt.Chart(df)
        .mark_arc(innerRadius=42, outerRadius=70)
        .encode(
            theta=alt.Theta("value:Q", stack=True),
            order=alt.Order("order:Q"),
            color=alt.Color("part:N", legend=None,
                            scale=alt.Scale(domain=["score", "rest"], range=[color(pct), "#d5dbe6"])),
            tooltip=[],
        )
        .properties(height=150)
    )


def reset():
    st.session_state.clear()
    st.session_state.stage = "start"
    st.session_state.i = 0
    st.session_state.answers = []


# ---- Screens ----
def start_screen():
    st.title("Are you ready for your A1 German exam?")
    st.write(
        "Answer a short check on vocabulary, grammar and reading. You will see your readiness for each "
        "skill and what to practise before you book Goethe Start Deutsch 1 or ÖSD A1."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Questions", N)
    c2.metric("Time", "~5 min")
    c3.metric("Skills scored", 3)
    st.caption("No sign-up. Nothing is stored.")
    if st.button("Start the check", type="primary"):
        st.session_state.stage = "quiz"
        st.rerun()


def quiz_screen():
    i = st.session_state.i
    q = QUESTIONS[i]
    st.progress(i / N)
    st.caption(f"Question {i + 1} of {N} · {SKILLS[q['s']]}")
    if "p" in q:
        with st.container(border=True):
            for line in q["p"].split("\n"):
                st.markdown(line)
    choice = st.radio(q["q"], q["o"], index=None, key=f"choice_{i}")
    label = "See my result" if i == N - 1 else "Next"
    if st.button(label, type="primary", disabled=choice is None):
        st.session_state.answers.append(q["o"].index(choice))
        st.session_state.i += 1
        if st.session_state.i >= N:
            st.session_state.stage = "result"
        st.rerun()


def result_screen():
    answers = st.session_state.answers
    sc = skill_scores(answers)
    v = verdict(sc)
    tops = top_priorities(answers)

    if v["level"] == "ready":
        st.success(f"### Ready · overall {v['overall']}%\nYou are scoring comfortably above the pass mark in every skill. "
                   "Book the exam, and do one full mock test first.")
    elif v["level"] == "almost":
        why = "one skill is still weak" if v["overall"] >= CONFIG["PASS"] else "your score is near the pass mark"
        st.warning(f"### Almost ready · overall {v['overall']}%\nYou are close, but {why}. Fix the points below, then book.")
    else:
        st.error(f"### Not yet · overall {v['overall']}%\nYour score is below the exam pass mark of {CONFIG['PASS']}%. "
                 "A few more weeks of practice will protect your exam fee.")

    st.subheader("By skill")
    cols = st.columns(3)
    for col, k in zip(cols, SKILLS):
        with col:
            st.altair_chart(donut(sc[k]["pct"]))
            st.metric(SKILLS[k], f"{sc[k]['pct']}%")

    ranked = sorted(SKILLS, key=lambda k: sc[k]["pct"], reverse=True)
    best, worst = ranked[0], ranked[-1]
    gap = sc[best]["pct"] - sc[worst]["pct"]
    if gap == 0:
        st.info("Your three skills are level, so practise all of them evenly.")
    else:
        st.info(f"**Strongest:** {SKILLS[best]} ({sc[best]['pct']}%). "
                f"**Weakest:** {SKILLS[worst]} ({sc[worst]['pct']}%), {gap} points lower. Start your practice there.")
    st.caption(f"Green is at or above {CONFIG['READY']}%, amber is {CONFIG['WEAK_SKILL']}–{CONFIG['READY'] - 1}%, "
               f"red is below {CONFIG['WEAK_SKILL']}%.")

    st.subheader("Practise these before you book" if tops else "Nothing to fix here")
    if tops:
        for t in tops:
            with st.container(border=True):
                st.markdown(f"**{LABELS[t]}**")
                st.write(TIPS[t])
    else:
        st.write("You answered everything correctly. Take a full mock exam to test listening, speaking and writing.")

    missed = [(q, a) for q, a in zip(QUESTIONS, answers) if a != q["a"]]
    if missed:
        with st.expander(f"Review {len(missed)} missed question{'s' if len(missed) > 1 else ''}"):
            for q, a in missed:
                st.markdown(f"**{q['q']}**  \nYour answer: {q['o'][a]}  \nCorrect: {q['o'][q['a']]}")

    st.caption("This check covers reading, vocabulary and grammar only. The real exam also tests listening, speaking "
               "and writing, so treat this as a guide, not a guarantee. Also try one full official mock test before you book.")
    if st.button("Retake the check"):
        reset()
        st.rerun()


# ---- App ----
st.set_page_config(page_title="A1 German exam readiness check", page_icon="🇩🇪", layout="centered")
if "stage" not in st.session_state:
    reset()
{"start": start_screen, "quiz": quiz_screen, "result": result_screen}[st.session_state.stage]()
