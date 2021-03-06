import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np

"""
Customized Loss Function for Formula (8) At Page 6

"""
class stAttentionLoss(nn.Module):
    """
    stAttentionLoss Constructor
    @param: lambda_1, lambda_2 are both hyperparameter of penalty

    """
    def __init__(self, lambda_1 = 0.1, lambda_2 = 0.01):
        super(stAttentionLoss, self).__init__()
        self.lambda_1 = lambda_1
        self.lambda_2 = lambda_2

    """
    Forward Method 
    Implement the loss function
    @param 
    
    inputs: model output # dimension: # (batch_size, seq_length, nClasses)
    target: true label # dimension: # (1) #### for one video, LongTensor scalar; for batch, (batch_size, 1)
    alpha: attn_weights # dimension: # (batch_size, seq_length, 196)
    beta: betas returned by model #(batch_size, seq_length, 1)

    @return: loss Tensor scalar
    """
    def forward(self, inputs, target, alpha, beta):
        #alpha = torch.squeeze(alpha,dim = 2)
        penalty_1 = self.lambda_1 * torch.sum(1 - torch.sum(alpha,dim = 1), dim = 1)
        
        beta_norm = torch.abs(beta) # Here should be norm |beta_{t}| #(batch_size, seq_length)

        penalty_2 = self.lambda_2 * torch.sqrt(torch.sum(torch.pow(beta_norm,2),dim = 1)) # Here should be summing over dim=0

        penalty_2 = torch.squeeze(penalty_2,dim = 1)


        # using cross entropy means have softmax inside loss, DO NOT add softmax at the end of model?
        return F.cross_entropy(inputs,target) + torch.mean(penalty_1) + torch.mean(penalty_2)

###################


# input = np.array([[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]])
# input = np.reshape(input,(1,10))
# input = torch.Tensor(input)

# label = torch.LongTensor([0])

# attn_weights = np.zeros((2,20,196))
# for j in range(2):
#     for i in range(20):
#         attn_weights[j][i] = np.array([1 / 196] * 196)
# attn_weights = torch.Tensor(attn_weights)
# #attn_weights = torch.unsqueeze(attn_weights,dim = 0)
# print(attn_weights.size())

# betas = torch.Tensor([[[0.0501],
#         [0.0285],
#         [0.0274],
#         [0.0275],
#         [0.0278],
#         [0.0280],
#         [0.0281],
#         [0.0282],
#         [0.0283],
#         [0.0284],
#         [0.0284],
#         [0.0285],
#         [0.0285],
#         [0.0285],
#         [0.0286],
#         [0.0286],
#         [0.0286],
#         [0.0286],
#         [0.0286],
#         [0.0286]],[[0.0501],
#         [0.0285],
#         [0.0274],
#         [0.0275],
#         [0.0278],
#         [0.0280],
#         [0.0281],
#         [0.0282],
#         [0.0283],
#         [0.0284],
#         [0.0284],
#         [0.0285],
#         [0.0285],
#         [0.0285],
#         [0.0286],
#         [0.0286],
#         [0.0286],
#         [0.0286],
#         [0.0286],
#         [0.0286]]])
# print(betas.size())


# ##########################################

# myLoss = stAttentionLoss(0.1, 0.01)
# loss = myLoss(input, label, attn_weights, betas)
# print(loss)
