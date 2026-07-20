# Unit 6: Principles of Artificial Intelligence (AI) I

## Unit Topic

This unit covers foundational AI principles: the distinctions between AI,
Machine Learning, and Deep Learning, practical applications like
automation and predictive analytics, and the ethical challenges of AI
adoption, including bias, transparency, and accountability.

## Learning Outcomes

On completion of this unit, I should be able to:

- Identify and critically analyze the challenges and opportunities of
  integrating AI into business systems.
- Evaluate AI methodologies and techniques to solve computing challenges
  in enterprise contexts.
- Articulate the legal, social, and ethical implications of AI
  technologies.

## Formative Assignment

Implement a simple AI prediction model using Python and Scikit-learn,
train it on a public dataset, evaluate its performance, and discuss its
limitations and ethical considerations in a 300-word analysis.

Full submission: https://github.com/fchagnon/essex-eportfolio/tree/main/LIC/Unit%206

## Reading List

Manure, A. and Bengani, S. (2023) *Introduction to Responsible AI:
Implement Ethical AI Using Python*. Berkeley, CA: Apress. Chapters 1-4.

## Reflection

I chose NHL game outcomes, using MoneyPuck's twenty years of game-by-game
statistics, over a more conventional dataset, since I wanted to test
whether "home ice advantage" was a real, measurable effect or just
sports folklore.

**Identifying challenges in integrating AI into systems.** My first
model, predicting a win from a team's own average performance over its
last five games, hit 67.41% accuracy, which looked good until I looked
closer: the model had noticed that losses were more common in that data
slice and simply predicted "loss" for every game. It was technically
accurate and strategically useless, a genuine, concrete example of a
model finding the path of least resistance rather than actually learning
the problem I intended.

**Evaluating AI methodologies for enterprise challenges.** Fixing this
meant forcing the model to compare two opponents directly rather than
evaluate a team in isolation, a comparative delta architecture weighing
puck possession (Corsi), shot quality (expected goals), and rolling
goals for and against. This dropped accuracy to 52.45%, lower, but
honest. I then tried using home-ice advantage as a tiebreaker for
closely matched teams, and the model assigned it a predictive weight of
zero. The explanation turned out to be the actual finding: home ice's
benefits (shorter line changes, crowd support, last change) had already
been converted into superior puck possession and shot quality stats
before the game even started, so home ice isn't a switch flipped at
face-off, it's a persistent performance effect already baked into the
recent data. The model's 52.45% also sat close to the 54.5% historical
home-win probability from long-term league studies (Swartz, Gill and
Muthootoo, 2011), suggesting the small remaining gap is likely explained
by factors the model doesn't see at all, travel fatigue, goaltender
rotation, rather than anything mystical about home advantage itself.

**Articulating ethical implications.** Relying on expected-goals-style
metrics risks undervaluing players whose contribution is leadership or
defensive grit that doesn't show up in a spreadsheet, a real risk if
this kind of model informed contract negotiations. The model is also
blind to current roster reality, it has no way of knowing a star player
is injured or a backup goalie is starting, and using it uncritically
risks a self-fulfilling prophecy where underdogs are written off on
incomplete history rather than the actual game in front of them.

## Tutor Feedback and Response

**Feedback.** A good submission, with particular praise for the
discussion of which variables mattered and the discovery that model
performance depends heavily on variable and algorithm choice. The one
note: citations were used well, but more would have strengthened it
further.

**My response.** A fair, easy addition to make going forward, the
analysis leaned on two sources (MoneyPuck for the data itself, and
Swartz, Gill and Muthootoo for the historical benchmark), and a genuinely
interesting result like the home-ice finding could likely have supported
a wider literature search on the underlying sports analytics research,
rather than relying on a single comparison point to validate it.
