from model import stDecoder
from loss import stAttentionLoss
import h5py
import torch
import numpy as np
import pdb




def main():
	myDecoder=stDecoder(256,2,51)
	myLoss = stAttentionLoss(0.1, 0.01)
	optimizer=torch.optim.Adam(myDecoder.parameters(),lr=0.0001)
	videos=h5py.File("train.hdf5",'r')['train_set']
    labels=h5py.File("../train_label.hdf5", 'r')['train_label']
    pdb.set_trace()
	# print(labels.size())
	for i,(video,label) in enumerate(zip(videos,labels)):
		optimizer.zero_grad()
		logits, alphas, betas=myDecoder(video)
		print("label",label)
		print(label.size())
		loss = myLoss(logit, label, alphas, betas)
		loss.backward()
		optimizer.step()

















if __name__== "__main__":
	main()
