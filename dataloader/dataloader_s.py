import pandas as pd

from config import dataloader_config


class DataLoaderSimple:
    def __init__(self):
        self.data_df = pd.DataFrame(index=[0])
        self.tech_words = dataloader_config.TECH_STACK

    def fit_transform(self, raw_data):
        # sponsored
        try:
            sponsored = raw_data['sponsored']
        except KeyError:
            raise KeyError("No sponsored found in the data")
        self.data_df['sponsored'] = int(sponsored)

        # location
        try:
            location = raw_data['location']
        except KeyError:
            raise KeyError("No location found in the data")
        self.data_df['location'] = int(location)

        # ratings
        try:
            beni_ratings = raw_data['benefitRating']
        except KeyError:
            raise KeyError("No benefit ratings found in the data")
        if beni_ratings < 0 or beni_ratings > 5:
            raise ValueError("Benefit ratings should be between 0 and 5")
        self.data_df['benefits.benefitRatingDecimal'] = beni_ratings

        try:
            ceo_ratings = raw_data['ceoRating']
        except KeyError:
            raise KeyError("No ceo ratings found in the data")
        if ceo_ratings < 0 or ceo_ratings > 5:
            raise ValueError("CEO ratings should be between 0 and 5")
        self.data_df['ceoRating'] = ceo_ratings

        try:
            recommend_to_friend_rating = raw_data['recommendToFriendRating']
        except KeyError:
            raise KeyError("No recommend to friend ratings found in the data")
        if recommend_to_friend_rating < 0 or recommend_to_friend_rating > 5:
            raise ValueError("Recommend to friend ratings should be between 0 and 5")
        self.data_df['recommendToFriendRating'] = recommend_to_friend_rating

        try:
            star_ratings = raw_data['starRating']
        except KeyError:
            raise KeyError("No star ratings found in the data")
        if star_ratings < 0 or star_ratings > 5:
            raise ValueError("Star ratings should be between 0 and 5")
        self.data_df['starRating'] = star_ratings

        # company size
        try:
            company_size = raw_data['companySize']
        except KeyError:
            raise KeyError("No company size found in the data")

        # job_description
        try:
            job_description = raw_data['job.description']
        except KeyError:
            raise KeyError("No job description found in the data")
        if job_description is None:
            raise ValueError("Job description should not be empty")
        job_description = job_description.lower()
        for word in self.tech_words:
            word_title = 'description_' + word + '_count'
            word_regex = word.replace('+', '\+')
            word_regex = word_regex.replace('.', '\.')
            self.data_df[word_title] = job_description.count(word_regex)

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
