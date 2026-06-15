# RiceGPlex Project

***Pangenome-informed deep learning with functional priors for genomic prediction and breeding design in rice.***

*RiceGPlex* is an integrated framework that bridges genomic prediction, model interpretability, and rational breeding design in rice. By combining graph pangenome variants, GWAS-derived markers, curated quantitative trait nucleotides (QTNs), and deep learning–based genomic selection, RiceGPlex extends conventional genomic selection from phenotype prediction to actionable breeding recommendations.  

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

## Repository Modules

**RiceGPlex** is organized as a collection of interoperable repositories, each responsible for a specific stage of the genomic prediction and breeding design workflow.

| Repository | Description |
|------------|------------|
| **GATK-DELLY-VariantsCalling** | Variant calling pipeline from BAM files. Generates SNPs, INDELs, and SVs from bam files using GATK and DELLY. |
| **VarsGT** | End-to-end genotyping workflow that converts raw sequencing reads into RiceGPlex-compatible genotype matrices. Supports graph pangenome alignment, SNP/INDEL/SV genotyping, genotype imputation, and marker-panel extraction. |
| **GATK-DELLY-Allele_based-Genotyping** | Allele-based targeted genotyping workflow for predefined marker panels. This is a sub-module of **VarsGT**|
| **GWAS-LD_Markers-Discovery** | Marker construction framework that integrates LD-pruned representative markers, GWAS lead variants, public GWAS resources, and RiceNavi QTNs to generate RiceGPlex marker panels. |
| **LDAK-Heritability-Calculation** | Heritability estimation workflows based on LD-adjusted kinship models. Supports SNP-, INDEL-, SV-, and multi-variant heritability analyses. |
| **Aquila-GS** | Deep learning framework for genomic selection. Implements allele-aware encoding, adaptive convolutional compression, multi-head self-attention, multi-task prediction, Integrated Gradients interpretation, and QTN-guided directed evolution. |


## Contact

For questions regarding workflow implementation, code reproduction, or other technical details, please contact Lei Gu at `goley04@foxmail.com`.