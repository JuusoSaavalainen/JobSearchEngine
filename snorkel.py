import pandas as pd
from snorkel.labeling import PandasLFApplier

df = pd.read_csv("uniquejobs_clean.csv")


@labeling_function()
def is_realistic_entry_level(x):
    if "PhD" in x["description"] or "Master" in x["description"]:
        return UNREALISTIC
    if "2+ years" in x["description"]:
        return UNREALISTIC
    if "3+ years" in x["description"]:
        return UNREALISTIC
    if "4+ years" in x["description"]:
        return UNREALISTIC
    return REALISTIC


applier = PandasLFApplier([is_realistic_entry_level])
L_train = applier.apply(df)