import json
import re

import pandas as pd


def count_terms(df: pd.DataFrame):
    with open("Resources/term_categories.json", "r") as f:
        terms = json.load(f)
    topic_yes_terms: list = [term["uri"] for term in terms["TopicYes"]]
    topic_maybe_terms: list = [term["uri"] for term in terms["TopicMaybe"]]
    operation_yes_terms: list = [term["uri"] for term in terms["OperationYes"]]
    operation_maybe_terms: list = [term["uri"] for term in terms["OperationMaybe"]]

    topic_regex_pattern = r"\((topic_[0-9]{4})\)"
    operation_regex_pattern = r"\((operation_[0-9]{4})\)"

    topic_yes_counts: list = []
    topic_maybe_counts: list = []
    operation_yes_counts: list = []
    operation_maybe_counts: list = []
    total_yes_counts: list = []
    total_maybe_counts: list = []
    total_topic_counts: list = []
    total_operation_counts: list = []
    for i, row in df.iterrows():
        topics: list = [re.search(topic_regex_pattern, term).group(1) for term in row["Topics"].split("\n")
                        if re.search(topic_regex_pattern, term) is not None]
        operations: list = [re.search(operation_regex_pattern, term).group(1) for term in row["Operations"].split("\n")
                            if re.search(operation_regex_pattern, term) is not None]

        topic_yes_count = len([term for term in topics if term in topic_yes_terms])
        topic_maybe_count = len([term for term in topics if term in topic_maybe_terms])
        operation_yes_count = len([term for term in operations if term in operation_yes_terms])
        operation_maybe_count = len([term for term in operations if term in operation_maybe_terms])

        topic_yes_counts.append(topic_yes_count)
        topic_maybe_counts.append(topic_maybe_count)
        operation_yes_counts.append(operation_yes_count)
        operation_maybe_counts.append(operation_maybe_count)

        total_yes_counts.append(topic_yes_count + operation_yes_count)
        total_maybe_counts.append(topic_maybe_count + operation_maybe_count)

        total_topic_counts.append(topic_yes_count + topic_maybe_count)
        total_operation_counts.append(operation_yes_count + operation_maybe_count)

    count_df = df.assign(TopicsYes=topic_yes_counts, TopicsMaybe=topic_maybe_counts,
                         OperationsYes=operation_yes_counts, OperationsMaybe=operation_maybe_counts,
                         TotalYes=total_yes_counts, TotalMaybe=total_maybe_counts, TotalTopics=total_topic_counts,
                         TotalOperations=total_operation_counts)

    count_df = count_df.set_index("Unnamed: 0")
    count_df.index.name = ""
    count_df.to_excel("TestFiles/Biotools_proteomics_count_no_proteomics.xlsx")


def main():
    file: pd.DataFrame = pd.read_excel("TestFiles/biotools_proteomics.xlsx")
    file = file.fillna('')
    count_terms(df=file)


if __name__ == "__main__":
    main()
