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
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            "Working at a job can be draining but we all do it for the same reason, a paycheck. Meanwhile, getting that constant paycheck can provide a sense of security and stability that we get stuck in. This would lead to goals and dreams being pushed back because we do not want to lose that sense of security.",
            "Why do we continue to work jobs that drain us, even when we know they are not fulfilling our dreams?",
            "Having a relationship, especially long distant relationships can be a grey area. Very challenging but if the love actually exists, it can stay true.",
            "I want a laptop, preferely a gaming laptop. I have also been thinking about getting a PS5 console, but i am having second thoughts cause of the tight schedule with work and school. Also, the money for it.",
            "Learning never gets boring, but understanding that there are so many things you do not know, while others are around know it can be humbling for sure. Now it gets you in state that i also have to learn more about everything.",
            "A knower of all is a master of none, is a very false statement. I can know about many things and use it to create something very niche that even the masters in their aspects will want to be part of the growth.",
            "Proscastination can really hinder your progress, and leads to missed opportunites. Whatever you want to do make sure to work on it immediately, or set a schedule you want to do, and make sure to do it.",
            "I understand the importance of people management and it all ties to effective communication and the ability to listen effectively.",
            "It was veteran's day yesterday. I forgot to wish my friend, and it means i am not really a good friend. I have to try to help them but firslty help myself.",
            "Men, we strrugle with a lot of things. Loneliness, masturbation, relationships, social anxiety, communitites. What we have to understand is it that as long as you keep grinding, and working through everything, it all gets better. Dont beat yourself up for something, rather fall and get back up is the only way to keep pushing forward.",
        ],
    },
    {
        "name": "AI paragraphs",
        "criterion": 2,
        "texts": [
            "Time management is an essential skill that can significantly improve both personal and professional outcomes. By prioritizing tasks, setting clear goals, and minimizing distractions, individuals can make better use of their limited hours. Furthermore, regularly reviewing progress allows for adjustments that keep efforts aligned with long-term objectives. Ultimately, effective time management reduces stress, enhances productivity, and creates space for activities that bring fulfillment and balance to everyday life.",
            "Regular exercise offers numerous benefits for both physical and mental well-being. It strengthens the cardiovascular system, improves muscle tone, and boosts energy levels throughout the day. Additionally, physical activity has been shown to reduce symptoms of anxiety and depression by releasing endorphins. By incorporating consistent movement into their routines, individuals can enhance their overall quality of life and build habits that support long-term health and resilience.",
            "Renewable energy plays a crucial role in addressing the challenges of climate change. Sources such as solar, wind, and hydroelectric power provide sustainable alternatives to fossil fuels, significantly reducing greenhouse gas emissions. Moreover, advances in technology have made these options increasingly affordable and efficient. As governments and businesses continue to invest in clean energy, the transition toward a more sustainable future becomes both achievable and economically beneficial for societies worldwide.",
            "Effective communication is the foundation of strong relationships in both personal and professional settings. It involves not only expressing ideas clearly but also listening actively and responding with empathy. By fostering open dialogue, individuals can resolve conflicts, build trust, and collaborate more successfully. In an increasingly connected world, the ability to communicate thoughtfully remains one of the most valuable skills a person can develop and refine over time.",
            "Education serves as a powerful tool for personal growth and societal progress. It equips individuals with the knowledge and critical thinking skills necessary to navigate an increasingly complex world. Furthermore, access to quality education promotes equality by providing opportunities for people from diverse backgrounds. By investing in learning at every stage of life, communities can foster innovation, strengthen economies, and cultivate informed citizens who contribute meaningfully to society.",
            "Cybersecurity has become a critical concern in the digital age. As organizations rely more heavily on interconnected systems, the risk of data breaches and cyberattacks continues to grow. Implementing strong passwords, multi-factor authentication, and regular software updates can significantly reduce vulnerabilities. Moreover, fostering a culture of security awareness among employees ensures that everyone plays a role in protecting sensitive information and maintaining trust with customers and partners.",
            "A balanced diet is fundamental to maintaining good health and sustaining energy throughout the day. It includes a variety of fruits, vegetables, whole grains, lean proteins, and healthy fats. Additionally, staying hydrated and practicing portion control can help prevent chronic conditions such as diabetes and heart disease. By making mindful food choices, individuals can support their immune systems, improve their mood, and promote long-term wellness and vitality.",
            "Travel provides valuable opportunities to explore new cultures, perspectives, and ways of life. Experiencing unfamiliar environments encourages adaptability and broadens one's understanding of the world. Moreover, interacting with people from different backgrounds fosters empathy and mutual respect. Whether visiting a nearby town or a distant country, travel enriches the mind, creates lasting memories, and inspires a deeper appreciation for the diversity that makes our global community so remarkable.",
            "Artificial intelligence is transforming industries by automating routine tasks and enabling data-driven decision-making. In healthcare, it assists with diagnostics, while in finance, it helps detect fraudulent transactions. However, the rapid adoption of AI also raises important ethical considerations, including privacy, bias, and accountability. By developing responsible frameworks and promoting transparency, society can harness the benefits of this technology while minimizing potential risks and unintended consequences.",
            "Volunteering is a meaningful way to give back to the community while developing new skills and relationships. By dedicating time to causes they care about, individuals can make a tangible difference in the lives of others. Additionally, volunteering fosters a sense of purpose and belonging, which contributes to improved mental well-being. Whether through local organizations or global initiatives, service strengthens communities and inspires others to contribute positively to the world.",
        ],
    },
    {
        "name": "bad requests",
        "criterion": 3,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "   ", "creator_id": "eval_bad_spaces"},
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
