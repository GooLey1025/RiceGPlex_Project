## Pangenome Construction

```sh
data_dir=/public/home/cszx_huangxh/qiujie/collabrators/gulei/rice_graph_pangenome/data/42accession

find $data_dir -type d -name "processed" -exec find {} -type f -name "*.fa" \; | while read -r file; do echo -e "$(basename $file)\t$file" ;done > files.list
awk '{gsub(/^processed_/,"",$1);gsub(/(\.genome\.fa|\.fa)$/, "",$1);gsub(/\./, "_", $1);gsub(/\-/,"_",$1); print $0}' files.list > pangenome.list
rm files.list
### follow the convention of SAMPLE.HALOTYPE 
ref=Nipponbare55
awk -v ref=$ref '{if ($0 ~ ref) {print} else {sub($1, $1".0"); print}}' pangenome.list > $ref.pangenome.list

source ~/.bashrc
conda activate py3.8

reference=$(grep "$ref" $ref.pangenome.list | cut -d " " -f 1) # "FaHC_P8_Nipponbare_TEJ" here.

# N is often defined as 10% of No. Haplotypes. 'It is indeed a shame to remove rarer variants before mapping, but is a necessity to get the best performance out of (the current version) of vg giraffe.'
# But for now, minigraph-cactus have better option to use 'haplotye' mode "--haplo". Details see: https://github.com/ComparativeGenomicsToolkit/cactus/blob/master/doc/pangenome.md#haplotype-sampling-instead-of-filtering-new

N=4
mkdir -p ./tmp
/usr/bin/time -v -o time.log cactus-pangenome ./js $ref.pangenome.list --outDir ./$ref.pangenome --outName $ref.pangenome --reference $reference --vcf --filter $N --haplo --giraffe clip full filter --gbz clip filter full --gfa clip full filter --xg --chrom-vg --odgi --chrom-og --viz --draw --logFile ./$ref.pangenome.log --workDir ./tmp
```

## Pangenome growth plot

```sh
#!/bin/bash
source ~/.bashrc

conda activate py3.8

dir=/public/home/cszx_huangxh/qiujie/collabrators/gulei/maize_graph_pangenome/graph_construction/MC/Nip_42_rice/Nip_42_rice.pangenome
gfa=Nip_42_rice.pangenome.gfa
ref_hap=Nip_Chr
ref=Nipponbare
output=$ref_hap.sorted.txt
graph_info=Graph_Pangenome_individual_info.csv


if [ ! -f $dir/$gfa ]; then
    if [ -f $dir/$gfa.gz ]; then
        echo "gunzip $gfa.gz ... "
        gunzip -c $dir/$gfa.gz > $dir/$gfa
    else
        echo "Error: $dir/$gfa.gz does not exist."
    fi
fi

# Exclude paths from reference genome.
grep '^W' $dir/$gfa | cut -f2 | grep -ie "$ref" | sort | uniq > $gfa.exclude.$ref_hap.txt
# grep '^W' $dir/$gfa | cut -f4 | grep -ie "$ref" | sort | uniq > $gfa.exclude.$ref_hap.txt
# for establish order
grep '^W' $dir/$gfa | cut -f2 | grep -ive "$ref" | sort | uniq > $gfa.paths.no_ref.haplotypes.txt


RUST_LOG=info panacus ordered-histgrowth -c bp -t 48 -l 1,1,2,1 -q 0.95,0.05,0,0 -S -e $gfa.exclude.$ref_hap.txt -O $output $dir/$gfa -o html > $gfa.ordered.html
RUST_LOG=info panacus ordered-histgrowth -c bp -t48 -l 1,1,2,1 -q 0.95,0.05,0,0 -S -e $gfa.exclude.$ref_hap.txt -O $output $dir/$gfa -o table > $gfa.ordered.tsv

```

## Plot with R

```sh
# data <- read.table("Nip_42_rice.gfa.ordered.tsv",header = TRUE)
data <- read.table("Nip_42_rice.gfa.ordered.tsv",header = TRUE)
map_data <- read.csv("filtered_Graph_Pangenome_individual_info.csv",header=FALSE)
head(data)
head(map_data)

data$Index <- 1:nrow(data)
merged_data <- merge(data, map_data, by.x = "panacus", by.y = "V1", all.x = TRUE)
merged_data <- merged_data[order(merged_data$Index), ]
merged_data$Index <- NULL
merged_data

library(ggplot2)
library(tidyr)
library(dplyr)
library(stringr)
library(RColorBrewer)
library(ggpattern)  # Support shadow patterns
library(ragg)
# 修正数据类型，将字符型列转换为数值型
filtered_data <- merged_data[-c(1, 2, 3), ]
filtered_data$ordered.growth <- as.numeric(filtered_data$ordered.growth)
filtered_data$ordered.growth.1 <- as.numeric(filtered_data$ordered.growth.1)
filtered_data$ordered.growth.2 <- as.numeric(filtered_data$ordered.growth.2)
filtered_data$ordered.growth.3 <- as.numeric(filtered_data$ordered.growth.3)


# 处理 V6 列：全部转为小写，然后将以 "o" 开头的首字母替换为大写 "O"
filtered_data <- filtered_data %>%
  mutate(V6 = str_to_lower(V6),  # 将所有内容转换为小写
         V6 = ifelse(startsWith(V6, "o"), paste0("O", substring(V6, 2)), V6))  # 替换首字母为大写 O

# 自定义类别顺序
desired_order <- c("O. rufipogon","aus", "indica", "intermediate", "temperate japonica", "tropical japonica", "basmati", "O. barthii","O. glaberrima","weedy rice")
filtered_data$V6 <- factor(filtered_data$V6, levels = desired_order)

# 确保横坐标按原始顺序排列
filtered_data$panacus <- factor(filtered_data$panacus, levels = unique(filtered_data$panacus))

# 将数值列换算为 MB
filtered_data <- filtered_data %>%
  mutate(across(starts_with("ordered.growth"), ~ . / 1e6))  # 换算为 MB

# 使用 RGB 定义自定义颜色
custom_colors <- c(
  "aus" = rgb(124,184,124, maxColorValue = 255),        # Red-Orange
  "indica" = rgb(107,124,179, maxColorValue = 255),     # Green
  "intermediate" = rgb(187,187,187, maxColorValue = 255),  # Blue
  "temperate japonica" = rgb(230,184,77, maxColorValue = 255),  # Yellow
  "tropical japonica" = rgb(199,91,91, maxColorValue = 255), # Light Green
  "basmati" = rgb(155,124,182, maxColorValue = 255),     # Dark Red
  "O. glaberrima" = rgb(185,141,24, maxColorValue = 255), # Purple
  "O. rufipogon" = rgb(24,124,124,maxColorValue = 255),
  "O. barthii"= rgb(152,52,52, maxColorValue = 255),
  "weedy rice"= rgb(100,100,52, maxColorValue = 255)
)

# 绘制柱状图
p <- ggplot(filtered_data, aes(x = panacus, y = ordered.growth.3, fill = V6)) +
  geom_bar(stat = "identity", position = "stack", alpha = 1,width = 1) +  # 基础柱状图
  scale_fill_manual(values = custom_colors) +  # 使用 RGB 自定义颜色
  labs(
    x = "Pangenome accessions",  # 横坐标标签
    y = "Length [Mb]",
    title = NULL
  ) +  # 移除图表标题
  theme_classic() +  # 使用 classic 主题
  theme(
    axis.text.x = element_blank(),  # 去掉横坐标刻度标签
    axis.ticks.x = element_blank(),  # 移除横轴刻度线
    axis.title.x = element_text(size = 12, hjust = 0.5),  # 横坐标标签居中对齐
    axis.text.y = element_text(size = 10),
    legend.text = element_text(face = "italic"),  # 图例文字斜体
    
    plot.title = element_blank()  # 移除标题
  ) +
  guides(fill = guide_legend(title = NULL)) +  # 去掉 V6 的图例标题
  scale_y_continuous(expand = c(0, 0))  # 纵坐标紧贴柱状图

# 叠加 ordered.growth.1 的阴影层
p <- p + geom_bar(data = filtered_data, aes(x = panacus, y = ordered.growth.1),
                  stat = "identity", fill = "white", alpha = 0.3, width=1,position = "identity")

# 叠加 ordered.growth 的阴影层
p <- p + geom_bar(data = filtered_data, aes(x = panacus, y = ordered.growth),
                  stat = "identity", fill = "black", alpha = 0.2, width=1,position = "identity")

# 设置画布大小
options(repr.plot.width = 4.2, repr.plot.height = 2.2)
# 显示图形
print(p)

ggsave(
  filename = "panacus_growth_stack.pdf",
  plot = p,
  device = cairo_pdf,
  width = 4.8,
  height = 2.2,
  units = "in"
)
```

