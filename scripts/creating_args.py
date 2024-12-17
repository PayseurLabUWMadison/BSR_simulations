BN_runcodes = ["EQUI", "BSRS", "BSMS", "BSRL", "BSML", "BWRS", "BWMS", "BWRL", "BWML", "BSDS", "BSDL", "BWDS", "BWDL", "ESRS", "EFRS", "ESRL", "EFRL", "ESDS",
			 "EFDS", "ESDL", "EFDL", "BMRS", "BMRL", "BMMS", "BMML", "BMDS", "BMDL", "BSRX", "BSMX", "BSDX", "BWRX", "BWMX", "BWDX", "BMRX", "BMMX", "BMDX"]

Demos = list(range(len(BN_runcodes))) 
for x in Demos:
	Demos[x] = str(x)


alphas = ["1", "3"]


rec_rates = ["5e-9", "5e-8"]

mut_rates = ["5e-9", "5e-8"]

lines = []

for idx in range(len(BN_runcodes)):
	for alpha in alphas:
		for rec_rate in rec_rates:
			for mut_rate in mut_rates:
				prefix = BN_runcodes[idx]+"_a"+alpha+"_r"+rec_rate+"_m"+mut_rate
				line = prefix+", "+Demos[idx]+", "+alpha+", "+rec_rate+", "+mut_rate
				lines.append(line)



with open('simulation_args.txt', 'w') as f:
	for line in lines:
		f.write(line)
		f.write("\n")


# all_prefixes = []
# for idx in range(len(BN_runcodes)):
# 	for alpha in alphas:
# 		for rec_rate in rec_rates:
# 			for mut_rate in mut_rates:
# 				prefix = BN_runcodes[idx]+"_a"+alpha+"_r"+rec_rate+"_m"+mut_rate
# 				all_prefixes.append(prefix)

# print(len(all_prefixes))


## Can print out the above list for use in R or anywhere else
