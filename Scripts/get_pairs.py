import argparse
import numpy as np


def get_pairs(insns, window):
    for i in range(len(insns)):
        first = np.zeros(256, dtype = int)
        first[insns[i]] = 1
        inds = [i-x for x in range(1, window+1)] + [i+x for x in range(1, window+1)]
        for ind in inds:
            second = np.zeros(256)
            if ind >= 0 and ind < len(insns):
                second[insns[ind]] = 1
                yield [first , second]


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("f", help = "The .csv file to extract pairs of instructions from", type = str)
	parser.add_argument("-n", help = "The window size you want to generate pairs with", type = int, default = 3)

	args = parser.parse_args()
	f = args.f
	n = args.n

	with open(f, "r") as in_file:
		with open ("X3.csv", "w+") as X_file:
			with open ("Y3.csv", "w+") as y_file:
				l = in_file.readline()
				while l:
					pairs = list(get_pairs([int(x.strip()) for x in l.split(",")], n))
					data_X = np.array([x[0] for x in pairs])
					data_Y = np.array([x[1] for x in pairs])
					for X in data_X:
						X_file.write(", ".join(str(x) for x in X))
						X_file.write("\n")
					for Y in data_Y:
						y_file.write(", ".join(str(y) for y in Y))
						y_file.write("\n")
					l = in_file.readline()

				y_file.close()
			X_file.close()
		in_file.close()