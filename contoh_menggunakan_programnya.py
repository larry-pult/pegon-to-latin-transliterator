from transliterasi import PegonToLatinBigramTransliterator
from cer import character_error_rate
import pandas as pd


def get_datasets():
    df_auliya = pd.read_csv("./pegon_auliya.csv")
    df_tasawwuf = pd.read_csv("./pegon_tassawuf.csv")
    df_almuttaqin = pd.read_csv("./pegon_almuttaqin.csv")

    df_auliya = df_auliya.sample(frac=1, random_state=1)
    df_tasawwuf = df_tasawwuf.sample(frac=1, random_state=1)
    df_almuttaqin = df_almuttaqin.sample(frac=1, random_state=1)

    auliya_split_index = int(len(df_auliya) * 0.8)
    tasawwuf_split_index = int(len(df_tasawwuf) * 0.8)
    almuttaqin_split_index = int(len(df_almuttaqin) * 0.8)

    auliya_train = df_auliya[:auliya_split_index]
    tasawwuf_train = df_tasawwuf[:tasawwuf_split_index]
    almuttaqin_train = df_almuttaqin[:almuttaqin_split_index]

    auliya_test = df_auliya[auliya_split_index:]
    tasawwuf_test = df_tasawwuf[tasawwuf_split_index:]
    almuttaqin_test = df_almuttaqin[almuttaqin_split_index:]

    df_train = pd.concat([auliya_train, tasawwuf_train, almuttaqin_train])
    df_test = pd.concat([auliya_test, tasawwuf_test, almuttaqin_test])

    x_train = df_train["pegon"].tolist()
    y_train = df_train["latin"].tolist()

    x_test = df_test["pegon"].tolist()
    y_test = df_test["latin"].tolist()

    return x_train, y_train, x_test, y_test


# training model

x_train, y_train, x_test, y_test = get_datasets()

tlr = PegonToLatinBigramTransliterator()

tlr.train(x_train, y_train)


# evaluasi 1 kata

x_test_0 = x_test[0]
y_test_0 = y_test[0]
y_pred_0 = tlr.predict_word(x_test_0)

cer_0 = character_error_rate(y_pred_0, y_test[0])
print(f"CER dari ground truth {y_test_0} dan hasil prediksi {y_pred_0} = {cer_0}")


# evaluasi semua data test

y_pred = tlr.predict(x_test)

cer_semua = 0
for i in range(len(x_test)):
    cer_semua += character_error_rate(y_pred[i], y_test[i])
cer_semua /= len(x_test)

print(f"rata-rata CER data testing: {round(cer_semua, 4)}")