JOB_TITLE_SEARCH_WORDS = [
    'Software',
    'Systems',
    'Project',
    'Principal',
    'Applications',
    'Cloud',
    'Solution',
    'Architect',
    'Algorithm',
    'Test',
    'IT',
    'IOS',
    'UI-UX',
    'Designer']

SELECTED_COLS = [
    'benefits.benefitRatingDecimal',  # Num Employee rating on company benefits TODO: eliminate outliers
    'gaTrackerData.empSize',  # Categorical Company size TODO: calculate unique values and ONE-HOT
    'gaTrackerData.industry',  # Categorical Company Industry TODO: calculate unique values and ONE-HOT
    'header.sponsored',  # Boolean Whether the job is sponsored TODO: convert to binary: sponsored/not sponsored
    'job.description',  # Job description TODO: calculate word count and TF-IDF on most 10~20 frequent words
    'map.location',  # Job location TODO: convert to binary: US/Non-US
    'overview.type',  # Company type TODO: calculate unique values and ONE-HOT
    'rating.ceoApproval',  # CEO approval rating TODO: eliminate outliers
    'rating.recommendToFriend',  # Recommend to friend rating TODO: eliminate outliers
    'rating.starRating',  # Overall rating TODO: eliminate outliers

    'benefits.highlights.val.name',  # Employee benefits TODO: - In glassdoor_benefits_highlights.csv
    #                         - Calculate unique values and ONE-HOT

    'reviews.val.cons',  # Employee reviews: cons TODO: - In glassdoor_reviews.csv
    #                              - Calculate sentiment score
    'reviews.val.pros',  # Employee reviews: pros TODO: - In glassdoor_reviews.csv
    #                              - Calculate sentiment score

    'salary.salaries.val.salaryPercentileMap.payPercentile10',
    'salary.salaries.val.salaryPercentileMap.payPercentile90',
    'salary.salaries.val.payPeriod',
    'salary.salaries.val.jobTitle']

OUTLIER_COLS = [
    'benefits.benefitRatingDecimal',
    'rating.ceoApproval',
    'rating.recommendToFriend',
    'rating.starRating']

DATA_FILE_PATHS = [
    '../data/glassdoor.csv',
    '../data/glassdoor_benefits_highlights.csv',
    '../data/glassdoor_reviews.csv',
    '../data/glassdoor_salary_salaries.csv'
]
