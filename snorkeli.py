import re
import pandas as pd
from snorkel.labeling import PandasLFApplier, labeling_function
import cleaner


@labeling_function()
def is_realistic_entry_level(x):
    experience_patterns = [
        r"\b\d+-\d+\syears\sof\sproven\sexperience\b",
        r"\b\d+\+\syears\sof\sexperience",
        r"\b\d+\s?to\s?\d+\syears",
        r"\b(at\sleast|minimum|min\.?)\s\d+\s(years|yr)",
        r"\bproven\strack\srecord\sof\sat\sleast\s\d+\syears",
        r"\bsignificant\sexperience",
        r"\b\d+-\d+\+\syears\sof\\experience\b",
        r"\b\d+-\d+\syears\sof\sexperience\b",
        r"\b\d+-?\d*\+?\s*(years|yrs|y)?\s*(of\s*)?(proven\s*)?(professional\s*)?experience\b",
        r"At\s+least\s+\d+\s*-\s*\d+\s*years'?(\s+of\s+experience)?",
        r"\b\d+\s*-\s*\d+\s*yr(s?)\b",
        r"\b\d+\s*-\s*\d+\s*yr(s?)\s*exp\b",
        r"\b\d+\s*-\s*\d+\s*y\s*exp\b",
        r"experience\s*:\s*\d+\s*-\s*\d+\s*years\b",
        r"\b\d+\s+or\s+more\s+years\b",
        r"required\s+experience\s*:\s*\d+\s*-\s*\d+\s*years\b",
        r"\b\d+\s*-\s*\d+\s*months\b",
        r"\b\d+\s*-\s*\d+\s*weeks\b",
        r"equivalent\s+experience\b",
        r"preferred\s+experience\s*:\s*\d+\s*-\s*\d+\s*years\b",
        r"or\s+an\s+equivalent\s+combination\s+of\s+education\s+and\s+experience\b",
        r"proven\s+ability\s+in\b",
        r"(minimum\s+of\s+)?\d+\s+years\s+of\s+(related\s+)?(professional\s+)?experience\b",
    ]

    education_patterns = [
        r"m\.sc",
        r"p\.hd",
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
        r"senior\sfull\sstack\sdeveloper",
        r"senior",
        r"senior\sfull\sstack\sdeveloper\s-\spotential\sfuture\slead",
        r"Solid\sworking\sas\sBackend\sDeveloper\swith\sNode",
    ]

    all_patterns = alarming_phrases + education_patterns + experience_patterns

    for pattern in all_patterns:
        if re.search(pattern, x["description"], re.IGNORECASE):
            return 1
    return 0


def label_dataframe(df: pd.DataFrame):
    df = cleaner.lower_description(df)
    applier = PandasLFApplier([is_realistic_entry_level])
    df = df.drop_duplicates(subset="description", keep='first')
    L_train = applier.apply(df)
    df.loc[:,"label"] = L_train
    df.loc[:,'custom_label'] = df.apply(lambda row: 1 if row['level'] in ['entry-level','Entry Level', 'internship', 'Not Applicable'] else 0, axis=1)
    df.loc[:,'final_label'] = df.apply(lambda row: row['custom_label'] if row['custom_label'] == 1 else row['label'], axis=1)
    return df


if __name__ == "__main__":
    df = cleaner.read_csv_relevant_columns_inorder("jobs.csv")
    df['description'].fillna('default_value', inplace=True)
    df = cleaner.clean_html_tags_from_dataset(df)
    df = label_dataframe(df)
    df.to_csv("jobs.csv")
    