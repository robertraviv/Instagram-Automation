![python-version]
![Selenium]
![pixabay]

<!-- PROJECT LOGO -->
<br />
<p align="center">
    <img src="src/instagram_bot.png" alt="Logo" width="140">
  </a>
</p>

# Self-Sustained Instagram Automation Bot

Completely self-sustained **hands-free** Instagram automation bot which operates and manages an Instagram account on its own:

* **Creating Unique Posts** 📷 (Really!)
* Uploading posts
* Liking posts
* Following Users
* Unfollowing Non-Followers

The main object is to imitate a real user browsing & use, which randomly performs each task.

**Each post is created by blending two random images from Pixabay latest keyword search results (random search keyword from a list), and adding a text (quote from csv file) to the final blended image result.**

**Each text quote is created by a random chosen font, with a random chosen size and a random chosen color.**

Image size is determined by the smallest width/height size of source images. The images are cropped exactly from the middle of each image to a **perfect square blended image**, suitable for Instagram postings. Example:

![image-creation][image-creation]

## Prerequisites

* Instagram account.
* [Pixabay API](https://pixabay.com/service/about/api/).
* Quotes list (or any other text you want to display on an image post) in a CSV file.

## Getting Started

Add all the relevant credentials in the example.env file and rename it to '`.env`'. include a browser's User-Agent for a **mobile device**, which can be found [online](https://developers.whatismybrowser.com/useragents/explore/operating_platform/pixel/2).

Add popular quotes (or any) list to CSV file (example.csv) and rename file to '`quotes.csv`'.

**That's it! On the default current settings each task is excuted randomly every few hours.**

## Usage (main functions default values)

**Building a new post and posting:**

`Object.newpost()`

**Follow new people with specific attributes:**

`Object.discover_people(follow_max=11, has_max_followers=15000, has_min_followers=450, follow_ratio=2)`

_* follow_ratio=2 attribute is a user's following / followers ratio._

**Unfollow non-followrs:**

`Object.unfollow(unfollow=12)`

**Explore search feed to like posts and follow accounts:**

`Object.explore_like_follow(explore_times=3, to_follow=True)`


## Disclaimer

This was built for educational purposes and any misuse can lead to an Instagram account ban/deletion.

**⚠️Please use at your own risk.**

<!-- CONTRIBUTING -->
## Contributing

Cotributers are welcome to add more features and improvements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[selenium]: https://img.shields.io/badge/built%20With-Selenium-yellow?style=flat-square
[contributers-welcome]: https://img.shields.io/badge/Contributers-Welcome-orange?style=flat-square
[python-version]: https://img.shields.io/badge/python-3.8-blue?style=flat-square&logo=python
[contributors-shield]: https://img.shields.io/github/contributors/
[image-creation]: src/post_img_creation.png
[pixabay]: https://img.shields.io/badge/API-pixabay-success?style=flat-square&logo=pixabay
