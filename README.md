# BSR Simulations 

Here, we outline the process in which coalescent simulatins were used to simulate the X-linked and autosomal loci under the combined presence of a non-constant demographic history and a biased breeding sex ratio (BSR). This process was completed in a high throughput manner via the University of Wisconsin-Madison's Center for High Throughput Computing (CHTC). While CHTC was required to simulate every scenario of interest quickly, this file will describe how to utilize these scripts for individual examples.

## Software Package Requirements

These packages can be found in the simulation_env conda environment located in the packages folder, which includes all underlying dependencies and was utilized in all simulations we preformed.

Indivdual packages are listed here:
- msprime (version 1.2.0)
- scikit-allel (version 1.3.6)

## 1. Creating Autosome and X Chromosome Classes

The simulation process begins using the python script __HTSimulate.py__. This script contains two classes: __Autosome__ and __X_Chr__. In this framework, X chromosome and autosome simulations are completed independently. Each class follows the same processs to output files summarizing patterns of variation of simulated loci, but makes unique adjustments to account for the ways in which evolutionary processes affect the X and autosomes. 

Each class is intialized by specifing parameters required to perform coalescent simulations using _msprime_. This includes the number of sampled individuals, the length of the simulated sequence, the per-site, per-generation mutation and recombination rates, the effective population size, and any demography object (see [msprime help](https://tskit.dev/msprime/docs/latest/demography.html)). Because sex differences in mutation rate can affect the X chromosome, but not autosomes (see Miyata et al. 1987), there is an additional option to provide alpha (male mutation rate/female mutation rate) for the X_Chr class. Additonally, there is a requirement to specific the proportion of females in the breeding population (pf), which will act as the means of adjusting each chromosome class based on the BSR. Once specified, each class will automatically adjust the effective population size and mutation/recombination rates according to previously derived equations for the X chromosome and autosomes. 

## 2. Simulating Independent Loci 

To perform simulations, we sought to replicate genomic data by grouping together independent loci for both the X and the autosomes. To generate evolutionary replicates of these independent loci, we constructed nested loops in each class. The inner loop begins with the generation of genealogies for each independent locus (we simulated 1000 for both the X and autosomes in our study at 10Kb in length). Using the `sim_ancestry` command in _msprime_, we create a generator object that contains the genealogy for every locus. We then iterate through each locus and perform the following steps:

- Add mutations to the genealogy using `add_mutations` in _msprime_
- Compile the variants into a Variant Call Format (VCF) 
- Calculate summary statistics (see below for more info)
- Store values of summary statistics in a list
- Repeat with next genealogy for next locus 

After completing these steps for all loci, there will be a list containing a distribution of every summary statistic. We sought to mimic genomic data further by calculating the mean and variance of each distriubtion for each genomic compartment. These means and variances were stored in dictionaries and were the result of one evolutionary replicate. The whole process is then repeated with a new generator of genealogies. In our study, we included 100 replicates in our simulations for a total of 100,000 genealogies for the X chromosome and Autosomes. 

### Summarizing Patterns of Variation

After completing all evolutionary replicates, we have constructed a new distribution of mean and variances for the X chromosome and autosomes (length = 100 in our study). To summarize these distributions, we calculated the mean value of each, along with a 95% CI comprised of the 2.5th and 97.5th quantile of each. These values are then compiled into a dataframe along with metadata about the parameters used in the simualtion and output as a CSV. These values are what we report in our study, and capture the stochasticity of evolutionary processess on the patterns we observe. 

### Calculating summary statistics 

We used [_scikit-allel_](https://scikit-allel.readthedocs.io/en/stable/stats.html) for all summary statistic calculation. To prevent the code from crashing, we include a series of filtering steps that use the framework of this package to remove troublesome features of the simulations. If after any of these filtering steps there are no more variants in the VCF, we end that loucs's run and output summary statsitcs that reflect a region with no variants. 

After filtering the simulated data, we seek to calculate a series of summary statistics that cover a wide range of genomic patterns of variation. The summary statistics we calculate include:

- Nucleotide diversity ('\pi')
- Watterson's '\theta'
- Tajima's D
- Number of unique haplotypes
- Frequency of the most common haplotype 
- $'r^2'$

Each of these statsitics were calculated across the entire 10kb locus and were summarized as described in __3__. If there were no SNPs in a given locus, we were unable to calculate $'r^2'$ or Tajima's D, but these loci would return values of 0 for both diversity statistics and 1 for the haplotype statstics (No variation leads to no diversity and one haplotype). 

We also calculate the unfolded site frequency spectrum (SFS), which utilizes the known ancestral and derived allele states from the simulated data, as each mutation creates a new derived state. 


## 3. Running the Simulations

To run the process described above, we created another script aptly named __running_HTSimulate.py__. This script can be called from the command line, where each parameter of interest may be called. These parameters include:

- mutation rate (default 5e-9)
- recombination rate (default 5e-9)
- effective population size (default 10000)
- alpha (male:female mutation rate; default 1)
- demographic history 
- prefix

By default, this script will simulate the full range of BSRs from 0.1-0.9 in 0.05 increments. The prefix is required to be included in the command line call as it will be used for naming the file, and should reflect the paramters used in the simulation. For the demographic history, we created 35 unique demography objects featuring bottlenecks and population expansions. To use one of these demographic histories, the command line argument is just the integer associated with it. To make this a little more clear, take this example call of running_HTSimulate:

`python running_HTSimulate.py --rec_rate 5e-8 --mut_rate 5e-8 --alpha 1 --demography 3 --prefix 'BSRL_a1_r5e-8_m5e-8'` 

This simulation run features a mutation and recombination rate equal to 5e-8, does not include a male biased mutation rate, and incorporates a 95% reduction bottleneck recovering in size 500 generations ago, lasting 1000 generations (BSRL standing for "Bottleneck", "Strong", "Recent" and "Long" - the third bottleneck listed in the script). Calling this line of code will lead to the creation of many new CSVs with the same prefix, except for the last few characters where the BSR is included (ex. BSRL_a1_r5e-8_m5e-8_0_1.csv indicates a pf = 0.1). 

To compile the output scripts into one, and include all metadata for ease of comparison, we include two R scripts: __Add_Metdata.R__ and __Processing_HTSim_Outputs.R__. First, __Processsing_HTSim_Outputs.R__ will pull together all BSRs for the specified prefixes to make one dataset for the means and variances. After these datasets are created, __Add_Metadata.R__ takes the prefixes of each scenario to add the metadata to each row (simulation run). 


### High Throughput Application

We took the approach described above to allow for high throughput computation through UW-Madison's Center for High Throughput Computing (CHTC), which utilizes HTCondor for parallelization. To generate the required commands for __running_HTSimulate.py__, we used __creating_args.py__ to generate a text file for all the required parameter combinations we were interested in investigating. This combination of parameters includes two mutation and recombination rates (5e-8 and 5e-9), two alpha values (1 and 3), and all demographic histories included in __running_HTSimulate.py__. After completing all simulations, we compiled on large dataset for the means and variances the statistics. 








