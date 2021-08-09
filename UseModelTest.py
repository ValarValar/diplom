import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import sklearn
import bokeh
import pandas as pd
import sklearn.metrics
import bokeh.models
import bokeh.plotting

#import sns
import seaborn as sns
import tensorflow_text

def visualize_similarity(embeddings_1, embeddings_2, labels_1, labels_2,
                         plot_title,
                         plot_width=1200, plot_height=600,
                         xaxis_font_size='12pt', yaxis_font_size='12pt'):

  assert len(embeddings_1) == len(labels_1)
  assert len(embeddings_2) == len(labels_2)

  # arccos based text similarity (Yang et al. 2019; Cer et al. 2019)
  sim = 1 - np.arccos(
      sklearn.metrics.pairwise.cosine_similarity(embeddings_1,
                                                 embeddings_2))/np.pi

  embeddings_1_col, embeddings_2_col, sim_col = [], [], []
  for i in range(len(embeddings_1)):
    for j in range(len(embeddings_2)):
      embeddings_1_col.append(labels_1[i])
      embeddings_2_col.append(labels_2[j])
      sim_col.append(sim[i][j])
  df = pd.DataFrame(zip(embeddings_1_col, embeddings_2_col, sim_col),
                    columns=['embeddings_1', 'embeddings_2', 'sim'])

  mapper = bokeh.models.LinearColorMapper(
      palette=[*reversed(bokeh.palettes.YlOrRd[9])], low=df.sim.min(),
      high=df.sim.max())

  p = bokeh.plotting.figure(title=plot_title, x_range=labels_1,
                            x_axis_location="above",
                            y_range=[*reversed(labels_2)],
                            plot_width=plot_width, plot_height=plot_height,
                            tools="save",toolbar_location='below', tooltips=[
                                ('pair', '@embeddings_1 ||| @embeddings_2'),
                                ('sim', '@sim')])
  p.rect(x="embeddings_1", y="embeddings_2", width=1, height=1, source=df,
         fill_color={'field': 'sim', 'transform': mapper}, line_color=None)

  p.title.text_font_size = '12pt'
  p.axis.axis_line_color = None
  p.axis.major_tick_line_color = None
  p.axis.major_label_standoff = 16
  p.xaxis.major_label_text_font_size = xaxis_font_size
  p.xaxis.major_label_orientation = 0.25 * np.pi
  p.yaxis.major_label_text_font_size = yaxis_font_size
  p.min_border_right = 300

  bokeh.io.output_notebook()
  bokeh.io.show(p)


embed = tf.saved_model.load("D:/Pycharm projects/use model/universal-sentence-encoder-multilingual_3")



ru1 = ["пока",
            "увидимся",
            "до встречи","привет", "здравствуй", "добрый вечер"]
ru_result = embed(ru1)
income = ["до свидания","Приветствую", "здарова"]
ru2 = ["привет", "здравствуй", "добрый день"]
income_result = embed(income)
visualize_similarity(ru_result, income_result,
                     ru1, income,  "Multilingual Universal Sentence Encoder for Semantic Retrieval (Yang et al., 2019)")
#embed = hub.load("")
#embed = hub.load("/use model/universal-sentence-encoder-multilingual_3/saved_model.pb")
print(1)



income = ["до свидания"]
ru_result = embed(ru1)
print(ru_result)
income_result = embed(income)
similarity_matrix_it = np.inner(ru_result, income_result)
print(similarity_matrix_it)

#income = "нет"
#income_result = embed(income)
similarity_matrix_it = np.inner(ru_result, income_result)
print(similarity_matrix_it)

visualize_similarity(ru_result, income_result,
                     ru1, income,  "Multilingual Universal Sentence Encoder for Semantic Retrieval (Yang et al., 2019)")
#for st in ru_result:
    #print(tf.keras.losses.cosine_similarity(income_result,st))


