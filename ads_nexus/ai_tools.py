import random

# Sample data for AI content generation
HEADLINES = [
    "Boost Your Sales Today with Our Unique Strategy!",
    "Unlock Your Business Potential with Targeted Ads!",
    "Create Viral Content in Minutes with Our AI!"
]

DESCRIPTIONS = [
    "Our AI-driven tools make marketing effortless and effective.",
    "Engage your audience with personalized, dynamic ads.",
    "Experience the future of advertising with AI-powered insights."
]

CALL_TO_ACTIONS = [
    "Sign Up Now!",
    "Start Your Free Trial!",
    "Learn More Today!"
]

def generate_creative_content():
    """
    Generate AI-driven ad content including a headline, description, and call-to-action.
    """
    headline = random.choice(HEADLINES)
    description = random.choice(DESCRIPTIONS)
    call_to_action = random.choice(CALL_TO_ACTIONS)

    return {
        "headline": headline,
        "description": description,
        "call_to_action": call_to_action
    }
