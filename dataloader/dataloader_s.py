import pandas as pd

from config import dataloader_config
from .sentianalysis import SentimentAnalyzer


class DataLoaderSimple:
    def __init__(self):
        self.columns = dataloader_config.CLEAN_DATA_COLUMNS
        self.data_df = pd.DataFrame(columns=self.columns, data=[[0] * len(self.columns)])
        self.tech_words = dataloader_config.TECH_STACK

    def fit_transform(self, raw_data):
        # sponsored
        try:
            sponsored = raw_data['sponsored_or_not']
        except KeyError:
            raise KeyError("No sponsored found in the data")
        if sponsored == '':
            raise ValueError("Sponsored should be either 0 or 1")
        self.data_df['header.sponsored'] = int(sponsored)

        # location
        try:
            location = raw_data['in_US_or_not']
        except KeyError:
            raise KeyError("No location found in the data")
        if location == '':
            raise ValueError("Location should be either 0 or 1")
        self.data_df['map.location'] = int(location)

        # ratings
        try:
            beni_ratings = raw_data['employee_rating_benefits']
        except KeyError:
            raise KeyError("No benefit ratings found in the data")
        try:
            beni_ratings = float(beni_ratings)
        except ValueError:
            raise ValueError("Benefit ratings should be a number, get {}".format(beni_ratings))
        if beni_ratings < 0 or beni_ratings > 5:
            raise ValueError("Benefit ratings should be between 0 and 5")
        self.data_df['benefits.benefitRatingDecimal'] = beni_ratings

        try:
            ceo_ratings = raw_data['ceo_approval_rating']
        except KeyError:
            raise KeyError("No ceo ratings found in the data")
        try:
            ceo_ratings = float(ceo_ratings)
        except ValueError:
            raise ValueError("CEO ratings should be a number, get {}".format(ceo_ratings))
        if ceo_ratings < 0 or ceo_ratings > 5:
            raise ValueError("CEO ratings should be between 0 and 5")
        self.data_df['rating.ceoApproval'] = ceo_ratings

        try:
            recommend_to_friend_rating = raw_data['recommend_to_friend_rating']
        except KeyError:
            raise KeyError("No recommend to friend ratings found in the data")
        try:
            recommend_to_friend_rating = float(recommend_to_friend_rating)
        except ValueError:
            raise ValueError(
                "Recommend to friend ratings should be a number, get {}".format(recommend_to_friend_rating))
        if recommend_to_friend_rating < 0 or recommend_to_friend_rating > 5:
            raise ValueError("Recommend to friend ratings should be between 0 and 5")
        self.data_df['recommendToFriendRating'] = recommend_to_friend_rating

        try:
            star_ratings = raw_data['company_overall_rating']
        except KeyError:
            raise KeyError("No star ratings found in the data")
        try:
            star_ratings = float(star_ratings)
        except ValueError:
            raise ValueError("Star ratings should be a number, get {}".format(star_ratings))
        if star_ratings < 0 or star_ratings > 5:
            raise ValueError("Star ratings should be between 0 and 5")
        self.data_df['rating.starRating'] = star_ratings

        # company size
        try:
            company_size = raw_data['company_size']
        except KeyError:
            raise KeyError("No company size found in the data")
        company_size_col_name = 'gaTrackerData.empSize_' + company_size
        if company_size_col_name not in self.columns:
            raise ValueError("Invalid company size: {}".format(company_size))
        self.data_df[company_size_col_name] = 1

        # industry type
        try:
            industry_type = raw_data['company_industry']
        except KeyError:
            raise KeyError("No industry type found in the data")
        industry_type_col_name = 'gaTrackerData.industry_' + industry_type
        if industry_type_col_name not in self.columns:
            raise ValueError("Invalid industry type: {}".format(industry_type))
        else:
            self.data_df[industry_type_col_name] = 1

        # company type
        try:
            company_type = raw_data['company_type']
        except KeyError:
            raise KeyError("No company type found in the data")
        company_type_col_name = 'overview.type_' + company_type
        if company_type_col_name not in self.columns:
            raise ValueError("Invalid company type: {}".format(company_type))
        else:
            self.data_df[company_type_col_name] = 1

        # benefit keywords
        try:
            benefit_keywords = raw_data['employee_benefits']
        except KeyError:
            raise KeyError("No benefit keywords found in the data")
        benefit_keyword_col_name = 'benefits.highlights.val.name_' + benefit_keywords
        if benefit_keyword_col_name not in self.columns:
            raise ValueError("Invalid benefit keywords: {}".format(benefit_keywords))
        else:
            self.data_df[benefit_keyword_col_name] = 1

        # review sentiment score
        try:
            pro_review = raw_data['reviews_pro']
        except KeyError:
            raise KeyError("No positive review found in the data")
        if pro_review == '':
            print("No positive review found in the data, use 0 as default")
            self.data_df['pro_sentiment'] = 0
        else:
            analyzer = SentimentAnalyzer(pro_review)
            self.data_df['pro_sentiment'] = analyzer.get_sentiment()

        try:
            con_review = raw_data['reviews_con']
        except KeyError:
            raise KeyError("No negative review found in the data")
        if con_review == '':
            print("No negative review found in the data, use 0 as default")
            self.data_df['con_sentiment'] = 0
        else:
            analyzer = SentimentAnalyzer(con_review)
            self.data_df['con_sentiment'] = analyzer.get_sentiment()

        # job_description
        try:
            job_description = raw_data['job_description']
        except KeyError:
            raise KeyError("No job description found in the data")
        if job_description == '':
            print("No job description found in the data, use 0 as default")
        job_description = job_description.lower()
        for word in self.tech_words:
            word_title = 'description_' + word + '_count'
            word_regex = word.replace('+', '\+')
            word_regex = word_regex.replace('.', '\.')
            self.data_df[word_title] = job_description.count(word_regex)

        # job_level
        try:
            job_level = raw_data['job_level']
        except KeyError:
            raise KeyError("No job level found in the data")
        try:
            job_level = float(job_level)
        except ValueError:
            raise ValueError("Job level should be a number, get {}".format(job_level))
        if job_level < 0 or job_level > 5:
            raise ValueError("Job level should be between 0 and 5")
        self.data_df['jobLevel'] = job_level

        # job category
        try:
            job_category = raw_data['job_category']
        except KeyError:
            raise KeyError("No job category found in the data")
        job_category_col_name = 'jobCategory_' + job_category
        if job_category_col_name not in self.columns:
            raise ValueError("Invalid job category: {}".format(job_category))
        else:
            self.data_df[job_category_col_name] = 1

        return self.data_df


if __name__ == '__main__':
    data = {'job.description': 'We are looking for a skilled Software Engineer who is proficient in Java, '
                               'Python, and JavaScript, and has a strong understanding of SQL and C++.'}
    dataloader = DataLoaderSimple()
    try:
        data_df = dataloader.fit_transform(data)
    except KeyError as e:
        print(e)
    pass
