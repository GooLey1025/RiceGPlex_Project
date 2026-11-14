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
| [**GATK-DELLY-VariantsCalling**](https://github.com/GooLey1025/GATK-DELLY-VariantsCalling) | Variant calling pipeline from BAM files. Generates SNPs, INDELs, and SVs from bam files using GATK and DELLY. |
| [**GATK-DELLY-Allele_based-Genotyping**](https://github.com/GooLey1025/GATK-DELLY-Allele_based-Genotyping) | Manuscript v1 workflow; can be ignored. Allele-based targeted genotyping for predefined marker panels. Now covered by [**Multi_Source_Marker_Panel_generation**](https://github.com/GooLey1025/Multi_Source_Marker_Panel_generation). |
| [**GWAS-LD_Markers-Discovery**](https://github.com/GooLey1025/GWAS-LD_Markers-Discovery) | Manuscript v1 workflow; can be ignored. Runs GWAS to obtain lead variants. Now covered by [**Multi_Source_Marker_Panel_generation**](https://github.com/GooLey1025/Multi_Source_Marker_Panel_generation). |
| [**Multi_Source_Marker_Panel_generation**](https://github.com/GooLey1025/Multi_Source_Marker_Panel_generation) | Current marker-panel workflow. Multi-source marker panel generation framework that integrates GWAS-LD markers, GWAS lead variants, public GWAS resources, and RiceNavi QTNs to generate RiceGPlex marker panels. |
| [**VarsGT**](https://github.com/GooLey1025/VarsGT) | End-to-end genotyping workflow that converts raw sequencing reads into RiceGPlex-compatible genotype matrices. Supports graph pangenome alignment, SNP/INDEL/SV genotyping, genotype imputation, and marker-panel extraction. |
| [**Aquila-GS**](https://github.com/GooLey1025/Aquila-GS) | Deep learning framework for genomic selection. Implements allele-aware encoding, adaptive convolutional compression, multi-head self-attention, multi-task prediction, Integrated Gradients interpretation, and QTN-guided directed evolution. |


## Contact

For questions regarding workflow implementation, code reproduction, or other technical details, please contact Lei Gu at `goley04@foxmail.com`.