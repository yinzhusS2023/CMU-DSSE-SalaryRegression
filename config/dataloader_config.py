JOB_TITLE_SEARCH_WORDS = [
    'Software',
    'Systems',
    'Applications',
    'Cloud',
    'Solution',
    'Architect',
    'Algorithm',
    'Test',
    'IOS',
    'UI-UX',
]

SELECTED_COLS_ID = [
    'benefits.highlights',  # Benefits highlights table id
    'reviews',  # Reviews table id
    'salary.salaries',  # Salaries table id
]

SELECTED_COLS_MAIN = [
    'job.description',  # Job description
    'header.sponsored',  # Boolean Whether the job is sponsored
    'map.location',  # Job location
    'gaTrackerData.empSize',  # Categorical Company size
    'gaTrackerData.industry',  # Categorical Company Industry
    'overview.type',  # Company type
    'benefits.benefitRatingDecimal',  # Num Employee rating on company benefits
    'rating.ceoApproval',  # CEO approval rating
    'rating.recommendToFriend',  # Recommend to friend rating
    'rating.starRating',  # Overall rating
]

SELECTED_COLS_BENI = [
    'id',
    'benefits.highlights.val.name'  # Employee benefits
]

SELECTED_COLS_REVIEW = [
    'id',
    'reviews.val.cons',  # Employee reviews: cons
    'reviews.val.pros',  # Employee reviews: pros
]

SELECTED_COLS_SALARY = [
    'id',
    'salary.salaries.val.salaryPercentileMap.payPercentile10',
    'salary.salaries.val.salaryPercentileMap.payPercentile90',
    'salary.salaries.val.payPeriod',
    'salary.salaries.val.jobTitle'
]

OUTLIER_COLS_MAIN = [
    'benefits.benefitRatingDecimal',
    'rating.ceoApproval',
    'rating.recommendToFriend',
    'rating.starRating'
]

DATA_FILE_PATHS = [
    '../data/glassdoor.csv',
    '../data/glassdoor_benefits_highlights.csv',
    '../data/glassdoor_reviews.csv',
    '../data/glassdoor_salary_salaries.csv'
]

CLEAN_DATA_PATH = '../data/glassdoor_clean_data.csv'

US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA',
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

TECH_STACK = [
    "java",
    "python",
    "javascript",
    "sql",
    "c++",
    "aws",
    "amazon web services",
    "git",
    "docker",
    "kubernetes",
    "react",
    "node.js",
    "html",
    "css",
    "agile",
    "linux",
    "devops",
    "restful",
    ".net",
    "c#",
    "php",
    "ruby",
    "apache",
    "spark",
    "typescript",
    "flask",
    "django",
    "tensorflow",
    "spring",
    "azure",
    "redux",
    "vue.js",
    "angular",
    "bash",
    "mongodb",
    "hadoop",
    "pytorch",
    "react",
    "firebase",
    "unity",
    "jenkins",
    "oauth",
    "mysql",
    "postgresql",
    "apache kafka",
    "ansible",
    "elasticsearch",
    "golang",
    "ionic",
    "swift",
    "objective-c",
    "kotlin",
    "xamarin",
    "express.js",
    "graphql",
    "selenium",
    "jira",
    "apache cassandra",
    "rabbitmq",
    "chef",
    "puppet"
]

JOB_LEVEL_MAP = {
    1: ['i', 'graduate', 'apprentice', 'junior', 'se1'],
    2: ['ii', 'se2'],
    3: ['iii', 'senior', 'sr', 'advisory'],
    4: ['iv', 'advanced', 'staff', 'chief'],
    5: ['v', 'lead', 'principal', 'director', 'president', 'level 7']
}

JOB_CATEGORY_MAP = {
    'Development': ['develop', 'software'],
    'Solution': ['solution'],
    'Test': ['test'],
    'Support': ['support'],
    'System': ['system'],
    'IT Director': ['associate director - it']
}
