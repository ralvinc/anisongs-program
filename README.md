# AniSongs Program

This program offers a streamlined approach to adding anime themes to one of the user's YouTube playlist, further simplifying the process compared to the previous AniSongs web application.

Instead of being redirected to a YouTube page displaying video search results for a chosen anime theme, this program leverages the YouTube Data API and OAuth to directly add the desired YouTube video of the anime theme to one of the user's playlists. This eliminates the extra steps and enables immediate playlist management.

<p align="center">
    <img src="https://github.com/ralvinc/anisongs-program/assets/126153932/b8755aed-d828-46ad-a24f-20be9676e61e" alt="Material Bread logo">
</p>
  
## Prerequisites

Before running the program, ensure that you have the following prerequisites:

- Python installed on your machine.
- A valid YouTube Channel
- OAuth Client ID 

Python dependencies can be installed using the following command:

    pip install google-auth google-auth-oauthlib google-auth-httplib2 requests
    
## OAuth Client ID Setup

To set up the OAuth Client ID using the Google Cloud Console, follow these steps:

1. Go to the **[Google Cloud Console](https://console.cloud.google.com/)** and log in to your Google account.

2. Select *Credentials* under the *APIs & Services* tab.

3. Create a new project.

4. Under the *APIs & Services* tab, select *OAuth consent screen*.

5. Fill in the necessary information and manually add **https://www.googleapis.com/auth/youtube.force-ssl** in the *Scopes* tab. Also, add all the Gmail accounts you wish to access with the YouTube API in the *Test Users* tab.

6. Go back to *Credentials* and create an **OAuth client ID**.

7. Select *Web Application* as the application type and add **http://localhost:8000/** to the Authorized redirect URIs.

8. Download the OAuth client ID file, place it in the same directory as the code, and rename it to **client_secrets.json**.

9. Select *Enabled APIs & services* under the *APIs & Services* tab.

10. Search for *YouTube Data API v3* and **enable** it.

## Installation and Usage

To install this project, download or clone the repository to your local machine:

    git clone https://github.com/ralvinc/anisongs-program.git

After downloading the code, follow the instructions provided in the program to interact with it.

## Built with

Python

## Author
This project was created by **Ralvinc**.

## Acknowledgments
Anime Data from **JIKAN API v4** \
YouTube Data from **YouTube Data API v3** \
Authentication using **OAuth 2.0**
