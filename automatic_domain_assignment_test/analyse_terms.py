import pandas as pd
from collections import Counter
from apyori import apriori


def _analyse_terms(term_type: str, term_list: list[list[str]]):
    """
    Analyse the terms.

    :param term_type: The term types.
    :param term_list: The term list
    """
    print('*' * 5, term_type, '*' * 5)
    _find_common_elements(term_list=term_list, top_n=15)
    print()
    _calculate_apriori_relations(term_list=term_list)


def _find_common_elements(term_list: list[list[str]], top_n: int = 10):
    """
    Find the most common elements.

    :param term_list: The list of terms.
    :param top_n: Get top n most common elements. Default 10.
    """
    counter: Counter = Counter()
    for tool_topics in term_list:
        counter.update(tool_topics)
    print('-' * 3, f"Top {top_n} most frequent terms", '-' * 3)
    [print(f"{rank}.\t{term} - {count} ({round(count / len(term_list) * 100, 2)} %)")
     for rank, (term, count) in enumerate(counter.most_common(top_n), start=1)]


def _calculate_apriori_relations(term_list: list[list[str]]):
    """
    Calculate apriori relations.

    :param term_list: The list of tool terms.
    :return:
    """
    print('-' * 3, f"Apriori relations", '-' * 3)

    relations = apriori(transactions=term_list, min_lift=1.01)

    if len(list(relations)) > 0:
        for relation in relations.ordered_statistics:
            antecedent: str = " + ".join(list(relation.items_base)) if len(relation.items_base) > 0 else '()'
            consequent: str = " + ".join(list(relation.items_add)) if len(relation.items_add) > 0 else '()'
            print(f"{antecedent} -> {consequent} ({round(relation.confidence*100,2)} % confidence - "
                  f"{round(relations.support*100,2)} % support - {round(relation.lift,2)})")
    else:
        print("No relations found")


def main():
    tool_list: pd.DataFrame = pd.read_excel("tool_list.xlsx")
    topics: list[list[str]] = list(tool_list["Topics"].str.split("\n"))
    operations: list[list[str]] = list(tool_list["Operations"].str.split("\n"))

    _analyse_terms(term_type="Topics", term_list=topics)
    # _analyse_terms(term_type="Operations", term_list=operations)


if __name__ == "__main__":
    main()
