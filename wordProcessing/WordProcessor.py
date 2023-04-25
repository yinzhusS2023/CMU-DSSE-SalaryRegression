# Modules
from nltk.stem import WordNetLemmatizer
import nltk
from sqlalchemy import column
nltk.download('omw-1.4')
nltk.download('wordnet')


class WordProcessor:
    @staticmethod
    def remove_punctuation(df, column_name):
        try:
            punctuation_signs = list("?:!.,;")
            for punctuation_sign in punctuation_signs:
                df[column_name] = df[column_name].str.replace(
                    punctuation_sign, ' ', regex=True)
                return True
        except Exception as e:
            print(
                "Error[In WordProcessor.remove_punctuation]: Failed because: " + str(e))
            return False

    @staticmethod
    def remove_s(df, column_name):
        try:
            df[column_name] = df[column_name].str.replace("'s", "", regex=True)
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.remove_punctuation]: Failed because: " + str(e))
            return False

    @staticmethod
    def remove_s(df, column_name):
        try:
            df[column_name] = df[column_name].str.replace("'s", "", regex=True)
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.remove_s]: Failed because: " + str(e))
            return False

    @staticmethod
    def apply_nltk_lemmatize(df, column_name):
        try: 
            WNL = WordNetLemmatizer()
            num_rows = len(df)
            result = []
            for row in range(num_rows):
                text_words = (df.loc[row][column_name]).split(" ")
                lemmatized_list = [WNL.lemmatize(
                    word, pos="v") for word in text_words]
                result.append(" ".join(lemmatized_list))
            df[column] = result
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.apply_nltk_lemmatize]: Failed because: " + str(e))
            return False