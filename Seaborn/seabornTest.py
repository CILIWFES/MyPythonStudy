import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Seaborn其实是在matplotlib的基础上进行了更高级的API封装，从而使得作图更加容易，在大多数情况下使用seaborn就能做出很具有吸引力的图
sns.set_style("whitegrid")
plt.plot(np.arange(10))
plt.show()
