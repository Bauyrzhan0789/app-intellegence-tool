import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="App Market Intelligence", layout="wide")

st.title("📱 App Market Intelligence Tool")
st.markdown("Добро пожаловать! Это интерактивное приложение для анализа мобильных приложений из Google Play.")

# Загрузка и очистка данных
@st.cache_data
def load_data():
    df = pd.read_csv("googleplaystore (1).csv")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["App", "Category", "Rating", "Reviews", "Installs", "Type", "Price"], inplace=True)

    # Числовые преобразования
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

    # Преобразуем Installs
    df["Installs"] = df["Installs"].str.replace(r"[+,]", "", regex=True)
    df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

    # Обрабатываем Price: заменим 'Free' на 0, затем убираем $ и конвертируем в число
    df["Price"] = df["Price"].replace("Free", "0")
    df["Price"] = df["Price"].str.replace("$", "")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # Рейтинг
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    # Удаляем строки, где остались пропуски после конверсий
    df.dropna(inplace=True)

    return df


df = load_data()

# Выбор категории
category = st.sidebar.selectbox("Выберите категорию:", sorted(df["Category"].unique()))

# Фильтрация по категории
filtered_df = df[df["Category"] == category]

# Визуализация общей информации
st.subheader(f"📊 Приложения в категории: {category}")
st.dataframe(filtered_df[["App", "Rating", "Reviews", "Installs", "Type", "Price"]].sort_values(by="Rating", ascending=False), use_container_width=True)

# Распределение рейтинга
st.subheader("⭐ Распределение рейтингов")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["Rating"], bins=20, kde=True, ax=ax1)
ax1.set_xlabel("Рейтинг")
ax1.set_ylabel("Количество приложений")
st.pyplot(fig1)

# ТОП-10 приложений по количеству отзывов
st.subheader("🏆 ТОП-10 приложений по количеству отзывов")
top_apps = (
    filtered_df.sort_values(by="Reviews", ascending=False)
    .drop_duplicates(subset="App")
    .head(10)
)
st.table(top_apps[["App", "Reviews", "Rating", "Installs"]])

# График по установкам
st.subheader("📈 Количество установок (топ-10)")
fig2, ax2 = plt.subplots()
sns.barplot(data=top_apps, x="Installs", y="App", ax=ax2)
ax2.set_xlabel("Установки")
ax2.set_ylabel("Приложение")
st.pyplot(fig2)

st.markdown("---")
st.markdown("🎯 Сделано с ❤️ для финального проекта")
