
**Schema Design Capstone-1**					

**users_table**
| id          | username      |  email             |    Avatar      | social_media      |  bio                     |  password   |
| :---        |    :----:     |      :----:        |   :----:       |    :----:         |     :----:               |    ---:     |
| 1           | "John "       | "john@gmail.com "  |      "url "    | "john_insta"      | "I am an artist"         |  $2b$8gj    |
| 2           | "smith"       | "smith@gmail.com  "|      "url "    | "smith_snap"      | "I want to me an artist" |  $2b$8gg    |

**post_table**
| id      | description         | title         | timestamp |imageURL |user_id  |
| :---    |    :----:           |       :----:  |   :----:  |  :----: |   ---:  |
| 1       | "Art Description"   | " Art title"  | timestamp |  "url"  |  FK id  |
| 2       | "Art Description"   | "Art title"   | timestamp |  "url"  |  FK id  |

**likes_table**

| id        | post_id       | user_id    |
| :---      |    :----:     |       ---: |
| 1         | FK id         | FK id      |
| 2         | FK id         | FK id      |

**inspiration_table**

| id        | object_id     | user_id    |
| :---      |    :----:     |       ---: |
| 1         | 658798597     | FK id      |
| 2         | 879476446     | FK id      |
    