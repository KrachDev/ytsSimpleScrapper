import requests
from bs4 import BeautifulSoup

# Function to scrape movie data from YTS website
def scrape_movies(query):
    # Construct the URL
    url = f"https://yts.mx/browse-movies/{query}/all/all/0/latest/0/all"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all movie elements within the 'row' div
        movie_elements = soup.find_all('div', class_='browse-movie-wrap')

        # List to store movie data
        movies = []

        # Loop through each movie element and extract relevant information
        for index, movie in enumerate(movie_elements, start=1):
            title = movie.find('a', class_='browse-movie-title').text
            year = movie.find('div', class_='browse-movie-year').text
            rating = movie.find('h4', class_='rating').text.strip()
            genres = [genre.text for genre in movie.find_all('h4')[1:-1]]
            link = movie.find('a', class_='browse-movie-link')['href']
            
            # Store movie data in a dictionary
            movie_data = {
                "title": title,
                "year": year,
                "rating": rating,
                "genres": genres,
                "link": link
            }

            # Append movie data to the list
            movies.append(movie_data)
            print(f"{index}. {title} ({year}) - Rating: {rating} - Genres: {', '.join(genres)}")

        return movies
    else:
        print("Failed to retrieve data")
        return None

# Function to scrape download links from a movie page
def scrape_download_links(movie_url):
    response = requests.get(movie_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        download_links = soup.find_all('a', class_='download-torrent')
        for link in download_links:
            href = link['href']
            print("Download Link:", href)
    else:
        print("Failed to retrieve download links")

# Example usage:
query = input("Enter your search query: ")
movies = scrape_movies(query)
if movies:
    selection = int(input("Enter the index of the movie you want to download: "))
    selected_movie = movies[selection - 1]
    print("Selected Movie:", selected_movie["title"])
    print("Loading movie page:", selected_movie["link"])
    scrape_download_links(selected_movie["link"])
