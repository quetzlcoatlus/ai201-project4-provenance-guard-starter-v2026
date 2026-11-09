"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

A "texts" scenario can also set "appeal": True. Then each text is submitted and
its content_id appealed, instead of just submitted — see
`run_eval.py::run_appeal_trial`.
"""

# ── The texts. Each is written once here and reused by the scenarios below. ──

# Pieces written entirely by me. Used by criterion 1.
MY_WRITING = [
    "I had a dream last night where I was in a plane crash I think? Not sure if there were Attack On Titan characters in it. It was kinda weird... as usual for dreams. It wasn't even really scary until the part where it went underwater and I went with it. I think the roof was open? Pretty much got nothing left of it. It was part of some kind of amusement ride if I recall correctly. I think I had another one this transitioned into where I was like, following Susie from Deltarune somewhere. Then it transformed into some pixel art side-scroller thing where there was a large guy and a skinny guy. Think they were championing for something to someone after something happened. Dust and echoes at this point. It's always annoying when I want to remember a dream but 20 minutes after it's over I have the faintest thread of it left. Thank you deeper memory processing or whatever. It felt good to sleep a little bit longer today, like 01:00 to 12:00. Sometimes I need to make up for the week, especially after I'm being a bit more hedonistic for fun the night before. I tend to look forward to Saturdays. I don't have much time off recently so I try my best to have Saturday free to unwind for the entire day. Most of the time I do a video game for a long time and I get burnt out or the dopamine just isn't hitting anymore and I get bored. Then I start wondering if I should've been doing something more boring/productive so that the evening is relatively joyful vs. feeling tired by 17:00.",
    "Persona is probably my favorite game series that I've ever played. I really like the social aspect. It's basically like reliving high school and getting to experiment with different priorities. Like there's incentive for building deep social links which simulates networking/making real friends. There's incentive to build up your skills (they're very general so not especially practical) like intelligence, guts, charm, etc. to succeed at different tasks. You have to pick one to focus on and getting all of them up basically takes all of your free time away. There are meaningful choices that mean you won't be able to do something that you would've been able to do on a different trajectory. I think that sort of thing should be common curriculum honestly. I had a lot of trouble dealing with decision paralysis growing up so being able to try things in a simulation might've been helpful, even if they were abstractions of what the real experience is like. Time is usually a lot slower than the games since, in order to be fun and playable within a lifetime, they compact a year into about 100 hours of gameplay. So rest and burn out that would probably be there normally is abstracted away. Kind of a rough takeaway in hindsight but end of the day it's a game that's meant to be fun and a learning experience second. Interacts with Capitalism in a sense where there's just obsession with productivity in order to 100% the game. Which, if you plan extremely well, is possible in one run. ",
]

# My writing, partly edited with AI. Should land in unsure. Criteria 1 and 3.
BORDERLINE = [
    "I apparently convinced someone to rethink their transphobia. A few days ago, he was making the familiar argument on Reddit: 'Why should I have to use your pronouns? You're not special.' I replied that expecting basic respect isn't special; it's normal. Today he messaged me to apologize, explaining that he had held that mindset for most of his life. Because he had been bullied in school for being overweight, the idea that someone outside the norm could expect kindness felt foreign to him. He believed decent treatment was something you had to earn. It's a good reminder that not everyone is beyond reach. 🪷",
    "Last night I dreamed I was in a plane crash, or at least I think I was. Not sure if there were Attack On Titan characters in it. It was strange, as dreams usually are. It wasn't even really scary until the part where it went underwater and I went with it. I think the roof was open? Pretty much got nothing left of it. It was part of some kind of amusement ride if I recall correctly. I think I had another one this transitioned into where I was like, following Susie from Deltarune somewhere. Then it transformed into some pixel art side-scroller thing where there was a large guy and a skinny guy. Think they were championing for something to someone after something happened. Dust and echoes at this point. It's always frustrating when I want to remember a dream, only to find that twenty minutes later just the faintest thread of it remains. Thank you deeper memory processing or whatever. It felt good to sleep a little bit longer today, like 01:00 to 12:00. Sometimes I need to make up for the week, especially after I'm being a bit more hedonistic for fun the night before. I tend to look forward to Saturdays. I don't have much time off recently so I try my best to have Saturday free to unwind for the entire day. Most of the time, I end up playing a video game for hours until I burn out or the dopamine stops hitting, and I get bored. Then I start wondering if I should've been doing something more boring/productive so that the evening is relatively joyful vs. feeling tired by 17:00.",
    "Persona is probably my favorite game series that I've ever played. What I appreciate most is the social aspect; it essentially lets you relive high school while experimenting with different priorities. Like there's incentive for building deep social links which simulates networking/making real friends. There's incentive to build up your skills (they're very general so not especially practical) like intelligence, guts, charm, etc. to succeed at different tasks. You have to pick one to focus on and getting all of them up basically takes all of your free time away. There are meaningful choices that mean you won't be able to do something that you would've been able to do on a different trajectory. Honestly, I think that kind of experience should be part of a standard curriculum. I had a lot of trouble dealing with decision paralysis growing up so being able to try things in a simulation might've been helpful, even if they were abstractions of what the real experience is like. Time is usually a lot slower than the games since, in order to be fun and playable within a lifetime, they compact a year into about 100 hours of gameplay. So rest and burn out that would probably be there normally is abstracted away. In hindsight, that's a somewhat rough takeaway, but at the end of the day, it's a game meant to be fun first and a learning experience second. It also reflects a capitalist mindset in a way, with its emphasis on maximizing productivity to 100% the game, which is possible in a single run if you plan extremely carefully.",
]

# Pre-labelled clearly AI. Should land in high-confidence AI. Criteria 3 and 4.
CLEARLY_AI = [
    (
        "Coffee is more than just a beverage; it is a rich tapestry of culture, history, and "
        "community. Originating in the highlands of Ethiopia, coffee has journeyed across "
        "continents, shaping economies and fostering connection along the way. It is important "
        "to note that coffee offers several potential benefits, including improved focus, "
        "enhanced energy levels, and a sense of comfort. Furthermore, the ritual of preparing "
        "coffee can serve as a mindful moment in an otherwise busy day. However, it is also "
        "essential to consume coffee in moderation, as excessive intake may lead to restlessness "
        "or disrupted sleep. In conclusion, coffee remains a multifaceted and beloved part of "
        "daily life for millions of people around the world."
    ),
    (
        "Time management is a crucial skill that can significantly enhance both personal and "
        "professional success. By prioritizing tasks effectively, individuals can reduce stress, "
        "increase productivity, and achieve a healthier work-life balance. There are several key "
        "strategies to consider. First, setting clear and achievable goals provides direction and "
        "motivation. Second, breaking larger projects into smaller, manageable steps can make "
        "complex tasks feel less overwhelming. Third, minimizing distractions, such as unnecessary "
        "notifications, allows for deeper focus. Additionally, it is important to schedule regular "
        "breaks to maintain energy and prevent burnout. Ultimately, mastering time management is "
        "an ongoing journey that empowers individuals to unlock their full potential."
    ),
    (
        "The ocean is a vast and mysterious realm that plays a vital role in sustaining life on "
        "Earth. Covering more than seventy percent of the planet's surface, it regulates the "
        "climate, produces a significant portion of the oxygen we breathe, and supports an "
        "incredibly diverse array of ecosystems. From vibrant coral reefs to the depths of the "
        "abyssal plains, the ocean is home to countless species, many of which remain "
        "undiscovered. Nevertheless, it faces numerous challenges, including pollution, "
        "overfishing, and rising temperatures. Addressing these issues requires a collaborative "
        "and multifaceted approach. By fostering awareness and embracing sustainable practices, "
        "we can help ensure that the ocean continues to thrive for generations to come."
    ),
]

# Pre-labelled clearly human. Should land in high-confidence human. Criteria 3 and 4.
CLEARLY_HUMAN = [
    "Convinced a guy to stop being transphobic apparently. Other day he was doing the usual 'why should I be expected to use your pronouns, you're not special' thing on reddit. I responded 'Expecting people to show you basic respect isn't special, it's normal'. He messaged me today and apologized since for most of his life he was in that mindset. Apparently due to being bullied in school for being overweight, the idea of expecting kindness when you exist outside the norm was alien to him. Like it was necessary to 'earn' the right to be treated decently. Not all of them are hopeless 🪷",
    "The world is in chaos, but for the bosses, it's all going according to plan. We can see their plan in the countless heartbreaking images coming out of war zones like Beirut, Gaza, and Tehran. We can hear it in the rumble of bulldozers making way to build detention camps and data centers. We can feel it in the air as the summer heat becomes unbearable, and in the pits of our stomachs when faced with the price of gas and rent. We're promised magical technology with AI, but in reality, the bosses lay us off and track our every move. The billionaire class is dividing workers against each other, and it's making us desperate and miserable. The political and economic system under which we live is built on private ownership and profit at all costs. As capitalism fails to solve problems of its own making, it turns to right-wing authoritarianism. Big business makes deals with the government to line their pockets, and politicians stoke hatred between working people. Instead of offering real solutions to unemployment and the cost of living, they attack immigrants, communities of color, and trans people. Rather than fixing our broken healthcare system, they push snake oil and circulate conspiracy theories. The Republicans are in on it, the Democratic Party is asleep at the wheel, and both are funded by the same criminal class of billionaires and war profiteers.",
    "Democratic socialists know that no one has to live like this. If we lived in a classless society and governed ourselves, we could freely build a world without war or poverty. We could build a world where no one suffers for their race, gender, or religion, and everyone is free, equal, and cared for. Building this world is the guiding star of our movement. When we labor for our common good instead of private profit, we can all have a secure and dignified life, and use our time and talents how we wish. To achieve this future, our class must organize. The Democratic Socialists of America is building a party whose goal is a democratic society of the working class. Our enemies are not just individual bosses, but the entire global system of capital; not just this or that cop, judge, or president, but the entire anti-democratic structure of our society. We are workers fighting to transform society: to win the battle for democracy, draft a new constitution, and create a democratic socialist republic. DSA has written this program for ending capitalist oligarchy and creating a real democracy. Some of these demands may be won under our current system, but we know complete victory will require building a new society from the ground up. We push these demands to their furthest extent today, so we can fight for their fullest realization in a socialist future. Join us.",
]

# Anything scoreable. Each trial submits these fresh, giving 5 new content_ids
# to appeal against. The wording doesn't matter. Criterion 2.
APPEAL_SUBMISSIONS = [
    f"Appeal path test submission {i}. The content of this text does not matter, "
    f"only the content_id that comes back."
    for i in range(1, 6)
]


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Pass: 0 of 5 come back guess "ai", in every trial. unsure is fine.
        "texts": BORDERLINE + MY_WRITING,
    },
    {
        "name": "appeal path",
        "criterion": 2,
        # "appeal": run_eval.py submits each text, appeals the content_id that
        # comes back (expect 200), repeats one appeal (expect 409), appeals a
        # made-up id (expect 404), then checks every result against the log.
        "appeal": True,
        "texts": APPEAL_SUBMISSIONS,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Pass: every text reaches its intended label, in every trial.
        "texts": CLEARLY_AI + BORDERLINE + CLEARLY_HUMAN,
    },
    {
        "name": "score spread",
        "criterion": 4,
        # Pass: lowest clearly-AI combined score is >= 0.3 above the highest
        # clearly-human combined score, in every trial.
        "texts": CLEARLY_AI + CLEARLY_HUMAN,
    },
    {
        "name": "bad input",
        "criterion": 5,
        # Pass: the first six get a 400 naming the problem, never a 500. The
        # long one gets a 200 with a `warnings` entry about truncation.
        "bodies": [
            {"creator_id": "eval_bad_missing"},                  # no text field at all
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n\t ", "creator_id": "eval_bad_whitespace"},
            {"text": 42, "creator_id": "eval_bad_int"},
            {"text": ["not", "a", "string"], "creator_id": "eval_bad_list"},
            {"text": "word " * 600, "creator_id": "eval_long"},  # well over 400 tokens
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
