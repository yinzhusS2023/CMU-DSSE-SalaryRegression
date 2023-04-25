# Modules
# Lemmatizer
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')
# Stop words
from nltk.corpus import stopwords
nltk.download('stopwords')


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
            df[column_name] = result
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.apply_nltk_lemmatize]: Failed because: " + str(e))
            return False
        

    @staticmethod
    def apply_nltk_remove_stopwords(df, column_name):
        try:
            stop_words = list(stopwords.words('english'))
            for stop_word in stop_words:
                regex_stopword = r"\b" + stop_word + r"\b"
                df[column_name] = df[column_name].str.replace(regex_stopword, '', regex=True)
            df[column_name] = df[column_name].replace(r'\s+', ' ', regex=True)
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.apply_nltk_remove_stopwords]: Failed because: " + str(e))
            return False
        
    
