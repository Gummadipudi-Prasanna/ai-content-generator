
def generate_ai_content(topic, content_type, tone, length):

    topic_lower = topic.lower().strip()

    # ---------------------------------
    # 1. Detect Question-Based Topics
    # ---------------------------------

    is_question_topic = any(
        word in topic_lower
        for word in ["question", "questions", "interview", "q&a"]
    )

    # ---------------------------------
    # 2. Python Interview Questions
    # ---------------------------------

    if is_question_topic and "python" in topic_lower:

        qa_list = [
            (
                "What is Python?",
                "Python is a high-level, interpreted programming language "
                "known for its simple syntax and readability."
            ),
            (
                "What are the main features of Python?",
                "Python is easy to learn, dynamically typed, object-oriented, "
                "cross-platform, and has a large collection of libraries."
            ),
            (
                "What is the difference between a List and a Tuple?",
                "A List is mutable, which means its elements can be changed. "
                "A Tuple is immutable, which means its elements cannot be changed."
            ),
            (
                "What is the difference between == and is?",
                "The == operator compares values, whereas the is operator "
                "checks whether two variables refer to the same object."
            ),
            (
                "What are Python decorators?",
                "Decorators are functions that modify or extend the behavior "
                "of another function without changing its original code."
            )
        ]

        if length == "Short":
            qa_list = qa_list[:3]
        elif length == "Medium":
            qa_list = qa_list[:4]

        content = "\n\n".join(
            f"### {i}. {question}\n\n**Answer:** {answer}"
            for i, (question, answer) in enumerate(qa_list, start=1)
        )

        return f"""
# {topic}

## Introduction

Here are some important Python questions and answers
that can help learners prepare for Python interviews.

## Python Questions and Answers

{content}

## Conclusion

Practicing these questions can help improve your
understanding of Python programming concepts.

Keep learning and practicing!
"""

    # ---------------------------------
    # 3. Topic Knowledge Base
    # ---------------------------------

    topic_knowledge = {

        "react": {
            "intro": (
                "React.js is a popular JavaScript library used to build "
                "interactive and reusable user interfaces."
            ),
            "points": [
                "Component-based architecture helps developers create reusable UI components.",
                "Virtual DOM helps update the user interface efficiently.",
                "React Hooks make it easier to manage state and component behavior.",
                "React supports reusable components and efficient application development.",
                "A large community provides libraries, tools, and learning resources."
            ]
        },

        "python": {
            "intro": (
                "Python is a high-level programming language known "
                "for its simple syntax and wide range of applications."
            ),
            "points": [
                "Simple and readable syntax makes Python beginner-friendly.",
                "Python supports object-oriented and functional programming.",
                "It is widely used in web development, automation, and data science.",
                "Libraries and frameworks help speed up development.",
                "Python has a large developer community."
            ]
        },

        "django": {
            "intro": (
                "Django is a Python web framework used to build "
                "secure and maintainable web applications."
            ),
            "points": [
                "Built-in authentication helps manage user accounts.",
                "Django ORM simplifies database operations.",
                "The admin interface helps manage application data.",
                "Security features help protect web applications.",
                "Django REST Framework can be used to build REST APIs."
            ]
        },

        "javascript": {
            "intro": (
                "JavaScript is a programming language used "
                "to make websites interactive and dynamic."
            ),
            "points": [
                "JavaScript supports interactive web page behavior.",
                "It can be used for both frontend and backend development.",
                "Asynchronous programming helps handle API requests.",
                "Modern ES6 features improve code readability.",
                "Frameworks such as React help build complex interfaces."
            ]
        },

        "artificial intelligence": {
            "intro": (
                "Artificial Intelligence enables computer systems "
                "to perform tasks that normally require human intelligence."
            ),
            "points": [
                "AI can analyze large amounts of data.",
                "Machine learning helps systems identify patterns.",
                "Natural Language Processing helps computers understand text.",
                "AI can automate repetitive tasks.",
                "AI is used in healthcare, education, business, and technology."
            ]
        }
    }

    # ---------------------------------
    # 4. Find Matching Topic
    # ---------------------------------

    selected_data = None

    for keyword, data in topic_knowledge.items():
        if keyword in topic_lower:
            selected_data = data
            break

    # ---------------------------------
    # 5. Generic Content Fallback
    # ---------------------------------

    if selected_data is None:

        selected_data = {
            "intro": (
                f"{topic} is the subject of this {content_type}. "
                "This article introduces the topic and highlights "
                "some important areas to explore."
            ),
            "points": [
                f"Introduction and overview of {topic}.",
                f"Important concepts and features related to {topic}.",
                f"Common applications and use cases of {topic}.",
                f"Benefits and challenges associated with {topic}.",
                f"Useful practices and recommendations for {topic}."
            ]
        }

    # ---------------------------------
    # 6. Length Selection
    # ---------------------------------

    points = selected_data["points"]

    if length == "Short":
        points = points[:3]

    elif length == "Medium":
        points = points[:4]

    elif length == "Long":
        points = points[:5]

    # ---------------------------------
    # 7. Tone Selection
    # ---------------------------------

    if tone == "Friendly":

        introduction = (
            f"Let's explore {topic}! {selected_data['intro']}"
        )

        conclusion = (
            f"We hope this overview helps you learn more about {topic}!"
        )

    elif tone == "Creative":

        introduction = (
            f"Discover the world of {topic}! {selected_data['intro']}"
        )

        conclusion = (
            f"Keep exploring the possibilities of {topic}!"
        )

    else:

        introduction = selected_data["intro"]

        conclusion = (
            f"In conclusion, {topic} offers useful concepts "
            "and opportunities to explore."
        )

    # ---------------------------------
    # 8. Generate Final Content
    # ---------------------------------

    highlights = "\n".join(
        f"{i + 1}. {point}"
        for i, point in enumerate(points)
    )

    generated_content = f"""
# {topic}

## Introduction

{introduction}

## {content_type} - Key Highlights

{highlights}

## Conclusion

{conclusion}

Thank you for reading!
"""

    return generated_content
