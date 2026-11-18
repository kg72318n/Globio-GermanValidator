A1 German Exam Readiness Check

A short web check that tells a German A1 learner how ready they are for the Goethe Start Deutsch 1 or ÖSD A1 exam, before they pay for it.



Problem Statement ?

Many learners finish A1 and book the exam without knowing if they are ready. Some fail and lose the exam fee and months on their journey abroad. This app gives them a quick, honest signal before they book.

What Webapp Does?
The learner answers 14 multiple-choice questions: 5 vocabulary, 5 grammar and 4 reading.
The app shows a verdict (Ready, Almost ready or Not yet) with an overall score.
It shows a score for each skill, compares the strongest and weakest, and lists the top 3 things to practise before booking.

The learner can review the questions that are wrong.

Why these rules:

60% is the pass mark for Goethe Start Deutsch 1. Check the current rules on the Goethe and ÖSD websites.
The 15-point buffer exists because a 14-question check is a noisy sample.
One weak skill can still fail the exam, so it blocks “Ready”.

All thresholds and weights live in one CONFIG object, so they are easy to change.

How “ready” is calculated
Skill score = difficulty-weighted % correct (easy = 1, medium = 1.5).
Overall score = average of the three skill scores.
Not yet: overall below 60% (the exam pass mark).
Ready: overall 75% or above, and no skill below 60%.
Almost ready: everything in between, including a high overall score with one weak skill.

Why these rules:
All thresholds and weights live in one CONFIG object, so they are easy to change.

Why no LLM, RAG or agents

The answer key is fixed, so plain code scores it. This keeps results instant, free, repeatable and easy to explain. A learner who retakes the check with the same answers always gets the same verdict.

AI would help in later versions, for generating questions (with human review), scoring writing and speaking, linking practice tips to real lessons, and follow-up reminders.

Limits
The check covers vocabulary, grammar and reading only. The real exam also tests listening, speaking and writing, so the result is a guide, not a guarantee.
The readiness thresholds are a hypothesis. They have not yet been validated against real exam results.
How I would validate it (V2)
Compare verdicts with real exam outcomes and check that “Ready” learners pass more often.
Retest the same learners with different questions to check the score is stable.
Interview learners about how they decide when to book and which tips they would follow.
Add listening, speaking and writing checks, adaptive questions and a bigger question bank.


Files
File	Purpose
app.py	Streamlit version of the app
requirements.txt	Python dependency (streamlit)
index.html	Standalone version, no server needed
Run locally
pip install -r requirements.txt
streamlit run app.py
