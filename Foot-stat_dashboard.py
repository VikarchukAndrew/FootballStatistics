import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache
def cache_func(a,b):
   return a(b)

sns.set(style='darkgrid', palette='colorblind')

df = cache_func(pd.read_csv, 'all_foot_stat.csv')
df = df.drop(columns=['Unnamed: 0'])
df = df.sort_values(['Клуб'])
df = df.drop(df.index[df['Кол-во минут'] == 0])


#Создаем сайдбар и селекторы

st.sidebar.title('Статистика игроков топ-5 лиг за 2019-20')

clubs = st.sidebar.multiselect(
	'Выберите клуб', df['Клуб'].unique()
)

position = st.sidebar.multiselect(
	'Выберите позицию', df['Позиция'].unique()
)

parameter = st.sidebar.multiselect(
	'Выберите параметры', df.columns
)

sort_by = st.sidebar.multiselect(
	'Фильтр', parameter 
)



new_df = df[(df['Клуб'].isin(clubs)) & (df['Позиция'].isin(position))]

new_df = new_df[parameter]


if sort_by:
	new_df = new_df.sort_values([*sort_by], ascending=False)


#Выводим результат пользователя и создаем общую описательную статистику

if st.sidebar.checkbox('Показать статистику'):
	st.subheader('Ваш результат')
	st.write(new_df)

	if not new_df.empty:
		st.subheader('Описательная статистика по вашей табличке:')

		try:
			st.write(new_df.groupby('Клуб').mean())
			max_goals_name = new_df['Имя'].where(new_df['Голы'] == new_df['Голы'].max())
			max_age_name = new_df['Имя'].where(new_df['Возраст'] == new_df['Возраст'].max())
			max_min_name = new_df['Имя'].where(new_df['Кол-во минут'] == new_df['Кол-во минут'].max())
			most_effective = new_df[['Имя', 'Голы', 'Кол-во минут']]
			most_effective['Эффективность'] = most_effective['Кол-во минут'] / most_effective['Голы'] 
			most_effective_score = most_effective['Имя'].where(most_effective['Эффективность'] == most_effective['Эффективность'].min())
		except:
			pass
		
		
		try:
			st.write('Лучший бомбардир: ', max_goals_name.sort_values().iloc[0], '(', new_df['Голы'].max(), ')')
			st.write('Самый возрастной игрок: ', max_age_name.sort_values().iloc[0], '(', new_df['Возраст'].max(), ')')
			st.write('Больше всего минут на поле: ', max_min_name.sort_values().iloc[0], '(', new_df['Кол-во минут'].max(), ')')
			st.write('Самый эффективный игрок: ', most_effective_score.sort_values().iloc[0], '(', most_effective['Эффективность'].min(), ')')
		except:
			pass


#Создаем параметр "Сумма голов" для круговой диаграммы
total = []
for i in clubs:
	
	team = df[df['Клуб'].str.contains(i)]
	team.loc[df['Голы']  < 0 , 'Голы'] = 0

	total_goals = team['Голы'].sum()

	
	total.append(total_goals.item())


#Диаграмма рассеяния
def scatter_plot(x, y, hue):
	
	sns.scatterplot(x=x, y=y, hue=hue)

#Круговая диаграмма
def pie_plot(x, y):
	
	fig1, ax1 = plt.subplots()
	ax1.pie(x, labels=y, autopct='%1.1f%%')
	ax1.axis('equal')

	plt.show()

#Диаграмма размаха
def box_plot(x, y):
	
	sns.boxplot(x=x, y=y)


#Гистограмма
def dist_plot(x):

	sns.distplot(x, hist=False, color="g", kde_kws={"shade": True})



#Рисуем все диаграммы
if st.sidebar.checkbox('Показать диаграммы'):

	# try:
	# 	scatter_plot(new_df[sort_by[0]], new_df[sort_by[1]], new_df['Клуб'])
	# 	st.subheader(f'Диаграмма рассеяния: \'{sort_by[0]}\' и \'{sort_by[1]}\'')
	# 	st.pyplot()
	# except (IndexError, KeyError) as e:
	# 	pass

	try:
		dist_plot(new_df[sort_by[0]])
		st.subheader(f'Гистограмма: \'{sort_by[0]}\'')
		st.pyplot()
	except (IndexError, ValueError) as e:
		pass

	
	try:
		box_plot(new_df['Клуб'], new_df[sort_by[0]])
		st.subheader(f'Диаграмма размаха: \'Клуб\' и \'{sort_by[0]}\'')
		st.pyplot()
	except (IndexError, KeyError, ValueError) as e:
		pass


	try:
		pie_plot(total, clubs)
		st.subheader(f'Круговая диаграмма: \'Голы\'')
		st.pyplot()
	except:
		pass







