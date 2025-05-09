# Custom script about "Horizontal gene transfer-mediated intra-species functional complementarity enhances intra-species population fitness"
This repository contains the Python and R scripts used for the data analysis and figure generation.

## Python Scripts (.py):

ANOVA.py:  Performs Analysis of Variance (ANOVA) tests. This script is likely used for statistical comparisons of gene expression levels or fitness parameters across different groups.

Gene_pool_average_length.py: Calculates the average length of genes within gene pool. This script is part of the pangenome analysis workflow, exploring the evolutionary trends in gene length within L. plantarum.

Gene_pool_counts.py:  Counts the number of genes present in gene pool.  Similar to Gene_pool_average_length.py, this script contributes to the pangenome analysis by quantifying gene presence and absence.

Gene_pool_proportion.py: Calculates the proportion of genes belonging to specific categories (e.g., COG categories) within gene pools. This script helps to analyze the functional composition of gene pool and how it changes with gene pool richness.

HGT_donors.py: Downloads 16S rRNA sequences of potential donor organisms for horizontally transferred genes from the NCBI server. This script is essential for identifying HGT donors and analyzing the phylogenetic relationships of gene transfer events in L. plantarum.

HGT_fishertest.py:  Performs Fisher's exact test related to Horizontal Gene Transfer (HGT). This script likely tests for statistical associations, such as whether certain gene categories are significantly enriched in specific donor groups.

Logistic_Model.py:  Implements a logistic growth model. This script is used to fit growth curves obtained from mono- and co-culture experiments, allowing for the extraction of key growth parameters like maximum growth rate, carrying capacity, and inflection time.

Phenotypic_distance.py: Calculates phenotypic distances between L. plantarum strains. This script quantifies the dissimilarity in growth phenotypes based on the parameters derived from the logistic growth model.

Phylogenetic_distance.py: Calculates phylogenetic distances between L. plantarum strains. This script likely computes distances based on genomic sequences to quantify evolutionary relatedness.

Total_length_cutoff.py: Determines the optimal cutoff value for the total gene length within specific categories to assess its significant impact on organismal growth. This script systematically identifies the threshold where gene length differences lead to statistically significant variations in growth, using a t-test approach.

Total_sequence_length.py:  Calculates the total sequence length for various gene categories.

Transcriptomic_distance.py: Calculates transcriptomic distances between L. plantarum strains. This script uses Jensen-Shannon Divergence to quantify the dissimilarity in gene expression profiles obtained from RNA-seq data.

complementary_ratio_fisher.py: Calculates the complementary ratio of horizontally transferred genes and performs Fisher's exact test related to this ratio. This script is central to the analysis of functional complementarity and its association with fitness, especially for Q-category genes.

## R Scripts (.R):

Clustervis.R:  Performs cluster visualization. This script likely generates visualizations of gene expression clusters (e.g., from Mfuzz clustering) or phenotypic clusters, aiding in the interpretation of clustering results.

Mantel_test.R:  Performs Mantel tests. This script is used for correlation analyses between different distance matrices, such as genome distance to assess their interrelationships.
