import pandas as pd

# Load the dataset
file_path = 'data/dataSetFinal.csv'
df = pd.read_csv(file_path)

# Function to get user preferences
def get_user_preferences():
    preferences = {}
    print("Please rate your preference from 1 to 5 (1=least preferred, 5=most preferred):")
    
    # Asking user preferences for each feature
    features = ['bpm', 'nrgy', 'dnce', 'dB', 'live', 'val', 'dur', 'acous', 'spch', 'pop']
    for feature in features:
        rating = int(input(f"How much do you like songs with {feature} in the range 1-5? "))
        preferences[feature] = rating
    
    return preferences

# Function to calculate similarity score between user preferences and songs
def calculate_similarity(song, preferences):
    score = 0
    for feature in preferences:
        weight = preferences[feature]
        song_value = song[feature]
        score += weight * song_value
    return score

# Main function
def main():
    # Get user preferences
    user_preferences = get_user_preferences()
    
    # Calculate similarity scores for each song
    df['similarity_score'] = df.apply(lambda x: calculate_similarity(x, user_preferences), axis=1)
    
    # Display top 10 songs based on similarity score
    top_songs = df.nlargest(10, 'similarity_score')[['title', 'artist']]
    
    print("\nTop 10 songs that best match your preferences:")
    print(top_songs)

if __name__ == "__main__":
    main()