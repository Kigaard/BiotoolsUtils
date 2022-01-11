import pandas as pd


def count_terms(df: pd.DataFrame):
    topic_yes_words: list = ["Proteomics", "Protein modifications",
                             "Protein interactions", "Protein structure analysis",
                             "Protein folds and structural domains", "Protein expression",
                             "Protein sites, features and motifs", "Protein properties", "Protein secondary structure"]
    topic_maybe_words: list = ["Proteins", "Proteomics experiment", "Sequence analysis",
                               "Molecular interactions, pathways and networks", "Sequencing",
                               "Sequence sites, features and motifs", "Structure analysis"]
    operation_yes_words: list = ["Protein sequence analysis", "Peptide identification", "Protein identification",
                                 "Protein quantification", "Peptide database search", "Protein feature detection",
                                 "Protein fragment weight comparison", "Target-Decoy", "Blind peptide database search",
                                 "Protein structure analysis", "de Novo sequencing"]
    operation_maybe_words: list = ["Spectral analysis", "Mass spectrum visualisation", "Peak detection",
                                   "Chromatogram visualisation", "Plotting", "Database search", "Deisotoping",
                                   "Labeled quantification", "Differential protein expression analysis",
                                   "Isotopic distributions calculation"]

    topic_yes_counts: list = []
    topic_maybe_counts: list = []
    operation_yes_counts: list = []
    operation_maybe_counts: list = []
    total_yes_counts: list = []
    total_maybe_counts: list = []
    for i, row in df.iterrows():
        topics: list = [term for term in row["Topics"].split("\n")]
        operations: list = [term for term in row["Operations"].split("\n")]

        topic_yes_count = len([term for term in topics if term in topic_yes_words])
        topic_maybe_count = len([term for term in topics if term in topic_maybe_words])
        operation_yes_count = len([term for term in operations if term in operation_yes_words])
        operation_maybe_count = len([term for term in operations if term in operation_maybe_words])

        topic_yes_counts.append(topic_yes_count)
        topic_maybe_counts.append(topic_maybe_count)
        operation_yes_counts.append(operation_yes_count)
        operation_maybe_counts.append(operation_maybe_count)
        total_yes_counts.append(topic_yes_count + operation_yes_count)
        total_maybe_counts.append(topic_maybe_count + operation_maybe_count)

    count_df = df.assign(TopicsYes=topic_yes_counts, TopicsMaybe=topic_maybe_counts,
                         OperationsYes=operation_yes_counts, OperationsMaybe=operation_maybe_counts,
                         TotalYes=total_yes_counts, TotalMaybe=total_maybe_counts)

    count_df = count_df.set_index("Unnamed: 0")
    count_df.to_excel("Biotools_proteomics_count.xlsx")


def main():
    file: pd.DataFrame = pd.read_excel("biotools_proteomics.xlsx")
    file = file.fillna('')
    count_terms(df=file)


if __name__ == "__main__":
    main()
