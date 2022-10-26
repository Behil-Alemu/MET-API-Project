1. What goal will your website be designed to achieve?

    The goal is to create a website that lets users discover artists and art that are displayed in the MIT Museum. The information available can be used as an accurate reference or inspiration for artists. Users can select a timeline, Era, geoLocation, medium, title ….etc to find an art piece. There will also be an option to see if the art is available and displayed at the MIT Museum. Users can create a user account to login and post their artwork  or add a collection of their inspiration in a cart(Like a cart on an online shopping site ). Maybe an option for others to add comments. Their posts can include tags corresponding with the art piece that inspired them. Later on, the website can be developed further so that artists can sell their work by creating a buyer or seller account. 

2. What kind of users will visit your site? In other words, what is the demographic of your users?
    Artist, Art students, or anyone who is interested in art. 
3. What data do you plan on using? You may have not picked your actual API yet,
which is fine, just outline what kind of data you would like it to contain.
    `https://www.notion.so/Capstone-Project-708e70430de14af8b106f8e3475a7277#6a868bbd82ab4f459ec263903f66fb68`
4. In brief, outline your approach to creating your project (knowing that you may not
know everything in advance and that these details might change later). Answer
questions like the ones below, but feel free to add more information:
    -  What does your database schema look like?

**users_table**
| id          | username      |  email             |    Avatar      | social_media      |  bio                     |  password   |
| :---        |    :----:     |      :----:        |   :----:       |    :----:         |     :----:               |    ---:     |
| 1           | "John "       | "john@gmail.com "  |      "url "    | "john_insta"      | "I am an artist"         |  $2b$8gj    |
| 2           | "smith"       | "smith@gmail.com  "|      "url "    | "smith_snap"      | "I want to me an artist" |  $2b$8gg    |

**post_table**
| id      | description         | title         | imageURL|
| :---    |    :----:           |       :----:  |   ---:  |
| 1       | "Art Description"   | " Art title"  |  "url"  |
| 2       | "Art Description"   | "Art title"   |  "url"  |

**likes_table**

| id        | comment       | user_id    |
| :---      |    :----:     |       ---: |
| 1         | "comment"     | FK id      |
| 2         | "comment"     | FK id      |

**inspiration_table**

| id        | object_id     | user_id    |
| :---      |    :----:     |       ---: |
| 1         | 658798597     | FK id      |
| 2         | 879476446     | FK id      |
    

    - What kinds of issues might you run into with your API?
        Some of the information I need might be Null or "" (an empty string). I might have a hard time navigating the nested API. Having to vet through and selecting the information I need might be a challenge. Having access to the API might require API-Key. 
    
    - Is there any sensitive information you need to secure?
        The users password will be the post sensitive Information
    - What functionality will your app include?
        Users can add liked images to their inspiration cart and refer to them later. There will be a functionality to search for images as well as add your own artwork. 
    - What will the user flow look like?
        Welcome page with looping random image and nav bar on top. Next login or signup if desired. If logged in then view other users’ artwork or post your own artwork. If not then,  use the website to look through the art provided by the MIT Museum API. 

f. What features make your site more than CRUD? Do you have any stretch
goals?
*Create*, or add a new post for the image a user uploads and text title and description of their art

*Read*, retrieve, and search entries  from the API 

*Update*, or edit your post or your comment.

*Delete* your post or your comment.
