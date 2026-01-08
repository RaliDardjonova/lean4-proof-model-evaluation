
import numpy as np

from matplotlib import pyplot as plt


ds15_gptq_8 = []
ds15_gptq_4 = []
ds15_full = []
ds15_awq_4 = []

ds2_noncot_gptq_4 = []
ds2_noncot_gptq_8 = []
ds2_noncot_full = []
ds2_noncot_awq_4 = []

ds2_cot_gptq_4 = []
ds2_cot_gptq_8 = []
ds2_cot_full = []
ds2_cot_awq_4 = []


plt.plot(ds15_gptq_8[0], ds15_gptq_8[1], 
         '-gD',
         # markevery=markers_on,
          label='DeepSeek-Prover-v1.5-RL - 8bit gptq')
plt.plot(ds15_gptq_4[0], ds15_gptq_4[1], 
         '-gD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-v1.5-RL - 4bit gptq')
plt.plot(ds15_awq_4[0], ds15_awq_4[1], 
         '-yD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-v1.5-RL - 4bit awq')
plt.plot(ds15_full[0], ds15_full[1], 
         '-bD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-v1.5-RL')


plt.plot(ds2_noncot_gptq_8[0], ds2_noncot_gptq_8[1], 
         '-gD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B - 8bit gptq')
plt.plot(ds2_noncot_gptq_4[0], ds2_noncot_gptq_4[1], 
         '-gD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B - 4bit gptq')
plt.plot(ds2_noncot_awq_4[0], ds2_noncot_awq_4[1], 
         '-yD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B - 4bit awq')
plt.plot(ds2_noncot_full[0], ds2_noncot_full[1], 
         '-bD',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B')


plt.plot(ds2_cot_gptq_8[0], ds2_cot_gptq_8[1], 
         marker='D', mec = 'orange', mfc = 'orange', color='orange',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B - 8bit gptq (CoT)')
plt.plot(ds2_cot_gptq_4[0], ds2_cot_gptq_4[1], 
          marker='D', mec = 'orange', mfc = 'orange', color='orange',
         # markevery=markers_on,
          label='DeepSeek-Prover-V2-7B - 4bit gptq (CoT)')
plt.plot(ds2_cot_awq_4[0], ds2_cot_awq_4[1], 
          marker='D', mec = 'pink', mfc = 'pink',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B - 4bit awq (CoT)')
plt.plot(ds2_cot_full[0], ds2_cot_full[1], 
          marker='D', mec = 'r', mfc = 'r', color='red',
         # markevery=markers_on, 
          label='DeepSeek-Prover-V2-7B (CoT) - reported')

plt.legend(bbox_to_anchor=(1.1, -0.5))
plt.show()
