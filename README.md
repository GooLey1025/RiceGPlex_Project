# RiceGPlex Project

***Pangenome-informed deep learning with functional priors for genomic prediction and breeding design in rice.***

*RiceGPlex* is an integrated framework that bridges genomic prediction, model interpretability, and rational breeding design in rice. By combining graph pangenome variants, GWAS-derived markers, curated quantitative trait nucleotides (QTNs), and deep learning–based genomic selection, RiceGPlex extends conventional genomic selection from phenotype prediction to actionable breeding recommendations.

---


## RiceGPlex Web
🌐 Website: https://www.xhhuanglab.cn/tool/ricegplex

## Repository Modules

**RiceGPlex** is organized as a collection of interoperable repositories, each responsible for a specific stage of the genomic prediction and breeding design workflow.

| Repository | Description |
|------------|------------|
| **GATK-DELLY-VariantsCalling** | Variant calling pipeline from BAM files. Generates SNPs, INDELs, and SVs from bam files using GATK and DELLY. |
| **VarsGT** | End-to-end genotyping workflow that converts raw sequencing reads into RiceGPlex-compatible genotype matrices. Supports graph pangenome alignment, SNP/INDEL/SV genotyping, genotype imputation, and marker-panel extraction. |
| **GATK-DELLY-Allele_based-Genotyping** | Allele-based targeted genotyping workflow for predefined marker panels. This is a sub-function of **VarsGT**|
| **GWAS-LD_Markers-Discovery** | Marker construction framework that integrates LD-pruned representative markers, GWAS lead variants, public GWAS resources, and RiceNavi QTNs to generate RiceGPlex marker panels. |
| **LDAK-Heritability-Calculation** | Heritability estimation workflows based on LD-adjusted kinship models. Supports SNP-, INDEL-, SV-, and multi-variant heritability analyses. |
| **Aquila-GS** | Deep learning framework for genomic selection. Implements allele-aware encoding, adaptive convolutional compression, multi-head self-attention, multi-task prediction, Integrated Gradients interpretation, and QTN-guided directed evolution. |

## Reproduction Navigator

| Figure | Directory/Describtion | Data/Code |
|--------|-----------------------|-------------|
| **Fig. 1** | We use Adobe illustrator to sculpture this. | - |
| **Fig. 2A** | - | - |
| **Fig. 2B** | Aquila-GS/graph_variants_distribution/ | - |
| **Fig. 2C** | Pangenome-Construction/ | - |
| **Fig. 2D** | GWAS-LD_Markers-Discovery | cohort_pca_plot.py |
| **Fig. 2E** | LDAK-Heritability-Calculation/ & Reproduction_Navigator/Fig2E/ | Her.tsv & plot_her.py |
| **Fig. 2F** | GWAS-LD_Markers-Discovery | all_lead_markers_final.annotated.noredu.tsv & linear_hex_karyotype.py |
| **Fig. 3A** | We use Adobe illustrator to sculpture this and source code is available at Aquila-GS/ | - |
| **Fig. 3B** | We use Adobe illustrator to sculpture this and source code is available at Aquila-GS/src/layers.py | Line: `class MultiHeadPooling(nn.Module)`|
| **Fig. 3C-D** | Aquila-GS/model_ablation | - |
| **Fig. 3E-H** | Aquila-GS/benchmark | - |
| **Fig. 4A** | We use Adobe illustrator to sculpture this.| - |
| **Fig. 4B-G & Fig. 7E** | Aquila-GS/case/interpretability/ | - |
| **Fig. 5A** | We use Adobe illustrator to sculpture this.| - |
| **Fig. 5B-C** | Aquila-GS/evolve/ | `Case1: Teqing-to-HHZ` |
| **Fig. 6** | We use Adobe illustrator to sculpture this.| - |
| **Fig. 7A** | Aquila-GS/breeding_application/| plot_inbred_line_growth_subpop.py |
| **Fig. 7B** | Aquila-GS/case/rrBLUP_compare/ | - |
| **Fig. 7C** | Aquila-GS/breeding_application/| Inbred_120_heatmap.py |
| **Fig. 7D** | Reproduction_Navigator/Fig7D/| - |
| **Fig. 7F & Supp. Fig. 8** | Aquila-GS/evolve/| `Case2: HHZ-base` |
| **Fig. 7G** | Aquila-GS/evolve/site_pheno_pca_plot/| snp_violin_panel.py |
| **Supp. Fig. 1** | We use Adobe illustrator to sculpture this. | Marker construction method is available at [Reproduce of Rice GraphPangenome GS](https://github.com/GooLey1025/GWAS-LD_Markers-Discovery#reproduce-of-rice-graphpangenome-gs) |
| **Supp. Fig. 2** | GWAS-LDheritability_summary.tsvPangenome-Construction/plot_her.py | LDAK-Heritability-Calculation & plot_params_GYP.py |
| **Supp. Fig. 3** | Reproduction_Navigator/SuppFig3 | - |
| **Supp. Fig. 4** | Aquila-GS/model_ablation/marker_ablation | - |
| **Supp. Fig. 5** | Aquila-GS/case/ | plot_pred_vs_true_facets.py |
| **Supp. Fig. 6** | We use Adobe illustrator to sculpture this. | - |
| **Supp. Fig. 7** | Aquila-GS/case/ | plot_importance_loci_linked.py |


## Contact

For questions regarding workflow implementation, code reproduction, or other technical details, please contact Lei Gu at `goley04@foxmail.com`.