# Modules
# Lemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('omw-1.4')
nltk.download('wordnet')
# Stop words
nltk.download('stopwords')
# TF-IDF


class WordProcessor:
    @staticmethod
    def __remove_punctuation(df, column_name):
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
    def __remove_s(df, column_name):
        try:
            df[column_name] = df[column_name].str.replace("'s", "", regex=True)
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.remove_punctuation]: Failed because: " + str(e))
            return False

    @staticmethod
    def __apply_nltk_lemmatize(df, column_name):
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
    def __apply_nltk_remove_stopwords(df, column_name):
        try:
            stop_words = list(stopwords.words('english'))
            for stop_word in stop_words:
                regex_stopword = r"\b" + stop_word + r"\b"
                df[column_name] = df[column_name].str.replace(
                    regex_stopword, '', regex=True)
            df[column_name] = df[column_name].replace(r'\s+', ' ', regex=True)
            return True
        except Exception as e:
            print(
                "Error[In WordProcessor.apply_nltk_remove_stopwords]: Failed because: " + str(e))
            return False

    @staticmethod
    def generate_tfidf_matrix(df, column_name):
        try: 
            ngram_range = (1, 2)
            min_df = 0.01
            max_df = 0.8
            max_features = 300
            tfidf = TfidfVectorizer(encoding='utf-8',
                                    ngram_range=ngram_range,
                                    stop_words=None,
                                    lowercase=False,
                                    max_df=max_df,
                                    min_df=min_df,
                                    max_features=max_features,
                                    norm='l2',
                                    sublinear_tf=True)
            tfidf_result = tfidf.fit_transform(df[column_name]).toarray()
            return True, tfidf_result
        except Exception as e:
            print(
                "Error[In WordProcessor.generate_tfidf_matrix]: Failed because: " + str(e))
            return False, None
        
    @staticmethod
    def word_process_procedure(df, column_name):
        try:
            procedure_functions = [
                WordProcessor.__remove_punctuation,
                WordProcessor.__remove_s,
                WordProcessor.__apply_nltk_lemmatize,
                WordProcessor.__apply_nltk_remove_stopwords,
            ]
            before_tfidf = all([item(df, column_name) for item in procedure_functions])
            if not before_tfidf:
                return False, None
            return WordProcessor.generate_tfidf_matrix(df, column_name)
        except Exception as e:
            print(
                "Error[In WordProcessor.word_process_procedure]: Failed because: " + str(e))
            return False, None
