import seaborn
import matplotlib.pyplot as plt
import getKeyword

word_and_importance = getKeyword.getKeywordAndImportance()
seaborn.set(context="talk")
fig = plt.subplots(figsize=(8, 8))
 
seaborn.countplot(y=word_and_importance,order=[i[0] for i in c.most_common(20)])