import matplotlib.pyplot as plt
import io
import base64
from matplotlib import style

style.use('seaborn-pastel')
 
def build_graph(x_coordinates, y_coordinates):
	plt.figure(figsize=plt.figaspect(1))
	img = io.BytesIO()
    #plt.bar(x_coordinates, y_coordinates ,align = 'center', width = 0.3)
	def make_autopct(values):
		def my_autopct(pct):
			total = sum(values)
			val = int(round(pct*total/100.0))
			return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
		return my_autopct
	plt.title("President")
	plt.pie(y_coordinates, labels = x_coordinates, autopct=make_autopct(y_coordinates), explode = (0.1,0.1,0.1,0.1), shadow = True, wedgeprops = {'linewidth': 3})
	plt.savefig(img, format='png')
	img.seek(0)
	graph_url = base64.b64encode(img.getvalue()).decode()
	plt.close()
	return 'data:image/png;base64,{}'.format(graph_url)