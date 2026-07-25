#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

// 软件或文件地址请尽量指定绝对路径。如果要使用相对路径，需要添加file()，如：file("./scripts/remove_me.py")

params.reference       = "/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/nip.fa"
params.panel_vcf       = "/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/Nip_42_rice.filtered_ids.vcf.gz"
params.biallelic_vcf   = "/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/Nip_42_rice.filtered_ids_biallelic.vcf.gz"
params.reads_dir       = "/home/gulei/cohort/705rice_fq"
params.output_prefix   = "rice.pangenie"

params.pangenie_index  = "PanGenie-index"
params.pangenie        = "PanGenie"
params.python          = "python3"
params.convert_script  = "/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/pangenie/pipelines/run-from-callset/scripts/convert-to-biallelic.py"
params.bgzip           = "bgzip"
params.bcftools        = "bcftools"

Channel.fromPath(params.reference).set { reference_ch }
Channel.fromPath(params.panel_vcf).set { panel_vcf_ch }
Channel.fromPath(params.biallelic_vcf).set { biallelic_vcf_ch }
Channel.fromPath(params.convert_script).set { convert_script_ch }
Channel
    .fromFilePairs("${params.reads_dir}/*_{1,2}.fastq.gz", flat: true, checkIfExists: true)
    .set { read_pairs_ch }

process PANGENIE_INDEX {
    tag "pangenie_index"
    cpus 64
    memory "50 GB"

    input:
    path reference
    path panel_vcf

    output:
    path "pangenie_index"

    script:
    """
    mkdir -p pangenie_index
    ${params.pangenie_index} \
        -v ${panel_vcf} \
        -r ${reference} \
        -t ${task.cpus} \
        -o pangenie_index/index
    """
}

process PANGENIE_GENOTYPE {
    tag "${sample_id}"
    cpus 32
    memory "35 GB"
    maxForks 8 

    input:
    tuple val(sample_id), path(r1), path(r2), path(index_dir)

    output:
    tuple val(sample_id), path("${sample_id}_genotyping.vcf")

    script:
    """
    ${params.pangenie} \
        -f ${index_dir}/index \
        -i <(zcat ${r1} ${r2}) \
        -o ${sample_id} \
        -s ${sample_id} \
        -t ${task.cpus} \
        > ${sample_id}.pangenie.log 2>&1
    """
}

process CONVERT_BIALLELIC {
    tag "${sample_id}"
    cpus 2
    memory "20 GB"
    maxForks 8

    input:
    tuple val(sample_id), path(genotyping_vcf), path(biallelic_vcf), path(convert_script)

    output:
    tuple val(sample_id), path("${sample_id}.pangenie.biallelic.vcf")

    script:
    """
    ${params.python} ${convert_script} ${biallelic_vcf} \
        < ${genotyping_vcf} \
        > ${sample_id}.pangenie.biallelic.vcf
    """
}

process COMPRESS_VCF {
    tag "${sample_id}"
    cpus 4
    memory "4 GB"
    maxForks 8

    input:
    tuple val(sample_id), path(vcf)

    output:
    tuple val(sample_id), path("${sample_id}.pangenie.biallelic.vcf.gz"), path("${sample_id}.pangenie.biallelic.vcf.gz.tbi")

    script:
    """
    ${params.bgzip} -@ ${task.cpus} -c ${vcf} > ${sample_id}.pangenie.biallelic.vcf.gz
    ${params.bcftools} index -f --threads ${task.cpus} ${sample_id}.pangenie.biallelic.vcf.gz
    """
}

process MERGE_VCF {
    tag "merge_samples"
    cpus 64
    memory "64 GB"

    input:
    path vcfs

    output:
    path "${params.output_prefix}.vcf.gz"
    path "${params.output_prefix}.vcf.gz.tbi"

    script:
    """
    ${params.bcftools} merge \
        --threads ${task.cpus} \
        -m all \
        -Oz \
        -o ${params.output_prefix}.vcf.gz \
        ${vcfs}
    ${params.bcftools} index -f --threads ${task.cpus} ${params.output_prefix}.vcf.gz
    """
}

workflow {
    index_ch = PANGENIE_INDEX(reference_ch, panel_vcf_ch)
    genotype_input_ch = read_pairs_ch.combine(index_ch)
    genotyped_ch = PANGENIE_GENOTYPE(genotype_input_ch)

    convert_input_ch = genotyped_ch
        .combine(biallelic_vcf_ch)
        .combine(convert_script_ch)
    biallelic_ch = CONVERT_BIALLELIC(convert_input_ch)
    compressed_ch = COMPRESS_VCF(biallelic_ch)

    compressed_ch
        .map { sample_id, vcf, index -> vcf }
        .collect()
        .set { all_vcfs_ch }

    MERGE_VCF(all_vcfs_ch)
}
