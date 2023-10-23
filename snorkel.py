import re
import pandas as pd
from snorkel.labeling import PandasLFApplier

df = pd.read_csv("uniquejobs.csv")


@labeling_function()
def is_realistic_entry_level(x):
    experience_patterns = [
        r"\b\d+-\d+\syears\sof\sproven\sexperience\b",
        r"\b\d+\+\syears\sof\sexperience",
        r"\b\d+\s?to\s?\d+\syears",
        r"\b(at\sleast|minimum|min\.?)\s\d+\s(years|yr)",
        r"\bproven\strack\srecord\sof\sat\sleast\s\d+\syears",
        r"\bsignificant\sexperience",
        r"\b\d+-\d+\+\syears\sof\experience\b",
        r"\b\d+-\d+\syears\sof\sexperience\b",
    ]

    education_patterns = [
        r"m.sc",
        r"p.hd",
        r"phd",
        r"msc",
        r"doctoral",
        r"msc\sor\sphd",
        r"doctoral\sdegree",
        r"mba/msc",
        r"applicants\swith\sa\sdoctoral\sdegree",
    ]

    alarming_phrases = [
        r"(Previous|Prior|Past)\s*experience\s*(as\s+a\s*)?(professional\s*)?developer\s*(for\s*)?(roughly|approximately|about|around)?\s*\d+\s*years\s*(or\s+more)?",
        r"senior\sfull\sstack\sdeveloper" r"senior",
        r"senior\sfull\sstack\sdeveloper\s-\spotential\sfuture\slead",
        r"Solid\sworking\sas\sBackend\sDeveloper\swith\sNode",
    ]

    all_patterns = alarming_phrases + education_patterns + experience_patterns

    for pattern in all_patterns:
        if re.search(pattern, x["description"], re.IGNORECASE):
            return 1
    return 0


applier = PandasLFApplier([is_realistic_entry_level])
L_train = applier.apply(df)
print(L_train)
