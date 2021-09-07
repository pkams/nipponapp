import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
plt.style.use('ggplot')
st.set_option('deprecation.showfileUploaderEncoding', False)


def main():

	st.title('Análise de Eficiência dos Banhos')

	#st.markdown('Arquivos de exemplo: ')
	#st.markdown('[Baixar planilha de exemplo 1](https://drive.google.com/u/0/uc?id=13snS3ONuqyXG5bTWwIlULCzeUNuAB9xk&export=download)', unsafe_allow_html=True)	
	#st.markdown('[Baixar planilha de exemplo 2](https://drive.google.com/u/0/uc?id=1lwXTwdmTl4D6TKUP2wD6vdRESKBBMYZw&export=download)', unsafe_allow_html=True)		
	
	data = st.file_uploader('Faça upload do arquivo', type=['csv', 'txt', 'xlsx'])
	
	if data is not None:
		st.subheader('Dados:')
		df = pd.read_excel(data)
		
		st.dataframe(df.style.format(formatter="{:.3f}", subset=df.select_dtypes('number').columns))

		df_reduzido = df.iloc[:,2:]
		
		nominal_antes = st.number_input(label='Digite o valor nominal pré-cromo:', step=0.001, format="%.3f")

		nominal_cromo = st.number_input(label='Digite o valor nominal pós-cromo:', step=0.001, format="%.3f")
		
		lim_inf = st.number_input(label='Digite o valor mínimo pós-cromo:', step=0.001, format="%.3f")	

		lim_sup = st.number_input(label='Digite o valor máximo pós-cromo:', step=0.001, format="%.3f")
		
		tempodebanho = st.number_input(label='Insira o tempo de banho (em minutos) :', step=0.1, format="%.1f")


		if ((lim_sup and lim_inf) !=0):
				st.subheader('Valores abaixo do limite inferior e acima do limite superior:')
				st.dataframe(df.style.format(formatter="{:.3f}", subset=df.select_dtypes('number').columns).applymap(lambda x: "background-color: yellow" if ((x > lim_sup) | (x < lim_inf)) else "", subset=df.select_dtypes('number').columns))

		if ((nominal_cromo) and (nominal_antes)) != 0:

			media = np.round(np.mean(df_reduzido.values.ravel()),3)
			median = np.round(np.median(df_reduzido.values.ravel()),3)
			mean_dev = np.round((df_reduzido.values.ravel()-nominal_cromo).mean(),3)

			max = np.round(np.max(df_reduzido.values.ravel()),3)
			min = np.round(np.min(df_reduzido.values.ravel()),3)


			st.subheader('Sumarizações do banho:')
			st.write('Média:', str(media))
			st.write('Mediana (ponto central):', str(median))
			st.write('Valor máximo encontrado: ', str(max))
			st.write('Valor mínimo encontrado: ', str(min))
			st.write('Variação média: ±', str(mean_dev))

			
			st.subheader('Distribuição:')
			fig, ax = plt.subplots() 
			sns.boxplot(data=df_reduzido)
			if ((lim_sup and lim_inf) and st.checkbox('Mostrar valores de referência.')) != 0:
				plt.axhline(nominal_cromo, color='green', label='Valor Nominal')
				plt.axhline(lim_sup, color='red', label='Limites', alpha=0.8, ls='--')
				plt.axhline(lim_inf, color='red', alpha=0.8, ls='--')
			plt.title('Distribuição em cada gancheira')
			plt.xlabel('Gancheira')
			plt.ylabel('Diâmetro')
			plt.legend()
			st.pyplot(fig)

			st.subheader('Camada:')
			camada_med = df_reduzido.mean() - nominal_antes
			fig2, ax2 = fig, ax = plt.subplots()
			sns.barplot(x=camada_med.index,y=camada_med.values)
			plt.title('Camada média depositada em cada gancheira')
			plt.xlabel('Gancheira')
			plt.ylabel('Camada')
			st.pyplot(fig2)

			st.write(camada_med.to_frame(name='Camada Média de cada Gancheira').style.format(formatter="{:.3f}"))
			
			if ((lim_sup) and (lim_inf) and (tempodebanho)) != 0:

				st.subheader('Cálculo de ajuste do banho:')

				cte_deposicao = st.number_input(label='Insira a constante de deposição (em µm/min):', step=0.1, format="%.2f", value = ((media-nominal_antes)/2)*1000/tempodebanho)
				if cte_deposicao != 0:
					st.write(f'Alteração sugerida de tempo para centralizar o banho utilizando as mesmas características e o coeficiente de deposição de {np.round(cte_deposicao,2)} µm/min:')
					st.write(f'{-1*int(1000*(median-nominal_cromo)/(2*cte_deposicao))} minutos')

if __name__ == '__main__':
	main()

