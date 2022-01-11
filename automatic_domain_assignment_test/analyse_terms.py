from collections import Counter

import pandas as pd


def count_terms(df: pd.DataFrame):
    def show_terms(term_type: str):
        terms = [term for term in df[term_type].str.split("\n")]
        terms = [item for sublist in terms for item in sublist]
        counter: Counter = Counter(terms)
        print("*" * 5, f"Top {top_n} {term_type}", "*" * 5)
        [print(f"{term_rank}. {term} - {term_count}") for term_rank, (term, term_count) in
         enumerate(counter.most_common(top_n), start=1)]

    top_n: int = 30
    show_terms(term_type="Topics")
    show_terms(term_type="Operations")


def main():
    file: pd.DataFrame = pd.read_excel("biotools_proteomics.xlsx")
    file = file.fillna('')
    count_terms(df=file)


if __name__ == "__main__":
    main()
