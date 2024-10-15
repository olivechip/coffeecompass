# Coffee Compass

**[Deployment TBD]**

Coffee Compass is a simple web application that helps coffee enthusiasts discover and keep track of their favorite local coffee shops. 

## Features

* **User Authentication:** Secure user registration and login with password hashing.
* **Coffeeshop Search:** Search for coffee shops by location using the Yelp API.
* **Favorites:**  Save your favorite coffee shops for easy access later.
* **User Profiles:** View your favorite coffeeshops on your profile page.

**Why these features?**

These features provide a core set of functionalities for a coffee discovery app. User authentication ensures secure access to personalized features like favorites. The Yelp API integration provides a robust way to access coffee shop data, and the favorites feature allows users to curate their own lists of preferred spots. User profiles provide a personalized space for users to manage their favorite coffee shops.

## User Flow

1. **Landing Page:**  Users are presented with a search bar to enter a location.
2. **Search Results:**  After searching, users see a list of coffee shops from the Yelp API, including their name, address, phone number, rating, and an image.
3. **Authentication:** Users need to register or log in to add coffee shops to their favorites.
4. **Add to Favorites:**  Logged-in users can click a button to add a coffee shop to their favorites.
5. **Profile Page:** Users can view their saved favorite coffee shops on their profile page.
6. **Remove from Favorites:** Users can remove coffee shops from their favorites list on their profile page.

## API Integration

Coffee Compass uses the Yelp Fusion API to search for coffee shops. The API provides comprehensive data about businesses, including location details, contact information, ratings, reviews, and photos.

## Technology Stack

* **Backend:** Python, Flask
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS, JavaScript
* **Form Handling:** WTForms
* **Password Hashing:** bcrypt
* **API:** Yelp Fusion API

## Future Plans

* **Account Customization:**  Allow users to edit their profiles, also add a bio and location. 
* **Visited Feature:**  Add a "visited" feature to allow users to mark coffee shops they have visited.
* **Reviews/Ratings:**  Allow users to add their own notes on coffee shops.
* **Recommendations:** Implement a recommendation system to suggest new coffee shops based on user preferences and location.
* **Maps Integration:**  Integrate a map to visually display coffee shop locations.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License
TBD