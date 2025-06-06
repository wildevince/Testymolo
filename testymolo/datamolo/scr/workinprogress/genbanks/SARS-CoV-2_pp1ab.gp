LOCUS       YP_009724389            7096 aa            linear   VRL 18-JUL-2020
DEFINITION  ORF1ab polyprotein [Severe acute respiratory syndrome coronavirus
            2].
ACCESSION   YP_009724389
VERSION     YP_009724389.1
DBLINK      BioProject: PRJNA485481
DBSOURCE    REFSEQ: accession NC_045512.2
KEYWORDS    RefSeq.
SOURCE      Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2)
  ORGANISM  Severe acute respiratory syndrome coronavirus 2
            Viruses; Riboviria; Orthornavirae; Pisuviricota; Pisoniviricetes;
            Nidovirales; Cornidovirineae; Coronaviridae; Orthocoronavirinae;
            Betacoronavirus; Sarbecovirus; Severe acute respiratory
            syndrome-related coronavirus.
REFERENCE   1  (residues 1 to 7096)
  AUTHORS   Wu,F., Zhao,S., Yu,B., Chen,Y.M., Wang,W., Song,Z.G., Hu,Y.,
            Tao,Z.W., Tian,J.H., Pei,Y.Y., Yuan,M.L., Zhang,Y.L., Dai,F.H.,
            Liu,Y., Wang,Q.M., Zheng,J.J., Xu,L., Holmes,E.C. and Zhang,Y.Z.
  TITLE     A new coronavirus associated with human respiratory disease in
            China
  JOURNAL   Nature 579 (7798), 265-269 (2020)
   PUBMED   32015508
  REMARK    Erratum:[Nature. 2020 Apr;580(7803):E7. PMID: 32296181]
REFERENCE   2  (residues 1 to 7096)
  CONSRTM   NCBI Genome Project
  TITLE     Direct Submission
  JOURNAL   Submitted (17-JAN-2020) National Center for Biotechnology
            Information, NIH, Bethesda, MD 20894, USA
REFERENCE   3  (residues 1 to 7096)
  AUTHORS   Wu,F., Zhao,S., Yu,B., Chen,Y.-M., Wang,W., Hu,Y., Song,Z.-G.,
            Tao,Z.-W., Tian,J.-H., Pei,Y.-Y., Yuan,M.L., Zhang,Y.-L.,
            Dai,F.-H., Liu,Y., Wang,Q.-M., Zheng,J.-J., Xu,L., Holmes,E.C. and
            Zhang,Y.-Z.
  TITLE     Direct Submission
  JOURNAL   Submitted (05-JAN-2020) Shanghai Public Health Clinical Center &
            School of Public Health, Fudan University, Shanghai, China
COMMENT     PROVISIONAL REFSEQ: This record has not yet been subject to final
            NCBI review. The reference sequence is identical to QHD43415.
            Annotation was added using homology to SARSr-CoV NC_004718.3. ###
            Formerly called 'Wuhan seafood market pneumonia virus.' If you have
            questions or suggestions, please email us at info@ncbi.nlm.nih.gov
            and include the accession number NC_045512.### Protein structures
            can be found at
            https://www.ncbi.nlm.nih.gov/structure/?term=sars-cov-2.### Find
            all other Severe acute respiratory syndrome coronavirus 2
            (SARS-CoV-2) sequences at
            https://www.ncbi.nlm.nih.gov/genbank/sars-cov-2-seqs/
            
            ##Assembly-Data-START##
            Assembly Method       :: Megahit v. V1.1.3
            Sequencing Technology :: Illumina
            ##Assembly-Data-END##
            COMPLETENESS: full length.
            Method: conceptual translation.
FEATURES             Location/Qualifiers
     source          1..7096
                     /organism="Severe acute respiratory syndrome coronavirus
                     2"
                     /isolate="Wuhan-Hu-1"
                     /host="Homo sapiens"
                     /db_xref="taxon:2697049"
                     /country="China"
                     /collection_date="Dec-2019"
     Protein         1..7096
                     /product="ORF1ab polyprotein"
                     /calculated_mol_wt=793931
     mat_peptide     1..180
                     /product="leader protein"
                     /note="nsp1; produced by both pp1a and pp1ab"
                     /protein_id="YP_009725297.1"
                     /calculated_mol_wt=19775
     Region          13..127
                     /region_name="SARS-CoV-like_Nsp1_N"
                     /note="N-terminal domain of non-structural protein 1 from
                     Severe acute respiratory syndrome-related coronavirus and
                     betacoronavirus in the B lineage; cd21796"
                     /db_xref="CDD:439285"
     Region          128..180
                     /region_name="SARS-CoV-like_Nsp1_C"
                     /note="C-terminal domain of non-structural protein 1 from
                     Severe acute respiratory syndrome-related coronavirus and
                     betacoronavirus in the B lineage; cd22662"
                     /db_xref="CDD:439355"
     Site            order(148..152,154..161,173..175,177..178,180)
                     /site_type="other"
                     /note="oligomer interface [polypeptide binding]"
                     /db_xref="CDD:439355"
     Site            order(160,164..165,167..168,171..172,175)
                     /site_type="other"
                     /note="RNA binding site [nucleotide binding]"
                     /db_xref="CDD:439355"
     mat_peptide     181..818
                     /product="nsp2"
                     /note="produced by both pp1a and pp1ab"
                     /protein_id="YP_009725298.1"
                     /calculated_mol_wt=70512
     Region          182..818
                     /region_name="betaCoV_Nsp2_SARS-like"
                     /note="betacoronavirus non-structural protein 2 (Nsp2)
                     similar to SARS-CoV Nsp2, and related proteins from
                     betacoronaviruses in the B lineage; cd21516"
                     /db_xref="CDD:439199"
     mat_peptide     819..2763
                     /product="nsp3"
                     /note="former nsp1; conserved domains are: N-terminal
                     acidic (Ac), predicted phosphoesterase, papain-like
                     proteinase, Y-domain, transmembrane domain 1 (TM1),
                     adenosine diphosphate-ribose 1''-phosphatase (ADRP);
                     produced by both pp1a and pp1ab"
                     /protein_id="YP_009725299.1"
                     /calculated_mol_wt=217254
     Region          880..1050
                     /region_name="DUF3655"
                     /note="Protein of unknown function (DUF3655); pfam12379"
                     /db_xref="CDD:432517"
     Region          1054..1177
                     /region_name="Macro_X_Nsp3-like"
                     /note="X-domain (or Mac1 domain) of viral non-structural
                     protein 3 and related macrodomains; cd21557"
                     /db_xref="CDD:438957"
     Site            order(1060..1062,1066..1072,1147..1148,1150..1154,1176)
                     /site_type="other"
                     /note="ADP-ribose binding site [chemical binding]"
                     /db_xref="CDD:438957"
     Region          1233..1358
                     /region_name="Macro_SF"
                     /note="macrodomain superfamily; cl00019"
                     /db_xref="CDD:444655"
     Site            order(1257,1267,1269,1303,1328..1335)
                     /site_type="other"
                     /note="putative ADP-ribose binding site [chemical
                     binding]"
                     /db_xref="CDD:394871"
     Region          1368..1493
                     /region_name="SUD-M"
                     /note="Single-stranded poly(A) binding domain; pfam11633"
                     /db_xref="CDD:431970"
     Region          1496..1561
                     /region_name="SUD_C_SARS-CoV_Nsp3"
                     /note="C-terminal SARS-Unique Domain (SUD) of
                     non-structural protein 3 (Nsp3) from Severe Acute
                     Respiratory Syndrome coronavirus and related
                     betacoronaviruses in the B lineage; cd21525"
                     /db_xref="CDD:394841"
     Region          1566..1868
                     /region_name="betaCoV_PLPro"
                     /note="betacoronavirus papain-like protease; cd21732"
                     /db_xref="CDD:409649"
     Site            order(1672..1675,1725..1727,1729..1730,1733,1737,1762,
                     1770..1771,1786,1788,1811,1827,1833..1836,1864)
                     /site_type="other"
                     /note="ubiquitin binding site [polypeptide binding]"
                     /db_xref="CDD:409649"
     Site            order(1725..1727,1810..1811,1827,1830,1833,1836,1864)
                     /site_type="other"
                     /note="polypeptide substrate binding site [polypeptide
                     binding]"
                     /db_xref="CDD:409649"
     Region          1913..2019
                     /region_name="SARS-CoV-like_Nsp3_NAB"
                     /note="nucleic acid binding domain of non-structural
                     protein 3 from Severe acute respiratory syndrome-related
                     coronavirus and betacoronavirus in the B lineage; cd21822"
                     /db_xref="CDD:409348"
     Region          2044..2159
                     /region_name="SARS-CoV-like_Nsp3_betaSM"
                     /note="betacoronavirus-specific marker of non-structural
                     protein 3 from Severe acute respiratory syndrome-related
                     coronavirus and betacoronavirus in the B lineage; cd21814"
                     /db_xref="CDD:409629"
     Region          2232..2762
                     /region_name="TM_Y_SARS-CoV-like_Nsp3_C"
                     /note="C-terminus of non-structural protein 3, including
                     transmembrane and Y domains, from Severe acute respiratory
                     syndrome-related coronavirus and betacoronavirus in the B
                     lineage; cd21717"
                     /db_xref="CDD:409665"
     Region          2232..2254
                     /region_name="TM1"
                     /note="TM1 [structural motif]"
                     /db_xref="CDD:409665"
     Region          2337..2359
                     /region_name="TM2"
                     /note="TM2 [structural motif]"
                     /db_xref="CDD:409665"
     mat_peptide     2764..3263
                     /product="nsp4"
                     /note="nsp4B_TM; contains transmembrane domain 2 (TM2);
                     produced by both pp1a and pp1ab"
                     /protein_id="YP_009725300.1"
                     /calculated_mol_wt=56184
     Region          2777..3157
                     /region_name="cv_Nsp4_TM"
                     /note="coronavirus non-structural protein 4 (Nsp4)
                     transmembrane domain; cd21473"
                     /db_xref="CDD:394836"
     Region          2777..2799
                     /region_name="putative TM helix 1"
                     /note="putative TM helix 1 [structural motif]"
                     /db_xref="CDD:394836"
     Region          3043..3064
                     /region_name="putative TM helix 2"
                     /note="putative TM helix 2 [structural motif]"
                     /db_xref="CDD:394836"
     Region          3079..3100
                     /region_name="putative TM helix 3"
                     /note="putative TM helix 3 [structural motif]"
                     /db_xref="CDD:394836"
     Region          3127..3149
                     /region_name="putative TM helix 4"
                     /note="putative TM helix 4 [structural motif]"
                     /db_xref="CDD:394836"
     Region          3169..3261
                     /region_name="Corona_NSP4_C"
                     /note="Coronavirus nonstructural protein 4 C-terminus;
                     pfam16348"
                     /db_xref="CDD:406690"
     mat_peptide     3264..3569
                     /product="3C-like proteinase"
                     /note="nsp5A_3CLpro and nsp5B_3CLpro; main proteinase
                     (Mpro); mediates cleavages downstream of nsp4. 3D
                     structure of the SARSr-CoV homolog has been determined
                     (Yang et al., 2003); produced by both pp1a and pp1ab"
                     /protein_id="YP_009725301.1"
                     /calculated_mol_wt=33797
     Region          3267..3563
                     /region_name="betaCoV_Nsp5_Mpro"
                     /note="betacoronavirus non-structural protein 5, also
                     called Main protease (Mpro); cd21666"
                     /db_xref="CDD:394887"
     Site            order(3267..3274,3277,3381,3385..3391,3400..3404,3429,
                     3435,3549,3553,3561..3562)
                     /site_type="other"
                     /note="homodimer interface [polypeptide binding]"
                     /db_xref="CDD:394887"
     Site            order(3284,3287..3289,3312,3317,3403..3408,3426..3429,
                     3431,3435,3450,3452..3454)
                     /site_type="other"
                     /note="polypeptide substrate binding site [polypeptide
                     binding]"
                     /db_xref="CDD:394887"
     mat_peptide     3570..3859
                     /product="nsp6"
                     /note="nsp6_TM; putative transmembrane domain; produced by
                     both pp1a and pp1ab"
                     /protein_id="YP_009725302.1"
                     /calculated_mol_wt=33034
     Region          3570..3859
                     /region_name="betaCoV-Nsp6"
                     /note="betacoronavirus non-structural protein 6; cd21560"
                     /db_xref="CDD:394846"
     mat_peptide     3860..3942
                     /product="nsp7"
                     /note="produced by both pp1a and pp1ab"
                     /protein_id="YP_009725303.1"
                     /calculated_mol_wt=9240
     Region          3860..3942
                     /region_name="betaCoV_Nsp7"
                     /note="betacoronavirus non-structural protein 7; cd21827"
                     /db_xref="CDD:409253"
     Site            order(3861,3864..3867,3870..3872,3874..3875,3878,3887,
                     3890,3896,3908..3913,3915..3920,3927..3931)
                     /site_type="other"
                     /note="oligomer interface [polypeptide binding]"
                     /db_xref="CDD:409253"
     mat_peptide     3943..4140
                     /product="nsp8"
                     /note="produced by both pp1a and pp1ab"
                     /protein_id="YP_009725304.1"
                     /calculated_mol_wt=21881
     Region          3943..4139
                     /region_name="nsp8"
                     /note="nsp8 replicase; pfam08717"
                     /db_xref="CDD:400866"
     mat_peptide     4141..4253
                     /product="nsp9"
                     /note="ssRNA-binding protein; produced by both pp1a and
                     pp1ab"
                     /protein_id="YP_009725305.1"
                     /calculated_mol_wt=12378
     Region          4141..4253
                     /region_name="betaCoV_Nsp9"
                     /note="betacoronavirus non-structural protein 9; cd21898"
                     /db_xref="CDD:409331"
     Site            4141..4146
                     /site_type="other"
                     /note="N-finger"
                     /db_xref="CDD:409331"
     Site            order(4143..4145,4147..4149,4213..4214,4236..4237,
                     4239..4241,4243..4245,4247..4249,4251..4253)
                     /site_type="other"
                     /note="homodimer interface [polypeptide binding]"
                     /db_xref="CDD:409331"
     mat_peptide     4254..4392
                     /product="nsp10"
                     /note="nsp10_CysHis; formerly known as growth-factor-like
                     protein (GFL); produced by both pp1a and pp1ab"
                     /protein_id="YP_009725306.1"
                     /calculated_mol_wt=14790
     Region          4254..4384
                     /region_name="alpha_betaCoV_Nsp10"
                     /note="alphacoronavirus and betacoronavirus non-structural
                     protein 10; cd21901"
                     /db_xref="CDD:409326"
     Site            order(4254..4261,4265,4267..4269,4271..4274,4278..4279,
                     4282..4283,4286,4293..4298,4311..4312,4322,4324..4325,
                     4329,4331..4336,4341..4343,4346..4349)
                     /site_type="other"
                     /note="Nsp14 interface [polypeptide binding]"
                     /db_xref="CDD:409326"
     Site            order(4267..4269,4271..4273,4278,4293,4295..4298,
                     4311..4313,4331..4334,4337,4348..4349,4368)
                     /site_type="other"
                     /note="oligomer interface [polypeptide binding]"
                     /db_xref="CDD:409326"
     Site            order(4274..4275,4278,4295..4298,4311..4313,4337,
                     4348..4349,4368,4372)
                     /site_type="other"
                     /note="homotrimer interface [polypeptide binding]"
                     /db_xref="CDD:409326"
     Site            order(4293..4300,4311..4312,4322..4325,4330..4331,4333,
                     4346..4349)
                     /site_type="other"
                     /note="Nsp16 interface [polypeptide binding]"
                     /db_xref="CDD:409326"
     mat_peptide     4393..5324
                     /product="RNA-dependent RNA polymerase"
                     /note="nsp12; NiRAN and RdRp; produced by pp1ab only"
                     /protein_id="YP_009725307.1"
                     /calculated_mol_wt=106661
     Region          4397..5324
                     /region_name="SARS-CoV-like_RdRp"
                     /note="Severe acute respiratory syndrome coronavirus
                     RNA-dependent RNA polymerase, also known as non-structural
                     protein 12, and similar proteins from betacoronaviruses in
                     the B lineage: responsible for replication and
                     transcription of the viral RNA genome; cd21591"
                     /db_xref="CDD:394895"
     Site            order(4661..4665,4715..4716,4718,4720..4724,4730..4733,
                     4736,4760,4763..4764,4766..4767,4770,4772..4776,
                     4778..4784,4788,4790,4794..4795,4799,4897..4898,4901,
                     4906..4907,4909,4912..4915,5058)
                     /site_type="other"
                     /note="Nsp8 interaction site [polypeptide binding]"
                     /db_xref="CDD:394895"
     Site            order(4801..4805,4807,4812,4821,4823,4832..4837,4942,4944,
                     5235)
                     /site_type="other"
                     /note="Nsp7 interaction site [polypeptide binding]"
                     /db_xref="CDD:394895"
     Site            order(4890,4892..4894,4937,4949,4951,4957,4961,4965,4969,
                     4982,4984,4986,5074..5077,5080,5150..5153,5205..5206,5224,
                     5232,5249..5250,5254,5256..5257)
                     /site_type="other"
                     /note="putative RNA binding site [nucleotide binding]"
                     /db_xref="CDD:394895"
     Site            4892..4905
                     /site_type="other"
                     /note="conserved polymerase motif G"
                     /db_xref="CDD:394895"
     Site            4930..4952
                     /site_type="other"
                     /note="conserved polymerase motif F"
                     /db_xref="CDD:394895"
     Site            order(4941,5072..5074,5079,5083,5151)
                     /site_type="inhibition"
                     /note="inhibitor binding site [chemical binding]"
                     /db_xref="CDD:394895"
     Site            5003..5019
                     /site_type="other"
                     /note="conserved polymerase motif A"
                     /db_xref="CDD:394895"
     Site            5072..5101
                     /site_type="other"
                     /note="conserved polymerase motif B"
                     /db_xref="CDD:394895"
     Site            5145..5159
                     /site_type="other"
                     /note="conserved polymerase motif C"
                     /db_xref="CDD:394895"
     Site            5167..5188
                     /site_type="other"
                     /note="conserved polymerase motif D"
                     /db_xref="CDD:394895"
     Site            5202..5213
                     /site_type="other"
                     /note="conserved polymerase motif E"
                     /db_xref="CDD:394895"
     mat_peptide     5325..5925
                     /product="helicase"
                     /note="nsp13_ZBD, nsp13_TB, and nsp_HEL1core; zinc-binding
                     domain (ZD), NTPase/helicase domain (HEL), RNA
                     5'-triphosphatase; produced by pp1ab only"
                     /protein_id="YP_009725308.1"
                     /calculated_mol_wt=66855
     Region          5325..5419
                     /region_name="ZBD_cv_Nsp13-like"
                     /note="Cys/His rich zinc-binding domain (CH/ZBD) of
                     coronavirus SARS NSP13 helicase and related proteins;
                     cd21401"
                     /db_xref="CDD:439168"
     Site            order(5369,5390,5392,5405,5414..5418)
                     /site_type="other"
                     /note="oligomer interface [polypeptide binding]"
                     /db_xref="CDD:439168"
     Region          5423..5470
                     /region_name="stalk_CoV_Nsp13-like"
                     /note="stalk domain of coronavirus Nsp13 helicase and
                     related proteins; cd21689"
                     /db_xref="CDD:410205"
     Site            order(5426,5455)
                     /site_type="other"
                     /note="key interaction residues"
                     /db_xref="CDD:410205"
     Region          5474..5552
                     /region_name="1B_cv_Nsp13-like"
                     /note="1B domain of coronavirus SARS NSP13 helicase and
                     related proteins; cd21409"
                     /db_xref="CDD:394817"
     Site            order(5502..5503,5505,5536)
                     /site_type="other"
                     /note="nucleic acid substrate binding site [nucleotide
                     binding]"
                     /db_xref="CDD:394817"
     Site            5540..5542
                     /site_type="other"
                     /note="oligomer interface [polypeptide binding]"
                     /db_xref="CDD:394817"
     Region          5575..5914
                     /region_name="betaCoV_Nsp13-helicase"
                     /note="helicase domain of betacoronavirus non-structural
                     protein 13; cd21722"
                     /db_xref="CDD:409655"
     Site            order(5609..5614,5728,5767,5862,5864,5891)
                     /site_type="other"
                     /note="ATP binding site [chemical binding]"
                     /db_xref="CDD:409655"
     Site            order(5612..5613,5698..5699,5728,5891)
                     /site_type="active"
                     /note="putative active site [active]"
                     /db_xref="CDD:409655"
     mat_peptide     5926..6452
                     /product="3'-to-5' exonuclease"
                     /note="nsp14A2_ExoN and nsp14B_NMT; produced by pp1ab
                     only"
                     /protein_id="YP_009725309.1"
                     /calculated_mol_wt=59816
     Region          5930..6450
                     /region_name="betaCoV_Nsp14"
                     /note="nonstructural protein 14 of betacoronavirus;
                     cd21659"
                     /db_xref="CDD:394958"
     Site            order(5930,5932..5935,5944..5953,5976,5980,5985..5992,
                     6026..6027,6049,6051,6055..6056,6117,6120..6121,
                     6124..6126,6142)
                     /site_type="other"
                     /note="heterodimer interface [polypeptide binding]"
                     /db_xref="CDD:394958"
     Site            order(6015,6017,6116,6193,6198)
                     /site_type="active"
                     /note="ExoN active site [active]"
                     /db_xref="CDD:394958"
     Site            order(6217,6231,6234..6235,6238,6258..6261,6263,
                     6277..6279,6291..6293,6310..6314,6326,6345,6347..6348,
                     6351,6353,6431)
                     /site_type="active"
                     /note="N7-MTase active site [active]"
                     /db_xref="CDD:394958"
     mat_peptide     6453..6798
                     /product="endoRNAse"
                     /note="nsp15-A1 and nsp15B-NendoU; produced by pp1ab only"
                     /protein_id="YP_009725310.1"
                     /calculated_mol_wt=38814
     Region          6453..6513
                     /region_name="NTD_alpha_betaCoV_Nsp15-like"
                     /note="N-terminal domain of alpha- and beta-coronavirus
                     Nonstructural protein 15 (Nsp15), and related proteins;
                     cd21171"
                     /db_xref="CDD:439163"
     Site            order(6453..6455,6473,6475..6478,6486,6491,6500,
                     6502..6505)
                     /site_type="other"
                     /note="hexamer interface [polypeptide binding]"
                     /db_xref="CDD:439163"
     Site            order(6461..6466,6479..6482,6484,6487,6489..6494,
                     6497..6500,6513)
                     /site_type="other"
                     /note="trimer interface [polypeptide binding]"
                     /db_xref="CDD:439163"
     Region          6517..6648
                     /region_name="M_alpha_beta_cv_Nsp15-like"
                     /note="middle domain of alpha- and beta-coronavirus
                     Nonstructural protein 15 (Nsp15), and related proteins;
                     cd21167"
                     /db_xref="CDD:439161"
     Site            order(6529..6530,6540,6542,6544,6546..6548,6614..6615,
                     6617..6620)
                     /site_type="other"
                     /note="trimer interface [polypeptide binding]"
                     /db_xref="CDD:439161"
     Site            6555..6556
                     /site_type="other"
                     /note="hexamer interface [polypeptide binding]"
                     /db_xref="CDD:439161"
     Region          6646..6796
                     /region_name="NendoU_cv_Nsp15-like"
                     /note="Nidoviral uridylate-specific endoribonuclease
                     (NendoU) domain of coronavirus Nonstructural Protein 15
                     (Nsp15) and related proteins; cd21161"
                     /db_xref="CDD:439158"
     Site            order(6654,6656,6692..6694,6716,6720..6721,6723,6729,6731,
                     6733,6735,6737..6738,6740)
                     /site_type="other"
                     /note="trimer interface [polypeptide binding]"
                     /db_xref="CDD:439158"
     Site            order(6686,6690,6698..6699,6701,6741,6744..6745,6792,6794)
                     /site_type="active"
                     /note="putative active site [active]"
                     /db_xref="CDD:439158"
     mat_peptide     6799..7096
                     /product="2'-O-ribose methyltransferase"
                     /note="nsp16_OMT; 2'-o-MT; produced by pp1ab only"
                     /protein_id="YP_009725311.1"
                     /calculated_mol_wt=33324
     Region          6800..7095
                     /region_name="NSP13"
                     /note="Coronavirus NSP13; pfam06460"
                     /db_xref="CDD:399456"
     CDS             1..7096
                     /gene="ORF1ab"
                     /locus_tag="GU280_gp01"
                     /coded_by="join(NC_045512.2:266..13468,
                     NC_045512.2:13468..21555)"
                     /ribosomal_slippage
                     /note="pp1ab; translated by -1 ribosomal frameshift"
                     /db_xref="GeneID:43740578"
ORIGIN      
        1 meslvpgfne kthvqlslpv lqvrdvlvrg fgdsveevls earqhlkdgt cglvevekgv
       61 lpqleqpyvf ikrsdartap hghvmvelva elegiqygrs getlgvlvph vgeipvayrk
      121 vllrkngnkg agghsygadl ksfdlgdelg tdpyedfqen wntkhssgvt relmrelngg
      181 aytryvdnnf cgpdgyplec ikdllaragk asctlseqld fidtkrgvyc creheheiaw
      241 yterseksye lqtpfeikla kkfdtfngec pnfvfplnsi iktiqprvek kkldgfmgri
      301 rsvypvaspn ecnqmclstl mkcdhcgets wqtgdfvkat cefcgtenlt kegattcgyl
      361 pqnavvkiyc pachnsevgp ehslaeyhne sglktilrkg grtiafggcv fsyvgchnkc
      421 aywvprasan igcnhtgvvg egseglndnl leilqkekvn inivgdfkln eeiaiilasf
      481 sastsafvet vkgldykafk qivescgnfk vtkgkakkga wnigeqksil splyafasea
      541 arvvrsifsr tletaqnsvr vlqkaaitil dgisqyslrl idammftsdl atnnlvvmay
      601 itggvvqlts qwltnifgtv yeklkpvldw leekfkegve flrdgweivk fistcaceiv
      661 ggqivtcake ikesvqtffk lvnkflalca dsiiiggakl kalnlgetfv thskglyrkc
      721 vksreetgll mplkapkeii flegetlpte vlteevvlkt gdlqpleqpt seaveaplvg
      781 tpvcinglml leikdtekyc alapnmmvtn ntftlkggap tkvtfgddtv ievqgyksvn
      841 itfelderid kvlnekcsay tvelgtevne facvvadavi ktlqpvsell tplgidldew
      901 smatyylfde sgefklashm ycsfyppded eeegdceeee fepstqyeyg teddyqgkpl
      961 efgatsaalq peeeqeedwl dddsqqtvgq qdgsednqtt tiqtivevqp qlemeltpvv
     1021 qtievnsfsg ylkltdnvyi knadiveeak kvkptvvvna anvylkhggg vagalnkatn
     1081 namqvesddy iatngplkvg gscvlsghnl akhclhvvgp nvnkgediql lksayenfnq
     1141 hevllaplls agifgadpih slrvcvdtvr tnvylavfdk nlydklvssf lemksekqve
     1201 qkiaeipkee vkpfiteskp sveqrkqddk kikacveevt ttleetkflt enlllyidin
     1261 gnlhpdsatl vsdiditflk kdapyivgdv vqegvltavv iptkkaggtt emlakalrkv
     1321 ptdnyittyp gqglngytve eaktvlkkck safyilpsii snekqeilgt vswnlremla
     1381 haeetrklmp vcvetkaivs tiqrkykgik iqegvvdyga rfyfytsktt vaslintlnd
     1441 lnetlvtmpl gyvthglnle eaarymrslk vpatvsvssp davtayngyl tsssktpeeh
     1501 fietislags ykdwsysgqs tqlgieflkr gdksvyytsn pttfhldgev itfdnlktll
     1561 slrevrtikv fttvdninlh tqvvdmsmty gqqfgptyld gadvtkikph nshegktfyv
     1621 lpnddtlrve afeyyhttdp sflgrymsal nhtkkwkypq vngltsikwa dnncylatal
     1681 ltlqqielkf nppalqdayy rarageaanf calilaycnk tvgelgdvre tmsylfqhan
     1741 ldsckrvlnv vcktcgqqqt tlkgveavmy mgtlsyeqfk kgvqipctcg kqatkylvqq
     1801 espfvmmsap paqyelkhgt ftcaseytgn yqcghykhit sketlycidg alltksseyk
     1861 gpitdvfyke nsytttikpv tykldgvvct eidpkldnyy kkdnsyfteq pidlvpnqpy
     1921 pnasfdnfkf vcdnikfadd lnqltgykkp asrelkvtff pdlngdvvai dykhytpsfk
     1981 kgakllhkpi vwhvnnatnk atykpntwci rclwstkpve tsnsfdvlks edaqgmdnla
     2041 cedlkpvsee vvenptiqkd vlecnvktte vvgdiilkpa nnslkiteev ghtdlmaayv
     2101 dnssltikkp nelsrvlglk tlathglaav nsvpwdtian yakpflnkvv stttnivtrc
     2161 lnrvctnymp yfftlllqlc tftrstnsri kasmpttiak ntvksvgkfc leasfnylks
     2221 pnfsklinii iwflllsvcl gsliystaal gvlmsnlgmp syctgyregy lnstnvtiat
     2281 yctgsipcsv clsgldsldt ypsletiqit issfkwdlta fglvaewfla yilftrffyv
     2341 lglaaimqlf fsyfavhfis nswlmwliin lvqmapisam vrmyiffasf yyvwksyvhv
     2401 vdgcnsstcm mcykrnratr vecttivngv rrsfyvyang gkgfcklhnw ncvncdtfca
     2461 gstfisdeva rdlslqfkrp inptdqssyi vdsvtvkngs ihlyfdkagq ktyerhslsh
     2521 fvnldnlran ntkgslpinv ivfdgkskce essaksasvy ysqlmcqpil lldqalvsdv
     2581 gdsaevavkm fdayvntfss tfnvpmeklk tlvataeael aknvsldnvl stfisaarqg
     2641 fvdsdvetkd vveclklshq sdievtgdsc nnymltynkv enmtprdlga cidcsarhin
     2701 aqvakshnia liwnvkdfms lseqlrkqir saakknnlpf kltcattrqv vnvvttkial
     2761 kggkivnnwl kqlikvtlvf lfvaaifyli tpvhvmskht dfsseiigyk aidggvtrdi
     2821 astdtcfank hadfdtwfsq rggsytndka cpliaavitr evgfvvpglp gtilrttngd
     2881 flhflprvfs avgnicytps klieytdfat sacvlaaect ifkdasgkpv pycydtnvle
     2941 gsvayeslrp dtryvlmdgs iiqfpntyle gsvrvvttfd seycrhgtce rseagvcvst
     3001 sgrwvlnndy yrslpgvfcg vdavnlltnm ftpliqpiga ldisasivag givaivvtcl
     3061 ayyfmrfrra fgeyshvvaf ntllflmsft vlcltpvysf lpgvysviyl yltfyltndv
     3121 sflahiqwmv mftplvpfwi tiayiicist khfywffsny lkrrvvfngv sfstfeeaal
     3181 ctfllnkemy lklrsdvllp ltqynrylal ynkykyfsga mdttsyreaa cchlakalnd
     3241 fsnsgsdvly qppqtsitsa vlqsgfrkma fpsgkvegcm vqvtcgtttl nglwlddvvy
     3301 cprhvictse dmlnpnyedl lirksnhnfl vqagnvqlrv ighsmqncvl klkvdtanpk
     3361 tpkykfvriq pgqtfsvlac yngspsgvyq camrpnftik gsflngscgs vgfnidydcv
     3421 sfcymhhmel ptgvhagtdl egnfygpfvd rqtaqaagtd ttitvnvlaw lyaavingdr
     3481 wflnrftttl ndfnlvamky nyepltqdhv dilgplsaqt giavldmcas lkellqngmn
     3541 grtilgsall edeftpfdvv rqcsgvtfqs avkrtikgth hwllltilts llvlvqstqw
     3601 slffflyena flpfamgiia msafammfvk hkhaflclfl lpslatvayf nmvympaswv
     3661 mrimtwldmv dtslsgfklk dcvmyasavv llilmtartv yddgarrvwt lmnvltlvyk
     3721 vyygnaldqa ismwaliisv tsnysgvvtt vmflargivf mcveycpiff itgntlqcim
     3781 lvycflgyfc tcyfglfcll nryfrltlgv ydylvstqef rymnsqgllp pknsidafkl
     3841 nikllgvggk pcikvatvqs kmsdvkctsv vllsvlqqlr vesssklwaq cvqlhndill
     3901 akdtteafek mvsllsvlls mqgavdinkl ceemldnrat lqaiasefss lpsyaafata
     3961 qeayeqavan gdsevvlkkl kkslnvakse fdrdaamqrk lekmadqamt qmykqarsed
     4021 krakvtsamq tmlftmlrkl dndalnniin nardgcvpln iiplttaakl mvvipdynty
     4081 kntcdgttft yasalweiqq vvdadskivq lseismdnsp nlawplivta lransavklq
     4141 nnelspvalr qmscaagttq tactddnala yynttkggrf vlallsdlqd lkwarfpksd
     4201 gtgtiytele ppcrfvtdtp kgpkvkylyf ikglnnlnrg mvlgslaatv rlqagnatev
     4261 panstvlsfc afavdaakay kdylasggqp itncvkmlct htgtgqaitv tpeanmdqes
     4321 fggascclyc rchidhpnpk gfcdlkgkyv qipttcandp vgftlkntvc tvcgmwkgyg
     4381 cscdqlrepm lqsadaqsfl nrvcgvsaar ltpcgtgtst dvvyrafdiy ndkvagfakf
     4441 lktnccrfqe kdeddnlids yfvvkrhtfs nyqheetiyn llkdcpavak hdffkfridg
     4501 dmvphisrqr ltkytmadlv yalrhfdegn cdtlkeilvt ynccdddyfn kkdwydfven
     4561 pdilrvyanl gervrqallk tvqfcdamrn agivgvltld nqdlngnwyd fgdfiqttpg
     4621 sgvpvvdsyy sllmpiltlt raltaeshvd tdltkpyikw dllkydftee rlklfdryfk
     4681 ywdqtyhpnc vnclddrcil hcanfnvlfs tvfpptsfgp lvrkifvdgv pfvvstgyhf
     4741 relgvvhnqd vnlhssrlsf kellvyaadp amhaasgnll ldkrttcfsv aaltnnvafq
     4801 tvkpgnfnkd fydfavskgf fkegssvelk hfffaqdgna aisdydyyry nlptmcdirq
     4861 llfvvevvdk yfdcydggci nanqvivnnl dksagfpfnk wgkarlyyds msyedqdalf
     4921 aytkrnvipt itqmnlkyai saknrartva gvsicstmtn rqfhqkllks iaatrgatvv
     4981 igtskfyggw hnmlktvysd venphlmgwd ypkcdrampn mlrimaslvl arkhttccsl
     5041 shrfyrlane caqvlsemvm cggslyvkpg gtssgdatta yansvfnicq avtanvnall
     5101 stdgnkiadk yvrnlqhrly eclyrnrdvd tdfvnefyay lrkhfsmmil sddavvcfns
     5161 tyasqglvas iknfksvlyy qnnvfmseak cwtetdltkg phefcsqhtm lvkqgddyvy
     5221 lpypdpsril gagcfvddiv ktdgtlmier fvslaidayp ltkhpnqeya dvfhlylqyi
     5281 rklhdeltgh mldmysvmlt ndntsrywep efyeamytph tvlqavgacv lcnsqtslrc
     5341 gacirrpflc ckccydhvis tshklvlsvn pyvcnapgcd vtdvtqlylg gmsyyckshk
     5401 ppisfplcan gqvfglyknt cvgsdnvtdf naiatcdwtn agdyilantc terlklfaae
     5461 tlkateetfk lsygiatvre vlsdrelhls wevgkprppl nrnyvftgyr vtknskvqig
     5521 eytfekgdyg davvyrgttt yklnvgdyfv ltshtvmpls aptlvpqehy vritglyptl
     5581 nisdefssnv anyqkvgmqk ystlqgppgt gkshfaigla lyypsarivy tacshaavda
     5641 lcekalkylp idkcsriipa rarvecfdkf kvnstleqyv fctvnalpet tadivvfdei
     5701 smatnydlsv vnarlrakhy vyigdpaqlp aprtlltkgt lepeyfnsvc rlmktigpdm
     5761 flgtcrrcpa eivdtvsalv ydnklkahkd ksaqcfkmfy kgvithdvss ainrpqigvv
     5821 refltrnpaw rkavfispyn sqnavaskil glptqtvdss qgseydyvif tqttetahsc
     5881 nvnrfnvait rakvgilcim sdrdlydklq ftsleiprrn vatlqaenvt glfkdcskvi
     5941 tglhptqapt hlsvdtkfkt eglcvdipgi pkdmtyrrli smmgfkmnyq vngypnmfit
     6001 reeairhvra wigfdvegch atreavgtnl plqlgfstgv nlvavptgyv dtpnntdfsr
     6061 vsakpppgdq fkhliplmyk glpwnvvrik ivqmlsdtlk nlsdrvvfvl wahgfeltsm
     6121 kyfvkigper tcclcdrrat cfstasdtya cwhhsigfdy vynpfmidvq qwgftgnlqs
     6181 nhdlycqvhg nahvascdai mtrclavhec fvkrvdwtie ypiigdelki naacrkvqhm
     6241 vvkaalladk fpvlhdignp kaikcvpqad vewkfydaqp csdkaykiee lfysyathsd
     6301 kftdgvclfw ncnvdrypan sivcrfdtrv lsnlnlpgcd ggslyvnkha fhtpafdksa
     6361 fvnlkqlpff yysdspcesh gkqvvsdidy vplksatcit rcnlggavcr hhaneyrlyl
     6421 daynmmisag fslwvykqfd tynlwntftr lqslenvafn vvnkghfdgq qgevpvsiin
     6481 ntvytkvdgv dvelfenktt lpvnvafelw akrnikpvpe vkilnnlgvd iaantviwdy
     6541 krdapahist igvcsmtdia kkpteticap ltvffdgrvd gqvdlfrnar ngvlitegsv
     6601 kglqpsvgpk qaslngvtli geavktqfny ykkvdgvvqq lpetyftqsr nlqefkprsq
     6661 meidflelam defierykle gyafehivyg dfshsqlggl hlliglakrf kespfeledf
     6721 ipmdstvkny fitdaqtgss kcvcsvidll lddfveiiks qdlsvvskvv kvtidyteis
     6781 fmlwckdghv etfypklqss qawqpgvamp nlykmqrmll ekcdlqnygd satlpkgimm
     6841 nvakytqlcq ylntltlavp ynmrvihfga gsdkgvapgt avlrqwlptg tllvdsdlnd
     6901 fvsdadstli gdcatvhtan kwdliisdmy dpktknvtke ndskegffty icgfiqqkla
     6961 lggsvaikit ehswnadlyk lmghfawwta fvtnvnasss eafligcnyl gkpreqidgy
     7021 vmhanyifwr ntnpiqlssy slfdmskfpl klrgtavmsl kegqindmil sllskgrlii
     7081 rennrvviss dvlvnn
//

