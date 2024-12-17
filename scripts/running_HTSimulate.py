import HTSimulate 
import argparse
import msprime

parser = argparse.ArgumentParser()
parser.add_argument("--rec_rate", type=float, help="Recombination rate input into simulations. Default = 5e-9")
parser.add_argument("--mut_rate", type=float, help='Mutation rate input into simulations. Default = 5e-9')
parser.add_argument("--pop_size", type=int, help = "Effective population size of the simulated population. Ignored if demography is specified. Default = 10,000")
parser.add_argument("--alpha", type = float, help="Male mutation rate / female mutation rate. Default = 1")
parser.add_argument("--demography", type=int, help="*REQUIRED* Specify the demography object to use for simulations [1-12] (both inclusive), enter 0 for None")
parser.add_argument("--prefix", type=str, help="*REQUIRED* Prefix to be included in output file names.")
parser.add_argument("--rec_rate_X", type=float, help="Recombination rate for the X chromosome in females. If not specified, input rec_rate_X = rec_rate_A")

args = parser.parse_args()

## /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ##

## Compile arguments to be passed to all simulations (Conditional statments are used to establish a default for paramters that don't need to be specified to run)

##Required arguments [2] - Must Specify! 
prefix = args.prefix
#!!! demography: one of [0-26]

# Fixed Variables [4]
ind = 10
length = 10000
reps = 100
loci = 1000


## Optional Variables with Defaults [5]

if args.rec_rate != None:
	rec_rate = args.rec_rate
else:
	rec_rate = 5e-9

if args.rec_rate_X == None:
	rec_rate_X = rec_rate
else:
	rec_rate_X = args.rec_rate_X

if args.mut_rate != None:
	mut_rate = args.mut_rate
else:
	mut_rate = 5e-9

if args.alpha == None:
	alpha = 1
else:
	alpha = args.alpha

if args.demography == 0 or args.demography == None:
	if args.pop_size != None:
		size = args.pop_size
	else:
		size = 10000
else: size = None

# Based on input demography (0-12) create the relevent demography object and store it in demo to be used for simulations 

# Demography objects cover a full range 
if args.demography == 0 or args.demography == None:  ## Equilibrium pop
	demo = None
## Bottlenecks
elif args.demography == 1:
	## create number 1
	BSRS = msprime.Demography()
	BSRS.add_population(name="A", initial_size=10000)
	BSRS.add_population_parameters_change(time=500, initial_size = 500)
	BSRS.add_population_parameters_change(time=1000, initial_size = 10000)
	demo = BSRS

elif args.demography == 2:
	## create number 2
	BSMS = msprime.Demography()
	BSMS.add_population(name="A", initial_size=10000)
	BSMS.add_population_parameters_change(time=1000, initial_size = 500)
	BSMS.add_population_parameters_change(time=1500, initial_size = 10000)
	demo = BSMS

elif args.demography == 3:
	## create number 3
	BSRL = msprime.Demography()
	BSRL.add_population(name="A", initial_size=10000)
	BSRL.add_population_parameters_change(time=500, initial_size = 500)
	BSRL.add_population_parameters_change(time=1500, initial_size = 10000)
	demo = BSRL

elif args.demography == 4:
	## 4
	BSML = msprime.Demography()
	BSML.add_population(name="A", initial_size=10000)
	BSML.add_population_parameters_change(time=1000, initial_size = 500)
	BSML.add_population_parameters_change(time=2000, initial_size = 10000)
	demo = BSML

elif args.demography == 5:
	## 5
	BWRS = msprime.Demography()
	BWRS.add_population(name="A", initial_size=10000)
	BWRS.add_population_parameters_change(time=500, initial_size = 5000)
	BWRS.add_population_parameters_change(time=1000, initial_size = 10000)
	demo = BWRS

elif args.demography == 6:
	## 6
	BWMS = msprime.Demography()
	BWMS.add_population(name="A", initial_size=10000)
	BWMS.add_population_parameters_change(time=1000, initial_size=5000)
	BWMS.add_population_parameters_change(time=1500, initial_size=10000)
	demo = BWMS

elif args.demography == 7:
	## 7
	BWRL = msprime.Demography()
	BWRL.add_population(name="A", initial_size=10000)
	BWRL.add_population_parameters_change(time=500, initial_size=5000)
	BWRL.add_population_parameters_change(time=1500, initial_size=10000)
	demo = BWRL

elif args.demography == 8:
	## 8
	BWML = msprime.Demography()
	BWML.add_population(name="A", initial_size=10000)
	BWML.add_population_parameters_change(time=1000, initial_size=5000)
	BWML.add_population_parameters_change(time=2000, initial_size=10000)
	demo = BWML

elif args.demography == 9:
	## 9
	BSDS = msprime.Demography()
	BSDS.add_population(name="A", initial_size=10000)
	BSDS.add_population_parameters_change(time=5000, initial_size=500)
	BSDS.add_population_parameters_change(time=5500, initial_size=10000)
	demo = BSDS

elif args.demography == 10:
	## 10
	BSDL = msprime.Demography()
	BSDL.add_population(name="A", initial_size=10000)
	BSDL.add_population_parameters_change(time=5000, initial_size=500)
	BSDL.add_population_parameters_change(time=6000, initial_size=10000)
	demo = BSDL

elif args.demography == 11:
	## 11
	BWDS = msprime.Demography()
	BWDS.add_population(name="A", initial_size=10000)
	BWDS.add_population_parameters_change(time=5000, initial_size=5000)
	BWDS.add_population_parameters_change(time=5500, initial_size=10000)
	demo = BWDS

elif args.demography == 12:
	## 12
	BWDL = msprime.Demography()
	BWDL.add_population(name="A", initial_size=10000)
	BWDL.add_population_parameters_change(time=5000, initial_size=5000)
	BWDL.add_population_parameters_change(time=6000, initial_size=10000)
	demo = BWDL

## Expansions (not included in analyses)
elif args.demography == 13:
	ESRS = msprime.Demography()
	ESRS.add_population(name="A", initial_size=12840)
	ESRS["A"].growth_rate = 0.01
	ESRS.add_population_parameters_change(time= 25, growth_rate=0)
	demo = ESRS

elif args.demography == 14:
	EFRS = msprime.Demography()
	EFRS.add_population(name="A", initial_size=34904)
	EFRS["A"].growth_rate = 0.05
	EFRS.add_population_parameters_change(time= 25, growth_rate=0)
	demo = EFRS

elif args.demography == 15:
	ESRL = msprime.Demography()
	ESRL.add_population(name="A", initial_size=16487)
	ESRL["A"].growth_rate = 0.01
	ESRL.add_population_parameters_change(time= 50, growth_rate=0)
	demo = ESRL

elif args.demography == 16:
	EFRL = msprime.Demography()
	EFRL.add_population(name="A", initial_size=121832)
	EFRL["A"].growth_rate = 0.05
	EFRL.add_population_parameters_change(time= 50, growth_rate=0)
	demo = EFRL

elif args.demography == 17:
	ESDS = msprime.Demography()
	ESDS.add_population(name="A", initial_size=12840)
	ESDS.add_population_parameters_change(time=5000, growth_rate=0.01)
	ESDS.add_population_parameters_change(time=5025, growth_rate=0)
	demo = ESDS

elif args.demography == 18:
	EFDS = msprime.Demography()
	EFDS.add_population(name="A", initial_size=34904)
	EFDS.add_population_parameters_change(time=5000, growth_rate=0.05)
	EFDS.add_population_parameters_change(time=5025, growth_rate=0)
	demo = EFDS

elif args.demography == 19:
	ESDL = msprime.Demography()
	ESDL.add_population(name="A", initial_size=16487)
	ESDL.add_population_parameters_change(time=5000, growth_rate=0.01)
	ESDL.add_population_parameters_change(time=5050, growth_rate=0)
	demo = ESDL

elif args.demography == 20:
	EFDL = msprime.Demography()
	EFDL.add_population(name="A", initial_size=121832)
	EFDL.add_population_parameters_change(time=5000, growth_rate=0.05)
	EFDL.add_population_parameters_change(time=5050, growth_rate=0)
	demo = EFDL

## Additional demographic histories added after initial run (Covering more parameter space for strength, timing, and duration)

elif args.demography == 21:
	BMRS = msprime.Demography()
	BMRS.add_population(name="A", initial_size= 10000)
	BMRS.add_population_parameters_change(time = 500, initial_size = 2000)
	BMRS.add_population_parameters_change(time = 1000, initial_size = 10000)
	demo = BMRS

elif args.demography == 22:
	BMRL = msprime.Demography()
	BMRL.add_population(name="A", initial_size = 10000)
	BMRL.add_population_parameters_change(time = 500, initial_size = 2000)
	BMRL.add_population_parameters_change(time = 1500, initial_size = 10000)
	demo = BMRL

elif args.demography == 23:
	BMMS = msprime.Demography()
	BMMS.add_population(name="A", initial_size= 10000)
	BMMS.add_population_parameters_change(time = 1000, initial_size= 2000)
	BMMS.add_population_parameters_change(time = 1500, initial_size = 10000)
	demo = BMMS

elif args.demography == 24:
	BMML = msprime.Demography()
	BMML.add_population(name="A", initial_size=10000)
	BMML.add_population_parameters_change(time = 1000, initial_size = 2000)
	BMML.add_population_parameters_change(time = 2000, initial_size = 10000)
	demo = BMML

elif args.demography == 25: 
	BMDS = msprime.Demography()
	BMDS.add_population(name = "A", initial_size = 10000)
	BMDS.add_population_parameters_change(time = 5000, initial_size=2000)
	BMDS.add_population_parameters_change(time = 5500, initial_size=10000)
	demo = BMDS

elif args.demography == 26:
	BMDL = msprime.Demography()
	BMDL.add_population(name= "A", initial_size = 10000)
	BMDL.add_population_parameters_change(time = 5000, initial_size=2000)
	BMDL.add_population_parameters_change(time = 6000, initial_size=10000)
	demo = BMDL

elif args.demography == 27:
	BSRX = msprime.Demography()
	BSRX.add_population(name="A", initial_size=10000)
	BSRX.add_population_parameters_change(time = 500, initial_size=500)
	BSRX.add_population_parameters_change(time=600, initial_size=10000)
	demo = BSRX

elif args.demography == 28:
	BSMX = msprime.Demography()
	BSMX.add_population(name="A", initial_size=10000)
	BSMX.add_population_parameters_change(time = 1000, initial_size=500)
	BSMX.add_population_parameters_change(time = 1100, initial_size=10000)
	demo = BSMX

elif args.demography == 29:
	BSDX = msprime.Demography()
	BSDX.add_population(name='A', initial_size=10000)
	BSDX.add_population_parameters_change(time = 5000, initial_size=500)
	BSDX.add_population_parameters_change(time = 5100, initial_size=10000)
	demo = BSDX

elif args.demography == 30: 
	BWRX = msprime.Demography()
	BWRX.add_population(name="A", initial_size=10000)
	BWRX.add_population_parameters_change(time=500, initial_size=5000)
	BWRX.add_population_parameters_change(time=600, initial_size=10000)
	demo = BWRX

elif args.demography == 31: 
	BWMX = msprime.Demography()
	BWMX.add_population(name="A", initial_size=10000)
	BWMX.add_population_parameters_change(time=1000, initial_size=5000)
	BWMX.add_population_parameters_change(time=1100, initial_size=10000)
	demo = BWMX

elif args.demography == 32:
	BWDX = msprime.Demography()
	BWDX.add_population(name="A", initial_size=10000)
	BWDX.add_population_parameters_change(time = 5000, initial_size=5000)
	BWDX.add_population_parameters_change(time = 5100, initial_size=10000)
	demo = BWDX

elif args.demography == 33:
	BMRX = msprime.Demography()
	BMRX.add_population(name="A", initial_size = 10000)
	BMRX.add_population_parameters_change(time= 500, initial_size= 2000)
	BMRX.add_population_parameters_change(time= 600, initial_size=10000)
	demo = BMRX

elif args.demography == 34:
	BMMX = msprime.Demography()
	BMMX.add_population(name="A", initial_size=10000)
	BMMX.add_population_parameters_change(time=1000, initial_size= 2000)
	BMMX.add_population_parameters_change(time=1100, initial_size= 10000)
	demo = BMMX

elif args.demography == 35:
	BMDX = msprime.Demography()
	BMDX.add_population(name='A', initial_size = 10000)
	BMDX.add_population_parameters_change(time = 5000, initial_size = 2000)
	BMDX.add_population_parameters_change(time = 5100, initial_size = 10000)
	demo = BMDX

else: 
	raise ValueError("Demography "+ str(args.demography)+ " is not defined")

## /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ##

## Run the simulations for each proportion of females: Resulting in the demographic scenario specified being simulated across the range of BSRs (pf = 0.1 - pf = 0.9)

#initialize the autosomal call (adjust parameters to match BSR)
A1 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.1, pop_size=size, alpha=alpha, demography=demo)
#run the simulations and output the summary files
A1.simulate(reps=reps, loci=loci, pf_out="0_1", prefix=prefix)
#initialize the X chromosome call (adjust parameters to match BSR)
X1 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.1, pop_size=size, alpha=alpha, demography=demo)
#run the simulations and output the summary files 
X1.simulate(reps=reps, loci=loci, pf_out="0_1", prefix=prefix)


A15 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.15, pop_size=size, alpha=alpha, demography=demo)
A15.simulate(reps=reps, loci=loci, pf_out="0_15", prefix=prefix)
X15 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.15, pop_size=size, alpha=alpha, demography=demo)
X15.simulate(reps=reps, loci=loci, pf_out="0_15", prefix=prefix)


A2 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.2, pop_size=size, alpha=alpha, demography=demo)
A2.simulate(reps=reps, loci=loci, pf_out="0_2", prefix=prefix)
X2 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.2, pop_size=size, alpha=alpha, demography=demo)
X2.simulate(reps=reps, loci=loci, pf_out="0_2", prefix=prefix)


A25 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.25, pop_size=size, alpha=alpha, demography=demo)
A25.simulate(reps=reps, loci=loci, pf_out="0_25", prefix=prefix)
X25 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.25, pop_size=size, alpha=alpha, demography=demo)
X25.simulate(reps=reps, loci=loci, pf_out="0_25", prefix=prefix)


A3 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.3, pop_size=size, alpha=alpha, demography=demo)
A3.simulate(reps=reps, loci=loci, pf_out="0_3", prefix=prefix)
X3 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.3, pop_size=size, alpha=alpha, demography=demo)
X3.simulate(reps=reps, loci=loci, pf_out="0_3", prefix=prefix)


A35 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.35, pop_size=size, alpha=alpha, demography=demo)
A35.simulate(reps=reps, loci=loci, pf_out="0_35", prefix=prefix)
X35 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.35, pop_size=size, alpha=alpha, demography=demo)
X35.simulate(reps=reps, loci=loci, pf_out="0_35", prefix=prefix)


A4 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.4, pop_size=size, alpha=alpha, demography=demo)
A4.simulate(reps=reps, loci=loci, pf_out="0_4", prefix=prefix)
X4 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.4, pop_size=size, alpha=alpha, demography=demo)
X4.simulate(reps=reps, loci=loci, pf_out="0_4", prefix=prefix)


A45 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.45, pop_size=size, alpha=alpha, demography=demo)
A45.simulate(reps=reps, loci=loci, pf_out="0_45", prefix=prefix)
X45 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.45, pop_size=size, alpha=alpha, demography=demo)
X45.simulate(reps=reps, loci=loci, pf_out="0_45", prefix=prefix)


A5 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.5, pop_size=size, alpha=alpha, demography=demo)
A5.simulate(reps=reps, loci=loci, pf_out="0_5", prefix=prefix)
X5 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.5, pop_size=size, alpha=alpha, demography=demo)
X5.simulate(reps=reps, loci=loci, pf_out="0_5", prefix=prefix)


A55 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.55, pop_size=size, alpha=alpha, demography=demo)
A55.simulate(reps=reps, loci=loci, pf_out="0_55", prefix=prefix)
X55 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.55, pop_size=size, alpha=alpha, demography=demo)
X55.simulate(reps=reps, loci=loci, pf_out="0_55", prefix=prefix)


A6 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.6, pop_size=size, alpha=alpha, demography=demo)
A6.simulate(reps=reps, loci=loci, pf_out="0_6", prefix=prefix)
X6 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.6, pop_size=size, alpha=alpha, demography=demo)
X6.simulate(reps=reps, loci=loci, pf_out="0_6", prefix=prefix)


A65 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.65, pop_size=size, alpha=alpha, demography=demo)
A65.simulate(reps=reps, loci=loci, pf_out="0_65", prefix=prefix)
X65 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.65, pop_size=size, alpha=alpha, demography=demo)
X65.simulate(reps=reps, loci=loci, pf_out="0_65", prefix=prefix)


A7 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.7, pop_size=size, alpha=alpha, demography=demo)
A7.simulate(reps=reps, loci=loci, pf_out="0_7", prefix=prefix)
X7 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.7, pop_size=size, alpha=alpha, demography=demo)
X7.simulate(reps=reps, loci=loci, pf_out="0_7", prefix=prefix)


A75 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.75, pop_size=size, alpha=alpha, demography=demo)
A75.simulate(reps=reps, loci=loci, pf_out="0_75", prefix=prefix)
X75 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.75, pop_size=size, alpha=alpha, demography=demo)
X75.simulate(reps=reps, loci=loci, pf_out="0_75", prefix=prefix)


A8 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.8, pop_size=size, alpha=alpha, demography=demo)
A8.simulate(reps=reps, loci=loci, pf_out="0_8", prefix=prefix)
X8 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.8, pop_size=size, alpha=alpha, demography=demo)
X8.simulate(reps=reps, loci=loci, pf_out="0_8", prefix=prefix)


A85 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.85, pop_size=size, alpha=alpha, demography=demo)
A85.simulate(reps=reps, loci=loci, pf_out="0_85", prefix=prefix)
X85 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.85, pop_size=size, alpha=alpha, demography=demo)
X85.simulate(reps=reps, loci=loci, pf_out="0_85", prefix=prefix)


A9 = HTSimulate.Autosome(ind=ind, length=length, rec_rate=rec_rate, mut_rate_A=mut_rate, pf=0.9, pop_size=size, alpha=alpha, demography=demo)
A9.simulate(reps=reps, loci=loci, pf_out="0_9", prefix=prefix)
X9 = HTSimulate.X_chr(ind=ind, length=length, rec_rate_f=rec_rate_X, mut_rate_A=mut_rate, pf=0.9, pop_size=size, alpha=alpha, demography=demo)
X9.simulate(reps=reps, loci=loci, pf_out="0_9", prefix=prefix)



