# Custom script about "HGT-Mediated intra-species functional complementarity faciltates intra-species fitness"
This repository contains the Python and R scripts used for the data analysis and figure generation.

## Python Scripts (.py):

ANOVA.py:  Performs Analysis of Variance (ANOVA) tests. This script is likely used for statistical comparisons of gene expression levels or fitness parameters across different groups (e.g., comparing gene expression in different co-culture conditions).

Gene_pool_average_length.py: Calculates the average length of genes within defined gene pools. This script is part of the pangenome analysis workflow, exploring the evolutionary trends in gene length within L. plantarum.

Gene_pool_counts.py:  Counts the number of genes present in defined gene pools.  Similar to Gene_pool_average_length.py, this script contributes to the pangenome analysis by quantifying gene presence and absence.

Gene_pool_proportion.py: Calculates the proportion of genes belonging to specific categories (e.g., COG categories) within gene pools. This script helps to analyze the functional composition of gene pools and how it changes with gene pool richness.

HGT_donors.py:  Identifies the likely donor organisms for horizontally transferred genes. This script is crucial for tracing the origins of HGT events and understanding the phylogenetic context of gene transfer in L. plantarum.

HGT_fishertest.py:  Performs Fisher's exact test related to Horizontal Gene Transfer (HGT). This script likely tests for statistical associations, such as whether certain gene categories are significantly enriched in horizontally transferred genes or associated with specific donor groups.

Logistic_Model.py:  Implements a logistic growth model. This script is used to fit growth curves obtained from mono- and co-culture experiments, allowing for the extraction of key growth parameters like maximum growth rate, carrying capacity, and inflection time.

Phenotypic_distance.py: Calculates phenotypic distances between L. plantarum strains. This script quantifies the dissimilarity in growth phenotypes based on the parameters derived from the logistic growth model.

Phylogenetic_distance.py: Calculates phylogenetic distances between L. plantarum strains. This script likely computes distances based on genomic sequences to quantify evolutionary relatedness.

Total_length_cutoff.py: Implements a cutoff based on total sequence length. This script is likely used for filtering genes or genomic regions based on their total length, potentially for quality control or specific analyses.

Total_sequence_length.py:  Calculates the total sequence length for various gene sets or genomic features. This script might be used to analyze the overall genomic contribution of different gene categories.

Transcriptomic_distance.py: Calculates transcriptomic distances between L. plantarum strains. This script uses Jensen-Shannon Divergence to quantify the dissimilarity in gene expression profiles obtained from RNA-seq data.

complementary_ratio_fisher.py: Calculates the complementary ratio of horizontally transferred genes and performs Fisher's exact test related to this ratio. This script is central to the analysis of functional complementarity and its association with fitness, especially for Q-category genes.

## R Scripts (.R):

Clustervis.R:  Performs cluster visualization. This script likely generates visualizations of gene expression clusters (e.g., from Mfuzz clustering) or phenotypic clusters, aiding in the interpretation of clustering results.

Mantel_test.R:  Performs Mantel tests. This script is used for correlation analyses between different distance matrices, such as comparing phylogenetic distance, phenotypic distance, and transcriptomic distance to assess their interrelationships.
