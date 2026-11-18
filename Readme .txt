A1 German Exam Readiness Check

A short web check that tells a German A1 learner how ready they are for the Goethe Start Deutsch 1 or ÖSD A1 exam, before they pay for it.



Problem Statement ?

Many learners finish A1 and book the exam without knowing if they are ready. Some fail and lose the exam fee and months on their journey abroad. This app gives them a quick, honest signal before they book.


User persona: Priya, the hopeful mover
Priya, 27
Nurse planning to work in Germany.
Just finished an A1 course. Studies
after shifts, on her phone.

Goal-
Pass A1 on the first attempt and keep her visa timeline on track.
Frustration-
Her teacher says she is fine, but nobody tells her for sure before she pays.
Needs-
A short, trustworthy check that shows what to fix before booking.

Whys: why this problem matters
Why 1 Why do learners fail? They book the exam without knowing if they are ready.
Why 2 Why? Finishing a course feels like readiness, and no objective check exists.
Why 3 Why? Mock tests are scattered, long or paid, so many learners skip them.
Why 4 Why? Feedback arrives only after the exam, when it is too late.
Why 5 A fail costs the fee, months on a visa timeline and confidence. The root cause: no quick readiness signal
before booking

What Webapp Does?
The learner answers 14 multiple-choice questions: 5 vocabulary, 5 grammar and 4 reading.
The app shows a verdict (Ready, Almost ready or Not yet) with an overall score.
It shows a score for each skill, compares the strongest and weakest, and lists the top 3 things to practise before booking.

The learner can review the questions that are wrong.

Why these rules:

60% is the pass mark for Goethe Start Deutsch.

All thresholds and weights live in one CONFIG object, so they are easy to change.

How “ready” is calculated
Skill score = difficulty-weighted % correct (easy = 1, medium = 1.5).
Overall score = average of the three skill scores.

Ready: - overall 75% or above, 
Almost ready: -60% - 74% everything in between, including a high overall score with one weak skill.
Not yet: - overall below 60% (the exam pass mark).

Skill score = weighted % correct

For each skill (vocabulary, grammar, reading), add up the points the learner earned and divide by the total points available:

skill score = points earned ÷ points available × 100

The points available per skill:

Vocabulary: 2 easy + 3 medium = 2 + 4.5 = 6.5 points
Grammar: 2 easy + 3 medium = 6.5 points
Reading: 2 easy + 2 medium = 2 + 3 = 5 points
3. Overall = average of the three skill scores

Add the three skill scores and divide by 3. Each skill counts equally, so a learner can’t hide a weak reading score behind a strong vocabulary score.

Worked example
Skill	What the learner missed	Points earned	Score
Vocabulary	One medium question	5 of 6.5	77%
Grammar	One medium question	5 of 6.5	77%
Reading	One easy and one medium question	2.5 of 5	50%

Overall = (77 + 77 + 50) ÷ 3 = 68%.

The verdict is Almost ready. The overall score is above the 60% pass mark, but it’s below 75%, and reading is below 60%. A learner like this would likely fail the real exam on reading, which is why one weak skill stops the “Ready” verdict.

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
