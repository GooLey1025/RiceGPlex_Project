## Prepare environment
### create a conda environment for pangenie
conda create -n pangenie -c conda-forge bioconda::pangenie
conda activate pangenie

### prepare scripts from PanGenie
git clone https://github.com/eblerjana/pangenie.git

## VCF filtering and annotation for Pangenie-input
VCF_GZ=${VCF_GZ:-/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/Nip_42_rice.vcf.gz}
GFA_GZ=${GFA_GZ:-/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/Nip_42_rice.gfa.gz}
OUTPUT_VCF=${OUTPUT_VCF:-/data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/Nip_42_rice.filtered.vcf.gz}
ANNOTATION_PREFIX=${ANNOTATION_PREFIX:-Nip_42_rice.filtered_ids}
EXCLUDE_SAMPLES=${EXCLUDE_SAMPLES:-}
MAX_MISSING=${MAX_MISSING:-0.2}

tmp_vcf=$(mktemp --suffix=.bcf)
tmp_dir=$(mktemp -d)
trap 'rm -f "$tmp_vcf"; rm -rf "$tmp_dir"' EXIT

# Optionally remove comma-separated samples.
if [[ -n "$EXCLUDE_SAMPLES" ]]; then
    bcftools view --samples "^${EXCLUDE_SAMPLES}" --force-samples -Ou "$VCF_GZ" > "$tmp_vcf"
else
    bcftools view -Ou "$VCF_GZ" > "$tmp_vcf"
fi

# Filter variants and trim unused ALT alleles.
{ bcftools +fill-tags "$tmp_vcf" -Ou -- -t AC,AN,AF,F_MISSING \
    | bcftools view -i "INFO/AC>0 && INFO/F_MISSING<=${MAX_MISSING} && REF~\"^[ACGTacgt]*$\" && ALT~\"^[ACGTacgt]*$\"" -Ou \
    | bcftools view --trim-alt-alleles -Oz -o "$OUTPUT_VCF"
} 2>filter.log
bcftools index --tbi --force "$OUTPUT_VCF"

# Convert haploid and unphased GT values to phased diploid genotypes.
bcftools view -Ov -o "$tmp_dir/filtered.vcf" "$OUTPUT_VCF"
phase_genotypes='function phase_gt(sample, format,    fmt, values, n_fmt, n_values, gt_index, i, gt) {
    n_fmt = split(format, fmt, ":")
    n_values = split(sample, values, ":")
    gt_index = 0
    for (i = 1; i <= n_fmt; i++) {
        if (fmt[i] == "GT") {
            gt_index = i
            break
        }
    }
    if (gt_index == 0 || gt_index > n_values) return sample
    gt = values[gt_index]
    if (gt == ".") values[gt_index] = ".|."
    else if (gt ~ /^[0-9]+$/) values[gt_index] = gt "|" gt
    else if (gt ~ /\./) values[gt_index] = ".|."
    else gsub(/\//, "|", values[gt_index])
    sample = values[1]
    for (i = 2; i <= n_values; i++) sample = sample ":" values[i]
    return sample
}
BEGIN {OFS = "\t"}
$1 ~ /^#/ {print; next}
{
    for (i = 10; i <= NF; i++) $i = phase_gt($i, $9)
    print
}'

awk "$phase_genotypes" "$tmp_dir/filtered.vcf" > "$tmp_dir/filtered_phased.vcf"

# Add graph IDs and create multiallelic and biallelic VCFs.
python3 pangenie/pipelines/prepare-vcf-from-MC/workflow/scripts/annotate_vcf.py \
    -vcf "$tmp_dir/filtered_phased.vcf" \
    -gfa "$GFA_GZ" \
    -o "$tmp_dir/annotated" \
    >annotate.log 2>&1

awk '$1 ~ /^#/ {print; next} {print | "sort -k1,1 -k2,2n"}' \
    "$tmp_dir/annotated.vcf" \
    | bgzip -c -f > "${ANNOTATION_PREFIX}.vcf.gz"
awk '$1 ~ /^#/ {print; next} {print | "sort -k1,1 -k2,2n"}' \
    "$tmp_dir/annotated_biallelic.vcf" \
    | bgzip -c -f > "${ANNOTATION_PREFIX}_biallelic.vcf.gz"

tabix -f -p vcf "${ANNOTATION_PREFIX}.vcf.gz"
tabix -f -p vcf "${ANNOTATION_PREFIX}_biallelic.vcf.gz"

bgzip -d -f ${ANNOTATION_PREFIX}.vcf.gz -k
bgzip -d -f ${ANNOTATION_PREFIX}_biallelic.vcf.gz -k

## Run PanGenie-Genotyping
conda activate pangenie
nextflow run pangenie.nf \
  --reads_dir /data4/gulei/cohort/705rice_fq \
  --reference /data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/nip.fa \
  --panel_vcf /data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/${ANNOTATION_PREFIX}.vcf \
  --biallelic_vcf /data4/gulei/projects/RiceGPlex_Project/PanGenie-Genotyping/${ANNOTATION_PREFIX}_biallelic.vcf \
  --output_prefix 705rice.pangenie -resume
