#!/usr/bin/env bash

# Set working directory
cd '/home/vincentwilde/Documents/thesis_1/Testymolo/testymolo/datamolo/scr/workinprogress/profile'

# Create necessary directories
mkdir -p "./F189-search/PROFILE"
mkdir -p "./F189-search/Orthocoronaviridae"
mkdir -p "./F189-search/OUT"

# Define relative paths
PROFILE_f_p="./aln/F189.aln.fasta"
PROFILE="./F189-search/PROFILE/PROFILE"
Orthocoronavirinae_f_p="./in/Orthocoronaviridae.fasta"
Orthocoronavirinae="./F189-search/Orthocoronaviridae/Orthocoronaviridae"
OUT_m8="./F189-search/alnResult.m8"
tmp="./F189-search/tmp"

# Create MMseqs2 databases
mmseqs createdb $PROFILE_f_p $PROFILE -v 0
mmseqs createdb $Orthocoronavirinae_f_p $Orthocoronavirinae -v 0

# Perform search
OUT_db="./F189-search/OUT/OUT_db"
mmseqs search $PROFILE $Orthocoronavirinae $OUT_db $tmp

# Extract sequences from search results (this step ensures we have sequence data, not alignments)
OUT_db_m8="./F189-search/OUT/OUT_db_m8"
mmseqs conversalis $PROFILE $Orthocoronaviridae $OUT_db $OUT_db_m8 --extract-seq

# Cluster the sequences
OUT_clu="./F189-search/OUT/OUT_clu"
mmseqs cluster $OUT_db_m8 $OUT_clu $tmp --min-seq-id 0.9 

# Export clustering results to TSV format
OUT_clu_tsv="./F189-search/OUT/OUT_clu_tsv"
mmseqs createtsv $OUT_db $OUT_clu $OUT_clu_tsv

# Optionally convert to .m8 format if needed
# If you need to align the sequences and then convert to .m8 format
mmseqs align $PROFILE $Orthocoronavirinae $OUT_db $tmp
mmseqs convertalis $PROFILE $Orthocoronavirinae $OUT_db $OUT_m8
