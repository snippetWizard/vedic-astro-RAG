import json
from typing import Dict, Any, List

# -------------------------------------------------
# 1. Static knowledge bases for planet behavior
# -------------------------------------------------

PLANET_ARCHETYPES = {
    "Sun": {
        "keywords": "ego, identity, vitality, authority, visibility",
        "style": "I will lead. I must be seen.",
    },
    "Moon": {
        "keywords": "emotion, intuition, nurturing, sensitivity, bonding",
        "style": "I feel, I care, I respond emotionally.",
    },
    "Mars": {
        "keywords": "drive, force, survival, assertion, anger",
        "style": "I act. I push. I take territory.",
    },
    "Mercury": {
        "keywords": "logic, speech, thinking, adaptability, negotiation",
        "style": "I analyze, explain, and move fast between ideas.",
    },
    "Venus": {
        "keywords": "love, pleasure, attraction, harmony, aesthetics",
        "style": "I attract, I charm, I create sweetness.",
    },
    "Jupiter": {
        "keywords": "wisdom, ethics, growth, optimism, teaching",
        "style": "I guide, I expand, I believe in meaning.",
    },
    "Saturn": {
        "keywords": "discipline, pressure, reality, duty, time, karma",
        "style": "I endure. I take responsibility. I accept limits.",
    },
    "Rahu": {
        "keywords": "obsession, hunger, ambition, fame, disruption",
        "style": "I want more. I don’t care about the rules.",
    },
    "Ketu": {
        "keywords": "detachment, dissolving ego, past-life maturity, intuition",
        "style": "I let go. I transcend. I’m already done with this.",
    }
}


# -------------------------------------------------
# 2. Planet-in-house interpretation library
#    For each house, each planet gets:
#    - summary
#    - positives
#    - negatives
# -------------------------------------------------
# NOTE: You can grow this over time. Right now we embed
#       the logic we already wrote (1st..12th houses).


PLANET_IN_HOUSE_LIBRARY: Dict[str, Dict[str, Dict[str, Any]]] = {
    # house_number -> planet -> data
    "1": {
        "Sun": {
            "summary": "Sun in the 1st house creates a powerful, visible personality.",
            "positive": [
                "Leadership aura and natural authority.",
                "High confidence and willpower.",
                "Strong physical presence, noticeable energy."
            ],
            "negative": [
                "Ego clashes and 'my way only' attitude.",
                "Impatience with others.",
                "Can strain relationships by being too dominant."
            ],
        },
        "Moon": {
            "summary": "Moon in the 1st house makes the self emotional, intuitive, and sensitive.",
            "positive": [
                "Warm, caring presence that people trust.",
                "Strong empathy and emotional intelligence.",
                "Magnetic softness in personality."
            ],
            "negative": [
                "Mood swings and emotional dependency.",
                "Restlessness and anxiety if unsupported.",
                "Easily hurt by criticism."
            ],
        },
        "Mars": {
            "summary": "Mars in the 1st house gives force, competitiveness, survival instinct.",
            "positive": [
                "Fearless, bold, courageous.",
                "Action taker, natural fighter under pressure.",
                "Determined and intense presence."
            ],
            "negative": [
                "Short temper and impulsive reactions.",
                "Can intimidate or dominate others.",
                "Relationship friction (Manglik-type tension)."
            ],
        },
        "Mercury": {
            "summary": "Mercury in the 1st house makes identity revolve around intelligence, words, and adaptability.",
            "positive": [
                "Smart, witty, fast communicator.",
                "Socially flexible, can read rooms fast.",
                "Youthful and curious energy."
            ],
            "negative": [
                "Overthinking and nervousness.",
                "Scattered attention.",
                "Blunt honesty can offend people."
            ],
        },
        "Venus": {
            "summary": "Venus in the 1st house adds charm, grace, social attractiveness.",
            "positive": [
                "Pleasant personality and aesthetic sense.",
                "Diplomatic and likable in first impressions.",
                "Naturally magnetic in social situations."
            ],
            "negative": [
                "Vanity and image-obsession.",
                "Can manipulate with sweetness.",
                "Romantic drama if seeking constant attention."
            ],
        },
        "Jupiter": {
            "summary": "Jupiter in the 1st house makes the self wise, ethical, and protective.",
            "positive": [
                "Guiding, mentor-like presence.",
                "Optimistic and morally grounded.",
                "Respected by others, seen as reliable."
            ],
            "negative": [
                "Overconfidence: 'I know what's best for everyone.'",
                "Unrealistic optimism.",
                "Overindulgence, comfort-seeking."
            ],
        },
        "Saturn": {
            "summary": "Saturn in the 1st house makes the person serious, responsible, disciplined.",
            "positive": [
                "High endurance, can handle pressure.",
                "Mature beyond age.",
                "Shows reliability and duty."
            ],
            "negative": [
                "Self-doubt, heaviness, pessimism.",
                "Slow to trust or open up.",
                "Carries emotional weight alone."
            ],
        },
        "Rahu": {
            "summary": "Rahu in the 1st house creates extreme hunger for identity, fame, and impact.",
            "positive": [
                "Magnetic, unforgettable presence.",
                "Bold risk-taker who doesn't fear judgment.",
                "Can gain influence quickly."
            ],
            "negative": [
                "Identity confusion and restlessness.",
                "Obsession with status or public image.",
                "Impulsive, addictive patterns."
            ],
        },
        "Ketu": {
            "summary": "Ketu in the 1st house gives spiritual detachment and mysterious aura.",
            "positive": [
                "Deep intuition and insight.",
                "Can stay calm in ego games.",
                "Feels 'older than their age' spiritually."
            ],
            "negative": [
                "Low self-esteem in youth.",
                "Social withdrawal or coldness.",
                "Difficulty forming stable identity."
            ],
        }
    },

    # We’ll embed a lighter version for the rest of the houses for now.
    # You can expand this dict further (2..12 for all planets).
    # For demo, I’ll include Mars in 2, Venus in 3, Saturn in 4, Moon in 5,
    # Jupiter in 6 & 7, Rahu in 8, Ketu in 9, Sun in 10, Mars in 11, Venus in 12.
    # This covers the planets we used in the Sagar example.

    "2": {
        "Mars": {
            "summary": "Mars in the 2nd house makes speech bold and money approach aggressive.",
            "positive": [
                "Protective about family resources.",
                "Courage to earn independently.",
                "Can negotiate hard and win."
            ],
            "negative": [
                "Harsh words that hurt loved ones.",
                "Money fights in family.",
                "Impulse spending and risky bets."
            ]
        }
    },

    "3": {
        "Venus": {
            "summary": "Venus in the 3rd house makes communication stylish, attractive, and persuasive.",
            "positive": [
                "Great at relationship-building through words.",
                "Good for branding, marketing, content creation.",
                "Naturally socially likable voice."
            ],
            "negative": [
                "May manipulate emotionally to avoid conflict.",
                "Can sugarcoat instead of being direct.",
                "Image can matter more than truth."
            ]
        }
    },

    "4": {
        "Saturn": {
            "summary": "Saturn in the 4th house creates emotional heaviness but huge loyalty to family.",
            "positive": [
                "Takes responsibility at home.",
                "Thinks long-term about security and property.",
                "Very resilient under emotional stress."
            ],
            "negative": [
                "Feels lonely or unsupported emotionally.",
                "Heavy bond with mother or homeland.",
                "Difficulty relaxing or feeling safe."
            ]
        }
    },

    "5": {
        "Moon": {
            "summary": "Moon in the 5th house makes romance and creativity emotional and nurturing.",
            "positive": [
                "Loving, caring romantic style.",
                "Strong imagination and artistic intuition.",
                "Good with kids / mentoring younger people."
            ],
            "negative": [
                "Mood swings in love life.",
                "Needs attention/validation in romance.",
                "Emotions affect focus and creative output."
            ]
        }
    },

    "6": {
        "Jupiter": {
            "summary": "Jupiter in the 6th house wants to solve problems ethically and guide others.",
            "positive": [
                "Supportive teammate and advisor.",
                "Wins conflicts through fairness and wisdom.",
                "Good for service, consulting, mentoring."
            ],
            "negative": [
                "May act morally superior at work.",
                "Overextends trying to save others.",
                "Ignores own health to help everyone else."
            ]
        }
    },

    "7": {
        "Jupiter": {
            "summary": "Jupiter in the 7th house attracts wise, supportive partners.",
            "positive": [
                "Partners who bring growth and encouragement.",
                "Long-term mindset in relationships.",
                "Honesty and loyalty valued."
            ],
            "negative": [
                "Over-idealizing the partner.",
                "Turning every argument into a 'teaching moment'.",
                "Control disguised as guidance."
            ]
        }
    },

    "8": {
        "Rahu": {
            "summary": "Rahu in the 8th house is obsession with power, secrets, intensity, taboo.",
            "positive": [
                "Fearless in crisis situations.",
                "Deep psychological insight.",
                "Access to transformation others can't handle."
            ],
            "negative": [
                "Paranoia, control issues, secrecy.",
                "Rollercoaster mental states.",
                "Tangled or hidden power struggles."
            ]
        }
    },

    "9": {
        "Ketu": {
            "summary": "Ketu in the 9th house rejects shallow belief systems and chases real truth.",
            "positive": [
                "Strong inner spiritual compass.",
                "Doesn't fall for fake gurus.",
                "Wisdom through introspection."
            ],
            "negative": [
                "Disconnection from mentors or father figures.",
                "Restlessness with traditional education.",
                "Temporary loss of 'clear purpose' feeling."
            ]
        }
    },

    "10": {
        "Sun": {
            "summary": "Sun in the 10th house flags public recognition, leadership, and visible career ambition.",
            "positive": [
                "Strong reputation and authority energy.",
                "Wants to build something significant.",
                "Can lead, command, or run operations."
            ],
            "negative": [
                "Workaholic identity (self-worth = career status).",
                "Clashes with bosses / authority structures.",
                "Low tolerance for incompetence in teams."
            ]
        }
    },

    "11": {
        "Mars": {
            "summary": "Mars in the 11th house is raw drive to hit big goals fast.",
            "positive": [
                "Willpower to scale income and influence.",
                "Can mobilize networks quickly.",
                "Competitive hunger to win socially."
            ],
            "negative": [
                "Rivalries and jealousy in friend circles.",
                "Burns bridges if results are slow.",
                "Treats allies like soldiers, not humans."
            ]
        }
    },

    "12": {
        "Venus": {
            "summary": "Venus in the 12th house creates private fantasies, secret pleasures, and healing through beauty.",
            "positive": [
                "Art, music, romance become forms of escape and restoration.",
                "Can find peace in solitude, travel, retreat.",
                "Very loving in private, soft with trusted people."
            ],
            "negative": [
                "Escapism via pleasure / fantasy / spending.",
                "Hidden relationships, secrecy in love.",
                "Spends quietly on comfort or indulgence."
            ]
        }
    }
}


def load_house_lords_map(path: str) -> Dict[str, Any]:
    """
    Loads house_lords.json and returns a dict keyed by house_number as string.
    Easier to join with incoming data that will give house numbers as strings.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    out = {}
    for entry in raw["house_lords"]:
        hn = str(entry["house_number"])
        out[hn] = entry
    return out


def interpret_chart(user_payload: Dict[str, Any], house_lords_map: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build the final JSON response for the user.
    user_payload:
    {
      "name": "...",
      "dob": "...",
      "lat": ...,
      "long": ...,
      "houses": {
        "1": "Sun",
        "2": "Mars",
        ...
      }
    }

    Steps:
    - For each house_number in user_payload["houses"]:
        - get planet sitting there
        - get house meta (theme, natural_lord)
        - get planet-in-house meaning from PLANET_IN_HOUSE_LIBRARY
        - build host_guest_dynamics text using planet + house natural lord
    """

    name = user_payload.get("name")
    dob = user_payload.get("dob")
    lat = user_payload.get("lat")
    long_ = user_payload.get("long")
    houses = user_payload.get("houses", {})

    interpretations_out: List[Dict[str, Any]] = []
    summary_points_for_user: List[str] = []

    for house_num, planet in houses.items():
        house_info = house_lords_map.get(str(house_num))
        if not house_info:
            continue

        natural_lord = house_info["natural_lord"]
        house_theme = house_info["theme"]
        house_name = house_info["house_name"]

        planet_block = PLANET_IN_HOUSE_LIBRARY.get(str(house_num), {}).get(planet)

        if planet_block:
            summary = planet_block["summary"]
            pos = planet_block["positive"]
            neg = planet_block["negative"]
        else:
            # fallback if we didn't define that combo yet
            summary = f"{planet} in the {house_name} influences {house_theme.lower()}."
            pos = ["Positive traits not yet defined for this placement."]
            neg = ["Challenging traits not yet defined for this placement."]

        # Build the host-guest dynamic statement
        host_guest_line = (
            f"{planet} is operating inside a house that is naturally guided by {natural_lord}. "
            f"This creates a 'guest in someone else's home' effect, where {planet} expresses its nature "
            f"through the style and rules of {natural_lord}."
        )

        interpretations_out.append({
            "house_number": int(house_num),
            "house_name": house_name,
            "house_theme": house_theme,
            "natural_lord": natural_lord,
            "occupying_planet": planet,
            "interpretation": {
                "summary": summary,
                "host_guest_dynamics": host_guest_line,
                "positive_traits_current": pos,
                "negative_traits_current": neg
            }
        })

        # for top-level summary
        summary_points_for_user.append(
            f"{planet} in House {house_num}: {summary}"
        )

    final_payload = {
        "user": {
            "name": name,
            "dob": dob,
            "lat": lat,
            "long": long_
        },
        "interpretations": interpretations_out,
        "summary_for_user": " | ".join(summary_points_for_user)
    }

    return final_payload
