# RiceGPlex Project

An integrated analysis framework for genomic variation and genomic selection in rice.

This repository contains the core pipelines used in this study, including variant discovery, genotyping, marker construction, and heritability analysis.

---

## Repository Structure

- **GATK-DELLY-VariantsCalling**  
  De novo variant discovery pipeline for SNPs, INDELs, and structural variants (SVs).

- **GATK-DELLY-Allele_based-Genotyping**  
  Site-based genotyping pipeline that generates VCF files from BAM files using predefined variant sites.

- **GWAS-LD_Markers-Discovery**  
  Marker construction based on GWAS and LD pruning.

- **LDAK-Heritability-Calculation**  
  Heritability estimation using LDAK.

---

## Related Resources

- Aquila: https://github.com/GooLey1025/Aquila-GS  
- VarsGT: https://github.com/GooLey1025/VarsGT  

---
