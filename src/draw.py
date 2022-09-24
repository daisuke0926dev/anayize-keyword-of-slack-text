import matplotlib.pyplot as plt
import getKeyword
import numpy as np
import japanize_matplotlib

word_and_importance = getKeyword.getKeywordAndImportance()

myList = word_and_importance.items()
myList = sorted(myList) 
x, y = zip(*myList) 

plt.barh(x, y, color='#effef0', edgecolor='#9ffea0')
plt.title("キーワード", fontname="MS Gothic")
plt.show()