import pandas as pd
from cleaner import clean_df

entry_level_keywords = [
    'team', 'role', 'skill', 'opportun', 'support', 'learn', 'intern',
    'train', 'candid', 'entry', 'junior', 'assist', 'beginner', 'qualif',
    'agil', 'collabor', 'task', 'grow', 'flexibl', 'requir', 'excel',
    'client', 'remot', 'respons', 'educ', 'custom', 'posit', 'commun',
    'compani', 'process', 'hour', 'report', 'includ', 'provid', 'full',
    'coordin', 'work', 'retail', 'staff', 'solut', 'build', 'creat',
    'organ', 'time', 'admin', 'market', 'softwar', 'part', 'busi', 'individu','user'
]
nonentry_level_keywords = [
    'senior', 'expert', 'manag', 'lead', 'architect', 'strategi', 'consult',
    'execut', 'develop', 'technolog', 'engineer', 'program', 'analyt',
    'product', 'project', 'sales', 'specialist', 'implement', 'innov',
    'design', 'optim', 'platform', 'infrastructur', 'integr', 'network',
    'direct', 'research', 'global', 'scal', 'oper', 'data', 'perform',
    'test', 'system', 'cloud', 'plan', 'ensur', 'regul', 'financi', 'maintain',
    'qualiti', 'resourc', 'technic', 'review', 'complianc', 'user', 'object',
    'improv', 'servic', 'relat'
]


def calculate_entry_levelness(text):
    score = 0
    for keyword in entry_level_keywords:
        score += text.count(keyword)
    for keyword in nonentry_level_keywords:
        score -= text.count(keyword)
    return score


def level_score(clean_data: pd.DataFrame) -> list:
    """Compute 'entry levelness' scores for each job post in raw_data"""
    clean_data['entry_level_score'] = clean_data['description'].apply(calculate_entry_levelness)
    return clean_data


if __name__ == "__main__":
    df = pd.read_csv("uniquejobs_clean.csv")
    df = clean_df(df)
    df = level_score(df)
    df.to_csv("uniquejobs_clean_entry_level.csv")