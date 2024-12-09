from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy

# Sample data (user_id, item_id, rating)
data = [
    ('user1', 'ad1', 5),
    ('user2', 'ad2', 4),
    ('user1', 'ad3', 3),
    ('user3', 'ad1', 4),
    ('user2', 'ad3', 5),
]

# Prepare the data for Surprise
reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(pd.DataFrame(data, columns=['user_id', 'item_id', 'rating']), reader)

# Train a model
trainset, testset = train_test_split(dataset, test_size=0.2)
model = SVD()
model.fit(trainset)

# Function to get recommendations for a user
def recommend(user_id):
    predictions = [model.predict(user_id, ad_id) for ad_id in ['ad1', 'ad2', 'ad3']]
    recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)
    return [rec.iid for rec in recommendations]
