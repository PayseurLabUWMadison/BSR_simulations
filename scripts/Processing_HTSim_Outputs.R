## Will Spurley
## Date: 10/18/2023
## Email: wspurley@wisc.edu
## Description: Taking the summary statistic output files from HTSimulate and combining them all into one large dataframe

## Make sure this is the correct directory! 
setwd("/Users/willspurley/Simulation_Pilot/data/many_sim_pilot/")

## Initialize an empty maxtrix to populate (Adjust sizes based on number of columns in updated dataframe)
df_matrix_mean = matrix(NA, nrow=0, ncol=34)
df_matrix_var = matrix(NA, nrow=0, ncol=31)

list_of_prefix = c('EQUI_a1_r5e-9_m5e-9', 'EQUI_a1_r5e-9_m5e-8', 'EQUI_a1_r5e-8_m5e-9', 'EQUI_a1_r5e-8_m5e-8', 'EQUI_a3_r5e-9_m5e-9', 'EQUI_a3_r5e-9_m5e-8', 'EQUI_a3_r5e-8_m5e-9', 'EQUI_a3_r5e-8_m5e-8', 'BSRS_a1_r5e-9_m5e-9', 'BSRS_a1_r5e-9_m5e-8', 'BSRS_a1_r5e-8_m5e-9', 'BSRS_a1_r5e-8_m5e-8', 'BSRS_a3_r5e-9_m5e-9', 'BSRS_a3_r5e-9_m5e-8', 'BSRS_a3_r5e-8_m5e-9', 'BSRS_a3_r5e-8_m5e-8', 'BSMS_a1_r5e-9_m5e-9', 'BSMS_a1_r5e-9_m5e-8', 'BSMS_a1_r5e-8_m5e-9', 'BSMS_a1_r5e-8_m5e-8', 'BSMS_a3_r5e-9_m5e-9', 'BSMS_a3_r5e-9_m5e-8', 'BSMS_a3_r5e-8_m5e-9', 'BSMS_a3_r5e-8_m5e-8', 'BSRL_a1_r5e-9_m5e-9', 'BSRL_a1_r5e-9_m5e-8', 'BSRL_a1_r5e-8_m5e-9', 'BSRL_a1_r5e-8_m5e-8', 'BSRL_a3_r5e-9_m5e-9', 'BSRL_a3_r5e-9_m5e-8', 'BSRL_a3_r5e-8_m5e-9', 'BSRL_a3_r5e-8_m5e-8', 'BSML_a1_r5e-9_m5e-9', 'BSML_a1_r5e-9_m5e-8', 'BSML_a1_r5e-8_m5e-9', 'BSML_a1_r5e-8_m5e-8', 'BSML_a3_r5e-9_m5e-9', 'BSML_a3_r5e-9_m5e-8', 'BSML_a3_r5e-8_m5e-9', 'BSML_a3_r5e-8_m5e-8', 'BWRS_a1_r5e-9_m5e-9', 'BWRS_a1_r5e-9_m5e-8', 'BWRS_a1_r5e-8_m5e-9', 'BWRS_a1_r5e-8_m5e-8', 'BWRS_a3_r5e-9_m5e-9', 'BWRS_a3_r5e-9_m5e-8', 'BWRS_a3_r5e-8_m5e-9', 'BWRS_a3_r5e-8_m5e-8', 'BWMS_a1_r5e-9_m5e-9', 'BWMS_a1_r5e-9_m5e-8', 'BWMS_a1_r5e-8_m5e-9', 'BWMS_a1_r5e-8_m5e-8', 'BWMS_a3_r5e-9_m5e-9', 'BWMS_a3_r5e-9_m5e-8', 'BWMS_a3_r5e-8_m5e-9', 'BWMS_a3_r5e-8_m5e-8', 'BWRL_a1_r5e-9_m5e-9', 'BWRL_a1_r5e-9_m5e-8', 'BWRL_a1_r5e-8_m5e-9', 'BWRL_a1_r5e-8_m5e-8', 'BWRL_a3_r5e-9_m5e-9', 'BWRL_a3_r5e-9_m5e-8', 'BWRL_a3_r5e-8_m5e-9', 'BWRL_a3_r5e-8_m5e-8', 'BWML_a1_r5e-9_m5e-9', 'BWML_a1_r5e-9_m5e-8', 'BWML_a1_r5e-8_m5e-9', 'BWML_a1_r5e-8_m5e-8', 'BWML_a3_r5e-9_m5e-9', 'BWML_a3_r5e-9_m5e-8', 'BWML_a3_r5e-8_m5e-9', 'BWML_a3_r5e-8_m5e-8', 'BSDS_a1_r5e-9_m5e-9', 'BSDS_a1_r5e-9_m5e-8', 'BSDS_a1_r5e-8_m5e-9', 'BSDS_a1_r5e-8_m5e-8', 'BSDS_a3_r5e-9_m5e-9', 'BSDS_a3_r5e-9_m5e-8', 'BSDS_a3_r5e-8_m5e-9', 'BSDS_a3_r5e-8_m5e-8', 'BSDL_a1_r5e-9_m5e-9', 'BSDL_a1_r5e-9_m5e-8', 'BSDL_a1_r5e-8_m5e-9', 'BSDL_a1_r5e-8_m5e-8', 'BSDL_a3_r5e-9_m5e-9', 'BSDL_a3_r5e-9_m5e-8', 'BSDL_a3_r5e-8_m5e-9', 'BSDL_a3_r5e-8_m5e-8', 'BWDS_a1_r5e-9_m5e-9', 'BWDS_a1_r5e-9_m5e-8', 'BWDS_a1_r5e-8_m5e-9', 'BWDS_a1_r5e-8_m5e-8', 'BWDS_a3_r5e-9_m5e-9', 'BWDS_a3_r5e-9_m5e-8', 'BWDS_a3_r5e-8_m5e-9', 'BWDS_a3_r5e-8_m5e-8', 'BWDL_a1_r5e-9_m5e-9', 'BWDL_a1_r5e-9_m5e-8', 'BWDL_a1_r5e-8_m5e-9', 'BWDL_a1_r5e-8_m5e-8', 'BWDL_a3_r5e-9_m5e-9', 'BWDL_a3_r5e-9_m5e-8', 'BWDL_a3_r5e-8_m5e-9', 'BWDL_a3_r5e-8_m5e-8', 'ESRS_a1_r5e-9_m5e-9', 'ESRS_a1_r5e-9_m5e-8', 'ESRS_a1_r5e-8_m5e-9', 'ESRS_a1_r5e-8_m5e-8', 'ESRS_a3_r5e-9_m5e-9', 'ESRS_a3_r5e-9_m5e-8', 'ESRS_a3_r5e-8_m5e-9', 'ESRS_a3_r5e-8_m5e-8', 'EFRS_a1_r5e-9_m5e-9', 'EFRS_a1_r5e-9_m5e-8', 'EFRS_a1_r5e-8_m5e-9', 'EFRS_a1_r5e-8_m5e-8', 'EFRS_a3_r5e-9_m5e-9', 'EFRS_a3_r5e-9_m5e-8', 'EFRS_a3_r5e-8_m5e-9', 'EFRS_a3_r5e-8_m5e-8', 'ESRL_a1_r5e-9_m5e-9', 'ESRL_a1_r5e-9_m5e-8', 'ESRL_a1_r5e-8_m5e-9', 'ESRL_a1_r5e-8_m5e-8', 'ESRL_a3_r5e-9_m5e-9', 'ESRL_a3_r5e-9_m5e-8', 'ESRL_a3_r5e-8_m5e-9', 'ESRL_a3_r5e-8_m5e-8', 'EFRL_a1_r5e-9_m5e-9', 'EFRL_a1_r5e-9_m5e-8', 'EFRL_a1_r5e-8_m5e-9', 'EFRL_a1_r5e-8_m5e-8', 'EFRL_a3_r5e-9_m5e-9', 'EFRL_a3_r5e-9_m5e-8', 'EFRL_a3_r5e-8_m5e-9', 'EFRL_a3_r5e-8_m5e-8', 'ESDS_a1_r5e-9_m5e-9', 'ESDS_a1_r5e-9_m5e-8', 'ESDS_a1_r5e-8_m5e-9', 'ESDS_a1_r5e-8_m5e-8', 'ESDS_a3_r5e-9_m5e-9', 'ESDS_a3_r5e-9_m5e-8', 'ESDS_a3_r5e-8_m5e-9', 'ESDS_a3_r5e-8_m5e-8', 'EFDS_a1_r5e-9_m5e-9', 'EFDS_a1_r5e-9_m5e-8', 'EFDS_a1_r5e-8_m5e-9', 'EFDS_a1_r5e-8_m5e-8', 'EFDS_a3_r5e-9_m5e-9', 'EFDS_a3_r5e-9_m5e-8', 'EFDS_a3_r5e-8_m5e-9', 'EFDS_a3_r5e-8_m5e-8', 'ESDL_a1_r5e-9_m5e-9', 'ESDL_a1_r5e-9_m5e-8', 'ESDL_a1_r5e-8_m5e-9', 'ESDL_a1_r5e-8_m5e-8', 'ESDL_a3_r5e-9_m5e-9', 'ESDL_a3_r5e-9_m5e-8', 'ESDL_a3_r5e-8_m5e-9', 'ESDL_a3_r5e-8_m5e-8', 'EFDL_a1_r5e-9_m5e-9', 'EFDL_a1_r5e-9_m5e-8', 'EFDL_a1_r5e-8_m5e-9', 'EFDL_a1_r5e-8_m5e-8', 'EFDL_a3_r5e-9_m5e-9', 'EFDL_a3_r5e-9_m5e-8', 'EFDL_a3_r5e-8_m5e-9', 'EFDL_a3_r5e-8_m5e-8', 'BMRS_a1_r5e-9_m5e-9', 'BMRS_a1_r5e-9_m5e-8', 'BMRS_a1_r5e-8_m5e-9', 'BMRS_a1_r5e-8_m5e-8', 'BMRS_a3_r5e-9_m5e-9', 'BMRS_a3_r5e-9_m5e-8', 'BMRS_a3_r5e-8_m5e-9', 'BMRS_a3_r5e-8_m5e-8', 'BMRL_a1_r5e-9_m5e-9', 'BMRL_a1_r5e-9_m5e-8', 'BMRL_a1_r5e-8_m5e-9', 'BMRL_a1_r5e-8_m5e-8', 'BMRL_a3_r5e-9_m5e-9', 'BMRL_a3_r5e-9_m5e-8', 'BMRL_a3_r5e-8_m5e-9', 'BMRL_a3_r5e-8_m5e-8', 'BMMS_a1_r5e-9_m5e-9', 'BMMS_a1_r5e-9_m5e-8', 'BMMS_a1_r5e-8_m5e-9', 'BMMS_a1_r5e-8_m5e-8', 'BMMS_a3_r5e-9_m5e-9', 'BMMS_a3_r5e-9_m5e-8', 'BMMS_a3_r5e-8_m5e-9', 'BMMS_a3_r5e-8_m5e-8', 'BMML_a1_r5e-9_m5e-9', 'BMML_a1_r5e-9_m5e-8', 'BMML_a1_r5e-8_m5e-9', 'BMML_a1_r5e-8_m5e-8', 'BMML_a3_r5e-9_m5e-9', 'BMML_a3_r5e-9_m5e-8', 'BMML_a3_r5e-8_m5e-9', 'BMML_a3_r5e-8_m5e-8', 'BMDS_a1_r5e-9_m5e-9', 'BMDS_a1_r5e-9_m5e-8', 'BMDS_a1_r5e-8_m5e-9', 'BMDS_a1_r5e-8_m5e-8', 'BMDS_a3_r5e-9_m5e-9', 'BMDS_a3_r5e-9_m5e-8', 'BMDS_a3_r5e-8_m5e-9', 'BMDS_a3_r5e-8_m5e-8', 'BMDL_a1_r5e-9_m5e-9', 'BMDL_a1_r5e-9_m5e-8', 'BMDL_a1_r5e-8_m5e-9', 'BMDL_a1_r5e-8_m5e-8', 'BMDL_a3_r5e-9_m5e-9', 'BMDL_a3_r5e-9_m5e-8', 'BMDL_a3_r5e-8_m5e-9', 'BMDL_a3_r5e-8_m5e-8', 'BSRX_a1_r5e-9_m5e-9', 'BSRX_a1_r5e-9_m5e-8', 'BSRX_a1_r5e-8_m5e-9', 'BSRX_a1_r5e-8_m5e-8', 'BSRX_a3_r5e-9_m5e-9', 'BSRX_a3_r5e-9_m5e-8', 'BSRX_a3_r5e-8_m5e-9', 'BSRX_a3_r5e-8_m5e-8', 'BSMX_a1_r5e-9_m5e-9', 'BSMX_a1_r5e-9_m5e-8', 'BSMX_a1_r5e-8_m5e-9', 'BSMX_a1_r5e-8_m5e-8', 'BSMX_a3_r5e-9_m5e-9', 'BSMX_a3_r5e-9_m5e-8', 'BSMX_a3_r5e-8_m5e-9', 'BSMX_a3_r5e-8_m5e-8', 'BSDX_a1_r5e-9_m5e-9', 'BSDX_a1_r5e-9_m5e-8', 'BSDX_a1_r5e-8_m5e-9', 'BSDX_a1_r5e-8_m5e-8', 'BSDX_a3_r5e-9_m5e-9', 'BSDX_a3_r5e-9_m5e-8', 'BSDX_a3_r5e-8_m5e-9', 'BSDX_a3_r5e-8_m5e-8', 'BWRX_a1_r5e-9_m5e-9', 'BWRX_a1_r5e-9_m5e-8', 'BWRX_a1_r5e-8_m5e-9', 'BWRX_a1_r5e-8_m5e-8', 'BWRX_a3_r5e-9_m5e-9', 'BWRX_a3_r5e-9_m5e-8', 'BWRX_a3_r5e-8_m5e-9', 'BWRX_a3_r5e-8_m5e-8', 'BWMX_a1_r5e-9_m5e-9', 'BWMX_a1_r5e-9_m5e-8', 'BWMX_a1_r5e-8_m5e-9', 'BWMX_a1_r5e-8_m5e-8', 'BWMX_a3_r5e-9_m5e-9', 'BWMX_a3_r5e-9_m5e-8', 'BWMX_a3_r5e-8_m5e-9', 'BWMX_a3_r5e-8_m5e-8', 'BWDX_a1_r5e-9_m5e-9', 'BWDX_a1_r5e-9_m5e-8', 'BWDX_a1_r5e-8_m5e-9', 'BWDX_a1_r5e-8_m5e-8', 'BWDX_a3_r5e-9_m5e-9', 'BWDX_a3_r5e-9_m5e-8', 'BWDX_a3_r5e-8_m5e-9', 'BWDX_a3_r5e-8_m5e-8', 'BMRX_a1_r5e-9_m5e-9', 'BMRX_a1_r5e-9_m5e-8', 'BMRX_a1_r5e-8_m5e-9', 'BMRX_a1_r5e-8_m5e-8', 'BMRX_a3_r5e-9_m5e-9', 'BMRX_a3_r5e-9_m5e-8', 'BMRX_a3_r5e-8_m5e-9', 'BMRX_a3_r5e-8_m5e-8', 'BMMX_a1_r5e-9_m5e-9', 'BMMX_a1_r5e-9_m5e-8', 'BMMX_a1_r5e-8_m5e-9', 'BMMX_a1_r5e-8_m5e-8', 'BMMX_a3_r5e-9_m5e-9', 'BMMX_a3_r5e-9_m5e-8', 'BMMX_a3_r5e-8_m5e-9', 'BMMX_a3_r5e-8_m5e-8', 'BMDX_a1_r5e-9_m5e-9', 'BMDX_a1_r5e-9_m5e-8', 'BMDX_a1_r5e-8_m5e-9', 'BMDX_a1_r5e-8_m5e-8', 'BMDX_a3_r5e-9_m5e-9', 'BMDX_a3_r5e-9_m5e-8', 'BMDX_a3_r5e-8_m5e-9', 'BMDX_a3_r5e-8_m5e-8')

# Data frame that will be filled with 
All_Demo_Mean_Summary_Stats = data.frame(df_matrix_mean)
for (prefix in list_of_prefix) {
  # read in all Autosome summary stat files

  Af_01 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_1.csv", sep = ""))
  Af_015 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_15.csv", sep = ""))
  Af_02 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_2.csv", sep = ""))
  Af_025 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_25.csv", sep = ""))
  Af_03 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_3.csv", sep = ""))
  Af_035 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_35.csv", sep = ""))
  Af_04 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_4.csv", sep = ""))
  Af_045 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_45.csv", sep = ""))
  Af_05 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_5.csv", sep = ""))
  Af_055 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_55.csv", sep = ""))
  Af_06 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_6.csv", sep = ""))
  Af_065 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_65.csv", sep = ""))
  Af_07 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_7.csv", sep = ""))
  Af_075 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_75.csv", sep = ""))
  Af_08 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_8.csv", sep = ""))
  Af_085 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_85.csv", sep = ""))
  Af_09 = read.csv(paste(prefix,"/A",prefix,"_summarized_mean_sum_stats_pf0_9.csv", sep = ""))
  
  # read in all X chr summary stat files
  Xf_01 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_1.csv", sep = ""))
  Xf_015 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_15.csv", sep = ""))
  Xf_02 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_2.csv", sep = ""))
  Xf_025 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_25.csv", sep = ""))
  Xf_03 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_3.csv", sep = ""))
  Xf_035 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_35.csv", sep = ""))
  Xf_04 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_4.csv", sep = ""))
  Xf_045 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_45.csv", sep = ""))
  Xf_05 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_5.csv", sep = ""))
  Xf_055 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_55.csv", sep = ""))
  Xf_06 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_6.csv", sep = ""))
  Xf_065 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_65.csv", sep = ""))
  Xf_07 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_7.csv", sep = ""))
  Xf_075 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_75.csv", sep = ""))
  Xf_08 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_8.csv", sep = ""))
  Xf_085 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_85.csv", sep = ""))
  Xf_09 = read.csv(paste(prefix,"/X",prefix,"_summarized_mean_sum_stats_pf0_9.csv", sep = ""))
  
  Af = rbind(Af_01, Af_015, Af_02, Af_025, Af_03, Af_035, Af_04, Af_045, Af_05, Af_055, Af_06, Af_065, Af_07, Af_075, Af_08, Af_085, Af_09)
  Af$Chromosome = "Autosome"
  
  Xf = rbind(Xf_01, Xf_015, Xf_02, Xf_025, Xf_03, Xf_035, Xf_04, Xf_045, Xf_05, Xf_055, Xf_06, Xf_065, Xf_07, Xf_075, Xf_08, Xf_085, Xf_09)
  Xf$Chromosome = "X Chromosome"
  
  Total_f = rbind(Af, Xf)

  ## Put Total_f in a larger dataframe 
  colnames(All_Demo_Mean_Summary_Stats) = colnames(Total_f)
  All_Demo_Mean_Summary_Stats = rbind(All_Demo_Mean_Summary_Stats, Total_f)
}

# Write output file 
All_Demo_Mean_Summary_Stats <- All_Demo_Mean_Summary_Stats[,c(-1)]
write.csv(All_Demo_Mean_Summary_Stats, file = "All_Combos_Mean_Summary_Stats.csv")

print("Created Mean Summary Stastistic Dataset")


## /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ## 

All_Demo_Variance_Summary_Stats = data.frame(df_matrix_var)

for (prefix in list_of_prefix) {
  # read in all Autosome variance summary stat files
  Af_01 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_1.csv", sep = ""))
  Af_015 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_15.csv", sep = ""))
  Af_02 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_2.csv", sep = ""))
  Af_025 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_25.csv", sep = ""))
  Af_03 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_3.csv", sep = ""))
  Af_035 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_35.csv", sep = ""))
  Af_04 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_4.csv", sep = ""))
  Af_045 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_45.csv", sep = ""))
  Af_05 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_5.csv", sep = ""))
  Af_055 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_55.csv", sep = ""))
  Af_06 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_6.csv", sep = ""))
  Af_065 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_65.csv", sep = ""))
  Af_07 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_7.csv", sep = ""))
  Af_075 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_75.csv", sep = ""))
  Af_08 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_8.csv", sep = ""))
  Af_085 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_85.csv", sep = ""))
  Af_09 = read.csv(paste(prefix,"/A",prefix,"_summarized_variance_sum_stats_pf0_9.csv", sep = ""))
  
  # read in all X chr variance summary stat files
  Xf_01 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_1.csv", sep = ""))
  Xf_015 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_15.csv", sep = ""))
  Xf_02 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_2.csv", sep = ""))
  Xf_025 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_25.csv", sep = ""))
  Xf_03 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_3.csv", sep = ""))
  Xf_035 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_35.csv", sep = ""))
  Xf_04 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_4.csv", sep = ""))
  Xf_045 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_45.csv", sep = ""))
  Xf_05 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_5.csv", sep = ""))
  Xf_055 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_55.csv", sep = ""))
  Xf_06 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_6.csv", sep = ""))
  Xf_065 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_65.csv", sep = ""))
  Xf_07 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_7.csv", sep = ""))
  Xf_075 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_75.csv", sep = ""))
  Xf_08 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_8.csv", sep = ""))
  Xf_085 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_85.csv", sep = ""))
  Xf_09 = read.csv(paste(prefix,"/X",prefix,"_summarized_variance_sum_stats_pf0_9.csv", sep = ""))
  
  Af = rbind(Af_01, Af_015, Af_02, Af_025, Af_03, Af_035, Af_04, Af_045, Af_05, Af_055, Af_06, Af_065, Af_07, Af_075, Af_08, Af_085, Af_09)
  Af$Chromosome = "Autosome"
  
  Xf = rbind(Xf_01, Xf_015, Xf_02, Xf_025, Xf_03, Xf_035, Xf_04, Xf_045, Xf_05, Xf_055, Xf_06, Xf_065, Xf_07, Xf_075, Xf_08, Xf_085, Xf_09)
  Xf$Chromosome = "X Chromosome"
  
  Total_f = rbind(Af, Xf)

  ## Put Total_f in a larger dataframe 
  colnames(All_Demo_Variance_Summary_Stats) = colnames(Total_f)
  All_Demo_Variance_Summary_Stats = rbind(All_Demo_Variance_Summary_Stats, Total_f)
}


# Write output file 
All_Demo_Variance_Summary_Stats <- All_Demo_Variance_Summary_Stats[,c(-1)]
write.csv(All_Demo_Variance_Summary_Stats, file="All_Combos_Variance_Summary_Stats.csv")

print("Created Variance Summary Statistic Dataset - happy plotting!")




