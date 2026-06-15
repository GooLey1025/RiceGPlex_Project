# RiceGPlex Project

**Pangenome-informed deep learning with functional priors for genomic prediction and breeding design in rice**

RiceGPlex is an integrated framework that bridges genomic prediction, model interpretability, and rational breeding design in rice. By combining graph pangenome variants, GWAS-derived markers, curated quantitative trait nucleotides (QTNs), and deep learning–based genomic selection, RiceGPlex extends conventional genomic selection from phenotype prediction to actionable breeding recommendations.  

---

## Overview

RiceGPlex was designed to address three major limitations in current genomic selection:

1. **Incomplete variant representation**  

   Conventional SNP-only marker systems miss INDELs and structural variants that may contribute to agronomic traits.

2. **Limited biological interpretability**  

   Many genomic prediction models achieve prediction accuracy but provide limited information about functional loci.

3. **Lack of actionable breeding design**  

   Traditional genomic selection predicts existing germplasm but rarely suggests how to improve a genotype.

To overcome these limitations, RiceGPlex integrates multiple complementary components spanning genomic variation discovery, genomic prediction, model interpretation, and breeding design.

| Component | Purpose |
|------------|------------|
| **Graph pangenome-based SNP, INDEL, and SV discovery** | Expands genomic variation beyond linear-reference SNPs and improves recovery of missing heritability |
| **LD-pruned genome-wide representative markers** | Captures genome-wide genetic background while reducing marker redundancy and computational burden |
| **GWAS-derived lead variants** | Enriches marker panels with trait-associated loci identified from diverse rice populations |
| **Curated RiceNavi quantitative trait nucleotides (QTNs)** | Introduces biologically validated functional variants and enhances model interpretability |
| **Aquila deep learning framework** | Learns complex nonlinear relationships among variants for multi-trait genomic prediction |
| **Integrated Gradients-based interpretation** | Identifies loci driving model predictions and links predictive signals to biological mechanisms |
| **QTN-guided in silico directed evolution** | Converts prediction results into actionable breeding recommendations through multi-trait genotype optimization |

---

## Repository Structure

```text

RiceGPlex_Project

├── GATK-DELLY-VariantsCalling

│   ├── Linear-reference variant calling

│   ├── Graph pangenome-based variant calling

│   ├── SNP/INDEL discovery

│   └── Structural variant discovery

│

├── GATK-DELLY-Allele_based-Genotyping

│   ├── SNP/INDEL allele-based genotyping

│   ├── SV allele-based genotyping

│   ├── Marker-panel genotyping

│   └── Population genotype matrix generation

│

├── GWAS-LD_Markers-Discovery

│   ├── GWAS analysis

│   ├── LD clumping

│   ├── Public GWAS marker integration

│   ├── RiceNavi QTN integration

│   └── RiceGPlex marker panel construction

│

├── LDAK-Heritability-Calculation

│   ├── LD-adjusted kinship construction

│   ├── Single-variant-class heritability estimation

│   ├── Multi-variant heritability estimation

│   └── Variant contribution comparison

│

├── README.md

└── .gitmodules

