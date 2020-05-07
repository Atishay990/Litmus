from collections import defaultdict
import pickle

members = defaultdict(list)
outfile  = open('network','wb')
pickle.dump(members,outfile)
outfile.close()
