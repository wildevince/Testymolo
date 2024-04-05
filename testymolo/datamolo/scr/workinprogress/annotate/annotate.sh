#!/usr/bin/env bash


# if fasta DB not exist
## make DB
#cd "~/Documents/thesis_1/Testymolo/testymolo/datamolo/scr/workinprogress/annotate"
if [ ! -d ./fasta ]; then 
    mkdir fasta
fi
if [ ! -f FASTA ]; then 
    cd ../../profile/fasta
    mmseqs createdb $(ls) ../../annotate/fasta/FASTA -v 0
    cd ../../annotate/
fi


# if not argument
if [ $# -eq 0 ];
    then
        mmseqs easy-search ./in/reference.fasta ./fasta/FASTA ./out/out.aln tmp -v 0
else 
    mmseqs easy-search $1 ./fasta/FASTA ./out/out.aln tmp -v 0
fi


cd data/
(1)
mmseqs createtsv FASTA FASTA FASTA_clu FASTA_clu.tsv
mmseqs result2msa FASTA FASTA FASTA_clu FASTA_clu_msa

(2)
mmseqs createseqfiledb FASTA FASTA_clu FASTA_clu_seq
mmseqs apply FASTA_clu_seq FASTA_clu_seq_msa -- clustalo -i - --threads=1


(3) # search through DB
mmseqs search in/MERS data/FASTA resultDB tmp -s 7.5 --num-iterations 2
mmseqs convertalis in/MERS data/FASTA resultDB result.m8