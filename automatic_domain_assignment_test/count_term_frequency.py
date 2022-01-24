import json
import re
from collections import Counter

import pandas as pd


def count_terms(df: pd.DataFrame, topic_index, operation_index):
    def show_terms(term_type: str, index: dict, regex_pattern):
        terms = [term for term in df[term_type].str.split("\n")]
        terms = [item for sublist in terms for item in sublist]
        terms = [re.search(regex_pattern, term).group(1) for term in terms
                 if re.search(regex_pattern, term) is not None]
        counter: Counter = Counter(terms)
        print("*" * 5, f"Top {top_n} {term_type}", "*" * 5)
        [print(f"{term_rank}. {index[term]['name'] if term in index else 'N/A'} ({term}) - {term_count}")
         for term_rank, (term, term_count) in enumerate(counter.most_common(top_n), start=1)]

    top_n: int = 30
    show_terms(term_type="Topics", index=topic_index, regex_pattern=r"\((topic_[0-9]{4})\)")
    show_terms(term_type="Operations", index=operation_index, regex_pattern=r"\((operation_[0-9]{4})\)")


def main():
    with open("Resources/topic_index.json", "r") as f:
        topic_index = json.load(f)["data"]
    with open("Resources/operation_index.json", "r") as f:
        operation_index = json.load(f)["data"]

    file: pd.DataFrame = pd.read_excel("TestFiles/biotools_proteomics.xlsx")
    file = file.fillna('')
    count_terms(df=file, topic_index=topic_index, operation_index=operation_index)


if __name__ == "__main__":
    main()
