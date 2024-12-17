## Will Spurley
## wspurley@wisc.edu
## 2023-08-24
## Simulating Autosomes and X Chromosomes
## Simulating chromosomal loci in repeated fashion, outputting summary statistics and site frequency spectra for each replicate.

import msprime
import copy
import allel
import os
import pandas as pd 
import numpy as np
import statistics



class Autosome:
	"""Parameters:
	 ___________________
	 ind: number of individuals to sample
	 rec_rate: sex-averaged per-site recombination rate 
	 mut_rate_A: autosomal per-site recombination rate 
	 ploidy: ploidy of sample (defaults to 2)
	 length: sequence length simulated segment
	 pf: proportion of breeding individuals that are female. 
	 pop_size: effective population size of simulated population (default 1, will be modified based on pf)
	 alpha: ratio of male per-site mutation rate to female per-site mutation rate (defaults to 1)
	 pf_out: proportion of females expressed as a string, replacing the period with an underscore (eg. "0_5" instead of 0.5)
	 ___________________
	 Note: please include 0 when setting pf (example: use 0.5 instead of .5)
	 If running simualtions for populations with demograhpy object, the pop_size command will be ignored

	"""
	def __init__(self, ind=10, rec_rate=None, mut_rate_A=None, length=None, pf=0.5, pop_size=1, alpha = 1, demography=None):
		self.ind = ind
		self.ploidy = 2
		self.length = length
		self.pf = pf
		self.demography = copy.deepcopy(demography)
		aut_var = 4*pf*(1-pf) #adjust parameters according to the proportion of females in the population 


		# Modify effectivee population size based on breeding sex ratio
			## For demography object, adjust all epochs using the same BSR 
		if self.demography == None:
			self.pop_size = aut_var * pop_size
		else:
			for pop in self.demography.values():
				pop.initial_size *= aut_var
			for event in self.demography.events:
				if event.initial_size == None:
					continue
				event.initial_size *= aut_var

		self.rec_rate_A = rec_rate
		self.mut_rate_A = mut_rate_A
		self.alpha = alpha


		self.parent_path = os.getcwd()

 		# Report parameters for autosome after modifying for BSR 
		print("Autosome parameters (pf = "+str(self.pf)+"):")
		print("Mutation rate: ", self.mut_rate_A)
		print("Recombination rate: ", self.rec_rate_A)
		if self.demography == None:
			print("Effective Population Size: ", self.pop_size)
		else:
			print(self.demography)

	def simulate(self, reps, loci, pf_out="0_5", prefix="Autosome"):

		self.pf_out = str(pf_out)
		self.prefix = prefix
		self.loci = loci
		self.reps = reps
		num_ind = self.ind
		nchr = num_ind*self.ploidy
		seq_length = self.length

		## Make output data dictonary
		mean_dictA = {"mean_pi":[], "mean_theta":[], "mean_r2":[], "mean_r2_var":[], "mean_K":[], "mean_M":[], "mean_TD":[], "mean_S":[]}
		var_dictA = {"var_pi":[], "var_theta":[], "var_mr2":[], "var_r2_var":[], "var_K":[], "var_M":[],"var_TD":[] ,"var_S":[]}

		## lists to populate the dictionary 
		# mean lists 
		m_pi_list = []
		m_theta_list = []
		m_r2_list = []
		m_r2_var_list = []
		m_K_list = []
		m_M_list = []
		m_TD_list = []
		m_S_list = []
		prop_no_var_list = []
		m_dist_bw_list = []


		# variance lists
		v_pi_list = []
		v_theta_list = []
		v_r2_list = []
		v_r2_var_list = []
		v_K_list = []
		v_M_list = []
		v_TD_list = []
		v_S_list = []
		v_dist_bw_list = []

		# Mean SFS output dictionary
		mean_sfs_dict = {}
		mean_fsfs_dict = {}

		SFS_dict_A = {}
		FSFS_dict_A = {}

		# Set the keys for SFS_dictA
		for i in range(0, nchr+1):
			SFS_dict_A[i] = []

		#Set the keys for FSFS_dictA
		for i in range(0, num_ind+1):
			FSFS_dict_A[i] = []

		FSFS_list = []
		SFS_list = []

		for rep in range(0, self.reps):	# Loop for evolutionary replicates

			if self.demography == None:
				#Simulate genealogy using the specified parameters in msprime. Replicates represent independent loci
				self.anc = msprime.sim_ancestry(samples = self.ind, sequence_length = self.length, recombination_rate = self.rec_rate_A, 
												ploidy = self.ploidy, num_replicates = self.loci, population_size = self.pop_size)
			else:
				self.anc = msprime.sim_ancestry(samples = self.ind, sequence_length = self.length, recombination_rate = self.rec_rate_A, 
													ploidy = self.ploidy, num_replicates = self.loci, demography = self.demography)


			# Create dictionaries to be populated by replicates 
			stats_dict_A = {"pi":[], "theta":[], "mean_r2":[], "var_r2":[], "K":[], "M":[], "Tajima_D":[], "S":[]} 
			

			#lists to populate the dictionary 
			pi_list = []
			theta_list = []
			mean_r2_list = []
			var_r2_list = []
			K_list = []
			M_list = []
			Tajima_list = []
			S_list = []
			dist_between_list = []


			# _______________________________________________________________________________________________________________________________ #

			counter = 0
			for ts in self.anc: # loop for every locus in the chromosome
				# Add mutations to the genalogy of the ith locus
				mut_ts = msprime.sim_mutations(ts, rate = self.mut_rate_A) 
				

				vcf=mut_ts.as_vcf() #export as vcf to make readable file for scikit allel (mimic real data)

				with open(self.parent_path+"/temp_vcf"+str(counter)+".vcf", "w") as f:
					f.write(vcf)

				data = allel.read_vcf(self.parent_path+"/temp_vcf"+str(counter)+".vcf")

				os.remove(self.parent_path+"/temp_vcf"+str(counter)+".vcf")

				counter += 1

				if data == None: #If no data, there are no variants in locus
					pi_list.append(0)
					theta_list.append(0)
					mean_r2_list.append(np.nan)
					var_r2_list.append(np.nan)
					K_list.append(1)
					M_list.append(1)
					Tajima_list.append(np.nan)
					S_list.append(0)
					dist_between_list.append(np.nan)
				else:
					#Formatting data  
					POS = data['variants/POS']
					gt = allel.GenotypeArray(data['calldata/GT'])
					ac = gt.count_alleles()

					## If POS = 0, there are no SNPs in that replicate, thus pi and theta are 0 and the other statistics are unable to be calculated
					if len(POS) == 0:
						pi_list.append(0)
						theta_list.append(0)
						mean_r2_list.append(np.nan)
						var_r2_list.append(np.nan)
						K_list.append(1)
						M_list.append(1)
						Tajima_list.append(np.nan)
						S_list.append(0)
						dist_between_list.append(np.nan)
					else:
						biallelic_check = ac.is_biallelic_01()[:]
						ac_biallelic = ac.compress(biallelic_check,  axis=0)[:, :2]
						gt_biallelic = gt.compress(biallelic_check, axis=0)
						POS_bial = POS[biallelic_check]

						#Remove non-segregating sites from biallelic markers 
						seg_sites = ac.is_segregating()
						bi_seg_sites=seg_sites[biallelic_check]
						ac_seg_bi = ac_biallelic.compress(bi_seg_sites, axis=0)
						gt_seg_bi = gt_biallelic.compress(bi_seg_sites, axis=0)
						POS_seg_bi = POS_bial[bi_seg_sites]
						gn_seg_bi = gt_seg_bi.to_n_alt()

						## If the only SNPs are multiallelic or non-segregating, they will be filtered out and will lead to the same result as above
						if len(POS_seg_bi) == 0: 
							pi_list.append(0)
							theta_list.append(0)
							mean_r2_list.append(np.nan)
							var_r2_list.append(np.nan)
							K_list.append(1)
							M_list.append(1)
							Tajima_list.append(np.nan)
							S_list.append(0)
							dist_between_list.append(np.nan)
						else:
							h = gt_seg_bi.to_haplotypes()
							dac_seg_bi = ac_seg_bi[:,1]

							#Calculate pi 
							pi, windows, n_bases, counts = allel.windowed_diversity(pos = POS_seg_bi, ac = ac_seg_bi, size = seq_length, start=1, stop=seq_length)
							pi_list.append(round(float(pi), 8))

							#Calculate theta 
							theta, windows, n_bases, counts = allel.windowed_watterson_theta(pos=POS_seg_bi, ac=ac_seg_bi, size=seq_length, start=1, stop=seq_length)
							theta_list.append(round(float(theta), 8))

							#Calculate Tajima's D
							D, windows, counts = allel.windowed_tajima_d(pos = POS_seg_bi, ac = ac_seg_bi, size= seq_length, start=1, stop=seq_length)
							Tajima_list.append(round(float(D), 8))

							#Number of segregating sites
							S = len(POS_seg_bi)
							S_list.append(S)

							#r squared calc
								#Remove singletons from gn and POS to get better estimation of r2
							f_alt = gn_seg_bi.sum(axis=1)
							gn_nosingle = np.array(f_alt != 1)
							gn_r2 = gn_seg_bi.compress(gn_nosingle, axis=0)
							POS_r2 = POS_seg_bi[gn_nosingle]
								#Further filter for r2 to remove any sites where all ind are heterozygous 
							to_remove = np.all(gn_r2==1, axis=1)
							gn_r2_final = gn_r2[~to_remove]
							POS_r2_final = POS_r2[~to_remove]

							#The r2 output requires a comparison between two SNPs, so if only one SNP remains after filtering singletons, correlations can't be found
							if len(POS_r2_final) <= 1:
								mean_r2_list.append(np.nan)
								var_r2_list.append(np.nan)
								dist_between_list.append(np.nan)

							else:
								#Create r2 array for whole locus
								r_squared = allel.rogers_huff_r(gn_r2_final) ** 2
								#Calc mean r2
								meanr2 = float(np.mean(r_squared))
								mean_r2_list.append(meanr2)
								#Calc variance in r2
								varr2 = float(np.var(r_squared))
								var_r2_list.append(varr2)

								#Calculate distance between SNPs
								mean_dist = []
								for idx in range(len(POS_r2_final)):
									if idx+1 == len(POS_r2_final):
										break
									else:
										diff = POS_r2_final[idx+1] - POS_r2_final[idx]
										mean_dist.append(diff)
													
								dist_between_list.append((sum(mean_dist)) / (len(mean_dist)))


							#Calculate K
							unique_haps = h.distinct_counts() 
							K=len(unique_haps)
							K_list.append(K)

							#Calculate M
							sum_haps = sum(unique_haps)
							freq_hap=max(unique_haps)
							M = freq_hap/sum_haps
							M_list.append(M)

							#Calculate Folded SFS 
							FSFS = allel.sfs_folded(ac_seg_bi, n=nchr)
							PropFSFS = []
							for val in FSFS: # making each count a proportion of total snps 
								PropFSFS.append(val / sum(FSFS))
							FSFS_list.append(PropFSFS)
							
							#Calculate Unfolded SFS 
							SFS = allel.sfs(dac_seg_bi, n = nchr)
							PropSFS = []
							for val in SFS: # making each count a proportion of total snps 
								PropSFS.append(val / sum(SFS))
							SFS_list.append(PropSFS)
					
			### Compile datasets 

			stats_dict_A["pi"] = pi_list
			stats_dict_A["theta"] = theta_list
			stats_dict_A["mean_r2"] = mean_r2_list
			stats_dict_A["var_r2"] = var_r2_list
			stats_dict_A["K"]= K_list
			stats_dict_A["M"] = M_list
			stats_dict_A["Tajima_D"] = Tajima_list
			stats_dict_A["S"] = S_list
			stats_dict_A["dist_bw_SNPs"] = dist_between_list

			num_no_var = 0
			for val in pi_list:
				if val == 0:
					num_no_var += 1

			prop_no_var_list.append(num_no_var/len(pi_list))


			#Convert the sum statsdictionary to a pandas df 
			dfA = pd.DataFrame(stats_dict_A)
			#Add means to mean lists
			m_pi_list.append(dfA.pi.mean())
			m_theta_list.append(dfA.theta.mean())
			m_r2_list.append(dfA.mean_r2.mean())
			m_r2_var_list.append(dfA.var_r2.mean())
			m_K_list.append(dfA.K.mean())
			m_M_list.append(dfA.M.mean())
			m_TD_list.append(dfA.Tajima_D.mean())
			m_S_list.append(dfA.S.mean())
			m_dist_bw_list.append(dfA.dist_bw_SNPs.mean())
			

			#Add variances to variance lists
			v_pi_list.append(dfA.pi.var())
			v_theta_list.append(dfA.pi.var())
			v_r2_list.append(dfA.mean_r2.var())
			v_r2_var_list.append(dfA.var_r2.var())
			v_K_list.append(dfA.K.var())
			v_M_list.append(dfA.M.var())
			v_TD_list.append(dfA.Tajima_D.var())
			v_S_list.append(dfA.S.var())
			v_dist_bw_list.append(dfA.dist_bw_SNPs.var())

			## Autosome site frequency spectra datasets ##  

			# Create intermediate dictionaries to collect each bin in its own list instead of each SFS in a list
			# ex {"1":[ALL SINGLETONS], "2":[ALL DOUBLETONS]} etc 
			SFS_bin_dict = {}
			for key in SFS_dict_A.keys():
				SFS_bin_dict[key] = []
			FSFS_bin_dict = {}
			for key in FSFS_dict_A.keys():
				FSFS_bin_dict[key] = []

			#Populate above dictionary
			for SFS in SFS_list:
				for i in range(len(SFS)):
					SFS_bin_dict[i].append(float(SFS[i])) 			
			for FSFS in FSFS_list:
				for i in range(len(FSFS)):
					FSFS_bin_dict[i].append(float(FSFS[i]))
					
			## Take the mean of each bin and output it to the correct bin in SFS/FSFS dict_A
			for key, bin_list in SFS_bin_dict.items():
				SFS_dict_A[key].append(statistics.mean(bin_list))

			for key, bin_list in FSFS_bin_dict.items():
				FSFS_dict_A[key].append(statistics.mean(bin_list))	

		## After loop above finishes, there should be nrow = reps for SFS_dict, FSFS_dict, mean_dictA, and var_dictA. Each row will be the mean statistic/spectrum for all loci in each individual replicate

		# _______________________________________________________________________________________________________________________________ #

		#Populate dictionary and create new data frame for mean and variances
		mean_dictA["mean_pi"] = m_pi_list
		mean_dictA["mean_theta"] = m_theta_list
		mean_dictA["mean_r2"] = m_r2_list
		mean_dictA["mean_r2_var"] = m_r2_var_list
		mean_dictA["mean_K"] = m_K_list
		mean_dictA["mean_M"] = m_M_list
		mean_dictA["mean_TD"] = m_TD_list
		mean_dictA["mean_S"] = m_S_list
		mean_dictA["mean_prop_no_var"] = prop_no_var_list
		mean_dictA["mean_dist_bw_SNPs"] = m_dist_bw_list
		

		mean_df = pd.DataFrame(mean_dictA)

		var_dictA["var_pi"] = v_pi_list
		var_dictA["var_theta"] = v_theta_list
		var_dictA["var_mr2"] = v_r2_list
		var_dictA["var_r2_var"] = v_r2_var_list
		var_dictA["var_K"] = v_K_list
		var_dictA["var_M"] = v_M_list
		var_dictA["var_TD"] = v_TD_list
		var_dictA["var_S"] = v_S_list
		var_dictA["var_dist_bw_SNPs"] = v_dist_bw_list
		

		var_df = pd.DataFrame(var_dictA)


		## Summarize mean and var df's to allow for immediate plotting 
		mean_out_dict = {}

		#Take mean of the means 
		for col in mean_df.columns:
			mean_out_dict[col] = [mean_df[col].mean()]

		## Add keys for upper and lower CI (97.5th quantile and 2.5th quantile) #ignoring the mean prop of windows with no variants 
		mean_out_dict["CI_upper_pi"] = [mean_df["mean_pi"].quantile(0.975)]
		mean_out_dict["CI_lower_pi"] = [mean_df["mean_pi"].quantile(0.025)]
		mean_out_dict["CI_upper_theta"] = [mean_df["mean_theta"].quantile(0.975)]
		mean_out_dict["CI_lower_theta"] = [mean_df["mean_theta"].quantile(0.025)]
		mean_out_dict["CI_upper_r2"] = [mean_df["mean_r2"].quantile(0.975)]
		mean_out_dict["CI_lower_r2"] = [mean_df["mean_r2"].quantile(0.025)]
		mean_out_dict["CI_upper_r2_var"] = [mean_df["mean_r2_var"].quantile(0.975)]
		mean_out_dict["CI_lower_r2_var"] = [mean_df["mean_r2_var"].quantile(0.025)]
		mean_out_dict["CI_upper_K"] = [mean_df["mean_K"].quantile(0.975)]
		mean_out_dict["CI_lower_K"] = [mean_df["mean_K"].quantile(0.025)]
		mean_out_dict["CI_upper_M"] = [mean_df["mean_M"].quantile(0.975)]
		mean_out_dict["CI_lower_M"] = [mean_df["mean_M"].quantile(0.025)]
		mean_out_dict["CI_upper_TD"] = [mean_df["mean_TD"].quantile(0.975)]
		mean_out_dict["CI_lower_TD"] = [mean_df["mean_TD"].quantile(0.025)]
		mean_out_dict["CI_upper_S"] = [mean_df["mean_S"].quantile(0.975)]
		mean_out_dict["CI_lower_S"] = [mean_df["mean_S"].quantile(0.025)]
		mean_out_dict["CI_upper_no_var"] = [mean_df["mean_prop_no_var"].quantile(0.975)]
		mean_out_dict["CI_lower_no_var"] = [mean_df["mean_prop_no_var"].quantile(0.025)]
		mean_out_dict["CI_upper_SNP_dist"] = [mean_df["mean_dist_bw_SNPs"].quantile(0.975)]
		mean_out_dict["CI_lower_SNP_dist"] = [mean_df["mean_dist_bw_SNPs"].quantile(0.025)]


		#Slap on the BSR at the end for ease of plotting 
		mean_out_dict["pf"] = [self.pf]

		#Create dataframe to summarize var_df
		var_out_dict = {}

		#Mean of variances
		for col in var_df.columns:
			var_out_dict[col] = [var_df[col].mean()]

		#Add standard error for each stat
		var_out_dict["CI_upper_pi"] = [var_df["var_pi"].quantile(0.975)]
		var_out_dict["CI_lower_pi"] = [var_df["var_pi"].quantile(0.025)]
		var_out_dict["CI_upper_theta"] = [var_df["var_theta"].quantile(0.975)]
		var_out_dict["CI_lower_theta"] = [var_df["var_theta"].quantile(0.025)]
		var_out_dict["CI_upper_r2"] = [var_df["var_mr2"].quantile(0.975)]
		var_out_dict["CI_lower_r2"] = [var_df["var_mr2"].quantile(0.025)]
		var_out_dict["CI_upper_r2_var"] = [var_df["var_r2_var"].quantile(0.975)]
		var_out_dict["CI_lower_r2_var"] = [var_df["var_r2_var"].quantile(0.025)]
		var_out_dict["CI_upper_K"] = [var_df["var_K"].quantile(0.975)]
		var_out_dict["CI_lower_K"] = [var_df["var_K"].quantile(0.025)]
		var_out_dict["CI_upper_M"] = [var_df["var_M"].quantile(0.975)]
		var_out_dict["CI_lower_M"] = [var_df["var_M"].quantile(0.025)]
		var_out_dict["CI_upper_TD"] = [var_df["var_TD"].quantile(0.975)]
		var_out_dict["CI_lower_TD"] = [var_df["var_TD"].quantile(0.025)]
		var_out_dict["CI_upper_S"] = [var_df["var_S"].quantile(0.975)]
		var_out_dict["CI_lower_S"] = [var_df["var_S"].quantile(0.025)]
		var_out_dict["CI_upper_SNP_dist"] = [var_df["var_dist_bw_SNPs"].quantile(0.975)]
		var_out_dict["CI_lower_SNP_dist"] = [var_df["var_dist_bw_SNPs"].quantile(0.025)]

		#Slap on the BSR at the end for ease of plotting 
		var_out_dict["pf"] = [self.pf]

		mean_out_df = pd.DataFrame(mean_out_dict)
		var_out_df = pd.DataFrame(var_out_dict)

		# include runcodes for the simulation to keep track when combining
		mean_out_df["Run_Code"] = [self.prefix]
		var_out_df["Run_Code"] = [self.prefix]

		## Output summaries

		if self.prefix == None:
			mean_out_df.to_csv(self.parent_path+"/Autosome_summarized_mean_sum_stats_pf"+self.pf_out+".csv")
			var_out_df.to_csv(self.parent_path+"/Autosome_summarized_variance_sum_stats_pf"+self.pf_out+".csv")
		else:
			mean_out_df.to_csv(self.parent_path+"/A"+self.prefix+"_summarized_mean_sum_stats_pf"+self.pf_out+".csv")
			var_out_df.to_csv(self.parent_path+"/A"+self.prefix+"_summarized_variance_sum_stats_pf"+self.pf_out+".csv")

		# _______________________________________________________________________________________________________________________________ #

		# Compile SFS and FSFS 
		sfs_df = pd.DataFrame(SFS_dict_A)
		fsfs_df = pd.DataFrame(FSFS_dict_A)


		# Assemble a summarized mean SFS and FSFS for plotting 

		#SFS
		bins = []
		count = 0
		for i in range(0,nchr+1):
			bins.append(count)
			count+=1

		mean_sfs_dict = {"bins":bins, "Mean_prop":[], "CI_upper":[], "CI_lower":[], "Run_Code":[]}

		for col in sfs_df.columns:
			mean_sfs_dict["Mean_prop"].append(sfs_df[col].mean())
			mean_sfs_dict["CI_upper"].append(sfs_df[col].quantile(0.975))
			mean_sfs_dict["CI_lower"].append(sfs_df[col].quantile(0.025))
			mean_sfs_dict["Run_Code"].append(self.prefix)  # attach run code to end of dataframe 


		#FSFS
		bins = []
		count = 0
		for i in range(0,num_ind+1):
			bins.append(count)
			count+=1

		mean_fsfs_dict = {"bins":bins, "Mean_prop":[], "CI_upper":[], "CI_lower":[], "Run_Code":[]}

		for col in fsfs_df.columns:
			mean_fsfs_dict["Mean_prop"].append(sfs_df[col].mean())
			mean_fsfs_dict["CI_upper"].append(sfs_df[col].quantile(0.975))
			mean_fsfs_dict["CI_lower"].append(sfs_df[col].quantile(0.025))
			mean_fsfs_dict["Run_Code"].append(self.prefix) # attach run code to end of dataframe

		# write the summaries
		mean_sfs_df = pd.DataFrame(mean_sfs_dict)
		mean_fsfs_df = pd.DataFrame(mean_fsfs_dict)

		if self.prefix == None:
			mean_sfs_df.to_csv(self.parent_path+"/Autosome_summarized_mean_sfs_pf"+self.pf_out+".csv")
			mean_fsfs_df.to_csv(self.parent_path+"/Autosome_summarized_mean_fsfs_pf"+self.pf_out+".csv")
		else:
			mean_sfs_df.to_csv(self.parent_path+"/A"+self.prefix+"_summarized_mean_sfs_pf"+self.pf_out+".csv")
			mean_fsfs_df.to_csv(self.parent_path+"/A"+self.prefix+"_summarized_mean_fsfs_pf"+self.pf_out+".csv")







## /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ ##







class X_chr:
	"""Parameters:
	________________
	ind: number of individuals to sample
	rec_rate_f: female-specific per-site recombination rate (will be scaled with changing pf)
	mut_rate_A: autosomal per-site mutation rate (will differ from autosomal value if alpha does not equal 1)
	length: sequence length of simulated segment
	pf: proportion of breeding individuals that are female
	pop_size: effective population size of simulated population – must equal autosomal entry for proper comparison
	alpha: ratio of male per-site mutation rate to female per-site mutation rate (defaults to 1)
	demography: msprime demography object for the desired population. Must include initial_sizes representing the Ne of that population size
	pf_out: proportion of females expressed as a string, replacing the period with an underscore (eg. "0_5" instead of 0.5)
	_________________
	Note: please include 0 when setting pf (example: use 0.5 instead of .5)
	If running simualtions for populations with demograhpy object, the pop_size command will be ignored

	"""
	def __init__(self, ind=10, rec_rate_f=None, mut_rate_A=None, length=None, pf=0.5, pop_size=1, alpha = 1, demography=None):
		self.ind = ind
		self.ploidy = 2
		self.length = length
		self.pf = pf
		self.alpha = alpha
		self.demography = copy.deepcopy(demography)
		self.parent_path = os.getcwd()


		x_var = (9 * pf * (1-pf))/(2 * (2-pf)) #adjust parameters based on the proportion of females in the population 
		alp_num = 2 * (2+alpha)
		alp_den = 3 * (1+alpha)
		alp_eq = alp_num/alp_den # allows for differences in mutation rate between sexes 

		if self.demography == None:	
			self.pop_size = x_var * pop_size
		else:
			for pop in self.demography.values():
				pop.initial_size *= x_var
			for event in self.demography.events:
				if event.initial_size == None:
					continue
				event.initial_size *= x_var

		self.rec_rate_X = (2*pf)/(1+pf) * rec_rate_f #scaling recombination rate down for all chr based on pf 
		self.mut_rate_X = mut_rate_A * alp_eq #scales mutation rate accounting for differing rates among males and females


		print("X chromosome parameters:")
		print("Mutation rate: ", self.mut_rate_X)
		print("Recombination rate: ", self.rec_rate_X)
		if self.demography == None:
			print("Effective Population Size: ", self.pop_size, "\n")
		else:
			print(self.demography, "\n")



		## Make output data dictonary
		mean_dictX = {"mean_pi":[], "mean_theta":[], "mean_r2":[], "mean_r2_var":[], "mean_K":[], "mean_M":[], "mean_TD":[], "mean_S":[]}
		var_dictX = {"var_pi":[], "var_theta":[], "var_mr2":[], "var_r2_var":[], "var_K":[], "var_M":[],"var_TD":[] ,"var_S":[]}

		#lists to populate the dictionary 
		m_pi_list = []
		m_theta_list = []
		m_r2_list = []
		m_r2_var_list = []
		m_K_list = []
		m_M_list = []
		m_TD_list = []
		m_S_list = []
		prop_no_var_list = []
		m_dist_bw_list = []

		v_pi_list = []
		v_theta_list = []
		v_r2_list = []
		v_r2_var_list = []
		v_K_list = []
		v_M_list = []
		v_TD_list = []
		v_S_list = []
		v_dist_bw_list= []

		# Mean SFS
		mean_sfs_dict = {}
		mean_fsfs_dict = {}

		# Dictionaries to be populated at replicate level
		SFS_dict_X = {}
		FSFS_dict_X = {}

		# Set the keys for SFS_dictX
		for i in range(0, nchr+1):
			SFS_dict_X[i] = []

		#Set the keys for FSFS_dictX
		for i in range(0, num_ind+1):
			FSFS_dict_X[i] = []

		FSFS_list = []
		SFS_list = []


		for rep in range(0, self.reps):	# Loop for chromosomal replicates

			# Generate genealogies, each replicate is one independent X-linked locus
			if self.demography == None:
				self.anc = msprime.sim_ancestry(samples = self.ind, sequence_length = self.length, recombination_rate = self.rec_rate_X, 
												ploidy = self.ploidy, num_replicates = self.loci, population_size = self.pop_size)
			else:
				self.anc = msprime.sim_ancestry(samples = self.ind, sequence_length = self.length, recombination_rate = self.rec_rate_X, 
													ploidy = self.ploidy, num_replicates = self.loci, demography = self.demography)


			# Create dictionaries to be populated by replicates 
			stats_dict_X = {"pi":[], "theta":[], "mean_r2":[], "var_r2":[], "K":[], "M":[], "Tajima_D":[], "S":[]} 
			

			#lists to populate the dictionary 
			pi_list = []
			theta_list = []
			mean_r2_list = []
			var_r2_list = []
			K_list = []
			M_list = []
			Tajima_list = []
			S_list = []
			dist_between_list = []


			# _______________________________________________________________________________________________________________________________ #

			counter = 0
			for ts in self.anc: # loop for every locus in the chromosome

				#Add mutations to the ith locus's genealogy 
				mut_ts = msprime.sim_mutations(ts, rate = self.mut_rate_X)
				

				vcf=mut_ts.as_vcf()

				with open(self.parent_path+"/temp_vcf"+str(counter)+".vcf", "w") as f:
					f.write(vcf)

				data = allel.read_vcf(self.parent_path+"/temp_vcf"+str(counter)+".vcf")

				os.remove(self.parent_path+"/temp_vcf"+str(counter)+".vcf")

				counter += 1

				#Filter out scenarios that prevent cacluation of summary statistics 
				if data == None:
					pi_list.append(0)
					theta_list.append(0)
					mean_r2_list.append(np.nan)
					var_r2_list.append(np.nan)
					K_list.append(1)
					M_list.append(1)
					Tajima_list.append(np.nan)
					S_list.append(0)
					dist_between_list.append(np.nan)
				else:
					#Formatting data  
					POS = data['variants/POS']
					gt = allel.GenotypeArray(data['calldata/GT'])
					ac = gt.count_alleles()

					## If POS = 0, there are no SNPs in that replicate, thus pi and theta are 0 and the other statistics are unable to be calculated
					if len(POS) == 0:
						pi_list.append(0)
						theta_list.append(0)
						mean_r2_list.append(np.nan)
						var_r2_list.append(np.nan)
						K_list.append(1)
						M_list.append(1)
						Tajima_list.append(np.nan)
						S_list.append(0)
						dist_between_list.append(np.nan)
					else:
						biallelic_check = ac.is_biallelic_01()[:]
						ac_biallelic = ac.compress(biallelic_check,  axis=0)[:, :2]
						gt_biallelic = gt.compress(biallelic_check, axis=0)
						POS_bial = POS[biallelic_check]

						#Remove non-segregating sites from biallelic markers 
						seg_sites = ac.is_segregating()
						bi_seg_sites=seg_sites[biallelic_check]
						ac_seg_bi = ac_biallelic.compress(bi_seg_sites, axis=0)
						gt_seg_bi = gt_biallelic.compress(bi_seg_sites, axis=0)
						POS_seg_bi = POS_bial[bi_seg_sites]
						gn_seg_bi = gt_seg_bi.to_n_alt()

						## If the only SNPs are multiallelic or non-segregating, they will be filtered out and will lead to the same result as above
						if len(POS_seg_bi) == 0: 
							pi_list.append(0)
							theta_list.append(0)
							mean_r2_list.append(np.nan)
							var_r2_list.append(np.nan)
							K_list.append(1)
							M_list.append(1)
							Tajima_list.append(np.nan)
							S_list.append(0)
							dist_between_list.append(np.nan)
						else:
							h = gt_seg_bi.to_haplotypes()
							dac_seg_bi = ac_seg_bi[:,1]

							#Calculate pi 
							pi, windows, n_bases, counts = allel.windowed_diversity(pos = POS_seg_bi, ac = ac_seg_bi, size = seq_length, start=1, stop=seq_length)
							pi_list.append(round(float(pi), 8))

							#Calculate theta 
							theta, windows, n_bases, counts = allel.windowed_watterson_theta(pos=POS_seg_bi, ac=ac_seg_bi, size=seq_length, start=1, stop=seq_length)
							theta_list.append(round(float(theta), 8))

							#Calculate Tajima's D
							D, windows, counts = allel.windowed_tajima_d(pos = POS_seg_bi, ac = ac_seg_bi, size= seq_length, start=1, stop=seq_length)
							Tajima_list.append(round(float(D), 8))

							#Number of segregating sites
							S = len(POS_seg_bi)
							S_list.append(S)

							#r squared calc
								#Remove singletons from gn and POS to get better estimation of r2
							f_alt = gn_seg_bi.sum(axis=1)
							gn_nosingle = np.array(f_alt != 1)
							gn_r2 = gn_seg_bi.compress(gn_nosingle, axis=0)
							POS_r2 = POS_seg_bi[gn_nosingle]
								#Further filter for r2 to remove any sites where all ind are heterozygous 
							to_remove = np.all(gn_r2==1, axis=1)
							gn_r2_final = gn_r2[~to_remove]
							POS_r2_final = POS_r2[~to_remove]

							#The r2 output requires a comparison between two SNPs, so if only one SNP remains after filtering singletons, correlations can't be found
							if len(POS_r2_final) <= 1:
								mean_r2_list.append(np.nan)
								var_r2_list.append(np.nan)
								dist_between_list.append(np.nan)
							else:
								#Create r2 array for whole locus
								r_squared = allel.rogers_huff_r(gn_r2_final) ** 2
								#Calc mean r2
								meanr2 = float(np.mean(r_squared))
								mean_r2_list.append(meanr2)
								#Calc variance in r2
								varr2 = float(np.var(r_squared))
								var_r2_list.append(varr2)

								#Calculate distance between SNPs
								mean_dist = []
								for idx in range(len(POS_r2_final)):
									if idx+1 == len(POS_r2_final):
										break
									else:
										diff = POS_r2_final[idx+1] - POS_r2_final[idx]
										mean_dist.append(diff)
													
								dist_between_list.append((sum(mean_dist)) / (len(mean_dist)))

							#Calculate K
							unique_haps = h.distinct_counts() 
							K=len(unique_haps)
							K_list.append(K)

							#Calculate M
							sum_haps = sum(unique_haps)
							freq_hap=max(unique_haps)
							M = freq_hap/sum_haps
							M_list.append(M)

							#Calculate Folded SFS 
							FSFS = allel.sfs_folded(ac_seg_bi, n=num_ind*2)
							PropFSFS = []
							for val in FSFS: # making each count a proportion of total snps 
								PropFSFS.append(val / sum(FSFS))
							FSFS_list.append(PropFSFS)

							#Calculate Unfolded SFS 
							SFS = allel.sfs(dac_seg_bi, n = num_ind*2)
							PropSFS = []
							for val in SFS: # making each count a proportion of total snps 
								PropSFS.append(val / sum(SFS))
							SFS_list.append(PropSFS)

			# __________________________________________________________________________________________________________ # 

			### Compile datasets 

			stats_dict_X["pi"] = pi_list
			stats_dict_X["theta"] = theta_list
			stats_dict_X["mean_r2"] = mean_r2_list
			stats_dict_X["var_r2"] = var_r2_list
			stats_dict_X["K"]= K_list
			stats_dict_X["M"] = M_list
			stats_dict_X["Tajima_D"] = Tajima_list
			stats_dict_X["S"] = S_list
			stats_dict_X["dist_bw_SNPs"] = dist_between_list

			num_no_var = 0
			for val in pi_list:
				if val == 0:
					num_no_var += 1

			prop_no_var_list.append(num_no_var/len(pi_list))

			#Convert the dictionary to a pandas df 
			dfX = pd.DataFrame(stats_dict_X)
			#Add means to mean lists
			m_pi_list.append(dfX.pi.mean())
			m_theta_list.append(dfX.theta.mean())
			m_r2_list.append(dfX.mean_r2.mean())
			m_r2_var_list.append(dfX.var_r2.mean())
			m_K_list.append(dfX.K.mean())
			m_M_list.append(dfX.M.mean())
			m_TD_list.append(dfX.Tajima_D.mean())
			m_S_list.append(dfX.S.mean())
			m_dist_bw_list.append(dfX.dist_bw_SNPs.mean())

			#Add variances to variance lists
			v_pi_list.append(dfX.pi.var())
			v_theta_list.append(dfX.pi.var())
			v_r2_list.append(dfX.mean_r2.var())
			v_r2_var_list.append(dfX.var_r2.var())
			v_K_list.append(dfX.K.var())
			v_M_list.append(dfX.M.var())
			v_TD_list.append(dfX.Tajima_D.var())
			v_S_list.append(dfX.S.var())
			v_dist_bw_list.append(dfX.dist_bw_SNPs.var())

			## Site frequency spectra datasets ##

			# Create intermediate dictionaries to collect each bin in its own list instead of each SFS in a list
			# ex {"1":[ALL SINGLETONS], "2":[ALL DOUBLETONS]} etc 
			SFS_bin_dict = {}
			for key in SFS_dict_X.keys():
				SFS_bin_dict[key] = []
			FSFS_bin_dict = {}
			for key in FSFS_dict_X.keys():
				FSFS_bin_dict[key] = []

			#Populate above dictionary
			for SFS in SFS_list:
				for i in range(len(SFS)):
					SFS_bin_dict[i].append(float(SFS[i])) 			
			for FSFS in FSFS_list:
				for i in range(len(FSFS)):
					FSFS_bin_dict[i].append(float(FSFS[i]))

		
			## Take the mean of each bin and output it to the correct bin in SFS/FSFS dict_X
			for key, bin_list in SFS_bin_dict.items():
				SFS_dict_X[key].append(statistics.mean(bin_list))

			for key, bin_list in FSFS_bin_dict.items():
				FSFS_dict_X[key].append(statistics.mean(bin_list))	

		## After loop above finishes, there should be nrow = reps for SFS_dict, FSFS_dict, mean_dictX, and var_dictX. Each row will be the mean statistic/spectrum for all loci in each individual replicate
		# Problem: only one line in SFS and FSFS mean dataset

		# _______________________________________________________________________________________________________________________________ #

		#Populate dictionary and create new data frame for mean and variances
		mean_dictX["mean_pi"] = m_pi_list
		mean_dictX["mean_theta"] = m_theta_list
		mean_dictX["mean_r2"] = m_r2_list
		mean_dictX["mean_r2_var"] = m_r2_var_list
		mean_dictX["mean_K"] = m_K_list
		mean_dictX["mean_M"] = m_M_list
		mean_dictX["mean_TD"] = m_TD_list
		mean_dictX["mean_S"] = m_S_list
		mean_dictX["mean_prop_no_var"] = prop_no_var_list
		mean_dictX["mean_dist_bw_SNPs"] =  m_dist_bw_list


		mean_df = pd.DataFrame(mean_dictX)

		var_dictX["var_pi"] = v_pi_list
		var_dictX["var_theta"] = v_theta_list
		var_dictX["var_mr2"] = v_r2_list
		var_dictX["var_r2_var"] = v_r2_var_list
		var_dictX["var_K"] = v_K_list
		var_dictX["var_M"] = v_M_list
		var_dictX["var_TD"] = v_TD_list
		var_dictX["var_S"] = v_S_list
		var_dictX["var_dist_bw_SNPs"] = v_dist_bw_list

		var_df = pd.DataFrame(var_dictX)

		## Summarize mean and var df's to allow for immediate plotting 

		# Create dataframe to summarize mean_df 
		mean_out_dict = {}

		for col in mean_df.columns:
			mean_out_dict[col] = [mean_df[col].mean()]

		## Add columns for standard error (instead of this extract the 97.5th and 2.5th quantile)
		mean_out_dict["CI_upper_pi"] = [mean_df["mean_pi"].quantile(0.975)]
		mean_out_dict["CI_lower_pi"] = [mean_df["mean_pi"].quantile(0.025)]
		mean_out_dict["CI_upper_theta"] = [mean_df["mean_theta"].quantile(0.975)]
		mean_out_dict["CI_lower_theta"] = [mean_df["mean_theta"].quantile(0.025)]
		mean_out_dict["CI_upper_r2"] = [mean_df["mean_r2"].quantile(0.975)]
		mean_out_dict["CI_lower_r2"] = [mean_df["mean_r2"].quantile(0.025)]
		mean_out_dict["CI_upper_r2_var"] = [mean_df["mean_r2_var"].quantile(0.975)]
		mean_out_dict["CI_lower_r2_var"] = [mean_df["mean_r2_var"].quantile(0.025)]
		mean_out_dict["CI_upper_K"] = [mean_df["mean_K"].quantile(0.975)]
		mean_out_dict["CI_lower_K"] = [mean_df["mean_K"].quantile(0.025)]
		mean_out_dict["CI_upper_M"] = [mean_df["mean_M"].quantile(0.975)]
		mean_out_dict["CI_lower_M"] = [mean_df["mean_M"].quantile(0.025)]
		mean_out_dict["CI_upper_TD"] = [mean_df["mean_TD"].quantile(0.975)]
		mean_out_dict["CI_lower_TD"] = [mean_df["mean_TD"].quantile(0.025)]
		mean_out_dict["CI_upper_S"] = [mean_df["mean_S"].quantile(0.975)]
		mean_out_dict["CI_lower_S"] = [mean_df["mean_S"].quantile(0.025)]
		mean_out_dict["CI_upper_no_var"] = [mean_df["mean_prop_no_var"].quantile(0.975)]
		mean_out_dict["CI_lower_no_var"] = [mean_df["mean_prop_no_var"].quantile(0.025)]
		mean_out_dict["CI_upper_SNP_dist"] = [mean_df["mean_dist_bw_SNPs"].quantile(0.975)]
		mean_out_dict["CI_lower_SNP_dist"] = [mean_df["mean_dist_bw_SNPs"].quantile(0.025)]

		#Slap on the BSR at the end for ease of plotting 
		mean_out_dict["pf"] = [self.pf]

		#Create dataframe to summarize var_df
		var_out_dict = {}

		#Mean of variances
		for col in var_df.columns:
			var_out_dict[col] = [var_df[col].mean()]

		#Add standard error for each stat
		var_out_dict["CI_upper_pi"] = [var_df["var_pi"].quantile(0.975)]
		var_out_dict["CI_lower_pi"] = [var_df["var_pi"].quantile(0.025)]
		var_out_dict["CI_upper_theta"] = [var_df["var_theta"].quantile(0.975)]
		var_out_dict["CI_lower_theta"] = [var_df["var_theta"].quantile(0.025)]
		var_out_dict["CI_upper_r2"] = [var_df["var_mr2"].quantile(0.975)]
		var_out_dict["CI_lower_r2"] = [var_df["var_mr2"].quantile(0.025)]
		var_out_dict["CI_upper_r2_var"] = [var_df["var_r2_var"].quantile(0.975)]
		var_out_dict["CI_lower_r2_var"] = [var_df["var_r2_var"].quantile(0.025)]
		var_out_dict["CI_upper_K"] = [var_df["var_K"].quantile(0.975)]
		var_out_dict["CI_lower_K"] = [var_df["var_K"].quantile(0.025)]
		var_out_dict["CI_upper_M"] = [var_df["var_M"].quantile(0.975)]
		var_out_dict["CI_lower_M"] = [var_df["var_M"].quantile(0.025)]
		var_out_dict["CI_upper_TD"] = [var_df["var_TD"].quantile(0.975)]
		var_out_dict["CI_lower_TD"] = [var_df["var_TD"].quantile(0.025)]
		var_out_dict["CI_upper_S"] = [var_df["var_S"].quantile(0.975)]
		var_out_dict["CI_lower_S"] = [var_df["var_S"].quantile(0.025)]
		var_out_dict["CI_upper_SNP_dist"] = [var_df["var_dist_bw_SNPs"].quantile(0.975)]
		var_out_dict["CI_lower_SNP_dist"] = [var_df["var_dist_bw_SNPs"].quantile(0.025)]

		#Slap on the BSR at the end for ease of plotting 
		var_out_dict["pf"] = [self.pf]

		## Output summaries
		mean_out_df = pd.DataFrame(mean_out_dict)
		var_out_df = pd.DataFrame(var_out_dict)

		mean_out_df["Run_Code"] = [self.prefix]
		var_out_df["Run_Code"] = [self.prefix]

		if self.prefix == None:
			mean_out_df.to_csv(self.parent_path+"/X_chr_summarized_mean_sum_stats_pf"+self.pf_out+".csv")
			var_out_df.to_csv(self.parent_path+"/X_chr_summarized_variance_sum_stats_pf"+self.pf_out+".csv")
		else:
			mean_out_df.to_csv(self.parent_path+"/X"+self.prefix+"_summarized_mean_sum_stats_pf"+self.pf_out+".csv")
			var_out_df.to_csv(self.parent_path+"/X"+self.prefix+"_summarized_variance_sum_stats_pf"+self.pf_out+".csv")

		# _______________________________________________________________________________________________________________________________ #

		# Compile SFS and FSFS 
		sfs_df = pd.DataFrame(SFS_dict_X)
		fsfs_df = pd.DataFrame(FSFS_dict_X)

		# Assemble a big mean SFS and FSFS for plotting 

		#SFS
		bins = []
		count = 0
		for i in range(0,nchr+1):
			bins.append(count)
			count+=1

		mean_sfs_dict = {"bins":bins, "Mean_prop":[], "CI_upper":[], "CI_lower":[], "Run_Code":[]}

		for col in sfs_df.columns:
			mean_sfs_dict["Mean_prop"].append(sfs_df[col].mean())
			mean_sfs_dict["CI_upper"].append(sfs_df[col].quantile(0.975))
			mean_sfs_dict["CI_lower"].append(sfs_df[col].quantile(0.025))
			mean_sfs_dict["Run_Code"].append(self.prefix)


		#FSFS
		bins = []
		count = 0
		for i in range(0,num_ind+1):
			bins.append(count)
			count+=1

		mean_fsfs_dict = {"bins":bins, "Mean_prop":[], "CI_upper":[], "CI_lower":[], "Run_Code":[]}

		for col in fsfs_df.columns:
			mean_fsfs_dict["Mean_prop"].append(sfs_df[col].mean())
			mean_fsfs_dict["CI_upper"].append(sfs_df[col].quantile(0.975))
			mean_fsfs_dict["CI_lower"].append(sfs_df[col].quantile(0.025))
			mean_fsfs_dict["Run_Code"].append(self.prefix)

		# write the summaries
		mean_sfs_df = pd.DataFrame(mean_sfs_dict)
		mean_fsfs_df = pd.DataFrame(mean_fsfs_dict)

		if self.prefix == None:
			mean_sfs_df.to_csv(self.parent_path+"/X_chr_summarized_mean_sfs_pf"+self.pf_out+".csv")
			mean_fsfs_df.to_csv(self.parent_path+"X_chr_summarized_mean_fsfs_pf"+self.pf_out+".csv")
		else:
			mean_sfs_df.to_csv(self.parent_path+"/X"+self.prefix+"_summarized_mean_sfs_pf"+self.pf_out+".csv")
			mean_fsfs_df.to_csv(self.parent_path+"/X"+self.prefix+"_summarized_mean_fsfs_pf"+self.pf_out+".csv")











