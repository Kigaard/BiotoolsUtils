import itertools
import re
import warnings

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder

warnings.simplefilter(action='ignore', category=FutureWarning)


def process_df(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    def encode_terms(row_inf: tuple, term_encoder: OneHotEncoder, term_type: str, regex: str, columns: pd.Index) \
            -> pd.Series:
        terms = [re.search(regex, term).group(1) for term in str(row_inf[1][term_type]).split('\n')
                 if re.search(regex, term) is not None]
        if len(terms) < 1:
            return pd.Series([row_inf[0]] + list(np.zeros(len(columns) - 1)), index=columns)

        encoded_terms = term_encoder.transform(np.array(terms).reshape(-1, 1))
        return pd.Series([row_inf[0]] + list(itertools.chain(sum(encoded_terms.toarray()).tolist())), index=columns)

    TOPIC_REGEX_PATTERN = r"\((topic_[0-9]{4})\)"
    OPERATION_REGEX_PATTERN = r"\((operation_[0-9]{4})\)"
    topic_terms, topic_encoder = _create_one_hot_encoder(raw_df, "Topics", TOPIC_REGEX_PATTERN)
    topics_df: pd.DataFrame = pd.DataFrame(columns=["ID"] + list(topic_terms))
    operation_terms, operation_encoder = _create_one_hot_encoder(raw_df, "Operations", OPERATION_REGEX_PATTERN)
    operations_df: pd.DataFrame = pd.DataFrame(columns=["ID"] + list(operation_terms))

    for no, row_info in enumerate(raw_df.iterrows()):
        print(f"{no} - {row_info[0]}")
        topics_df = topics_df.append(
            encode_terms(row_inf=row_info, term_encoder=topic_encoder, term_type="Topics",
                         regex=TOPIC_REGEX_PATTERN, columns=topics_df.columns), ignore_index=True)

        operations_df = operations_df.append(
            encode_terms(row_inf=row_info, term_encoder=operation_encoder, term_type="Operations",
                         regex=OPERATION_REGEX_PATTERN, columns=operations_df.columns), ignore_index=True)

    topics_df = topics_df.set_index("ID")
    topics_df.to_excel("TestFiles/Topics_1HE.xlsx")
    operations_df = operations_df.set_index("ID")
    operations_df.to_excel("TestFiles/Operations_1HE.xlsx")
    return topics_df, operations_df


def _create_one_hot_encoder(df: pd.DataFrame, df_column: str, regex: str):
    """
    Create the OneHotEncoder.

    :param df: The dataframe.
    :param df_column: The column with the terms.
    :param regex: The regex to extract the term ID.
    :return: The OneHotEncoder.
    """
    terms = [term for term in df[df_column].str.split("\n")]
    terms = [item for sublist in terms for item in sublist]
    terms = [re.search(regex, term).group(1) for term in terms if re.search(regex, term) is not None]
    sorted_terms = np.unique(sorted(terms))
    encoder = OneHotEncoder()
    encoder.fit(sorted_terms.reshape(-1, 1))
    return sorted_terms, encoder


def cluster(term_df: pd.DataFrame, term_type: str):
    import scipy.cluster.hierarchy as shc
    plt.figure(figsize=(10, 7))
    plt.title(f"Dendrograms of tools based on EDAM {term_type}")
    linkage_matrix = shc.linkage(term_df.iloc[:, 1:], method='ward')
    dend = shc.dendrogram(linkage_matrix, labels=list(term_df["ID"]))
    plt.show()

def main():
    # raw_df: pd.DataFrame = pd.read_excel("TestFiles/biotools_proteomics.xlsx")
    # raw_df = raw_df.fillna('')
    # raw_df.index = pd.Series([re.search(r"\(https:\/\/bio.tools\/(.+)\)", tool).group(1) for tool in raw_df["ID"]])
    #
    # topics_df, operation_df = process_df(raw_df)
    #

    topics_df: pd.DataFrame = pd.read_excel(io="TestFiles/Operations_1HE.xlsx", index_col=1)
    cluster(term_df=topics_df, term_type="Topics")
    operation_df: pd.DataFrame = pd.read_excel(io="TestFiles/Topics_1HE.xlsx")
    cluster(term_df=operation_df, term_type="Operations")


if __name__ == "__main__":
    main()
