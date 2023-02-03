
# Coffee Crew


## Table of Contents

## Introduction

The project is an E-commerce site for a shop selling specialty coffee equipment.

Users can register to submit resources to the directory, and upvote and bookmark resources they find useful.

The project was built keeping the Agile management principles in mind, and I utilised many of GitHub's features such as Issue and Projects to implement Scrum methodology.

[Kanban Board for project](https://github.com/users/davidindub/projects/8/)

[Closed Issues on GitHub for the project](https://github.com/davidindub/coffeecrew/issues?q=is%3Aissue+is%3Aclosed)

I used [GitHub issues](https://github.com/davidindub/coffeecrew/issues) for the product backlog containing the user stories. Issues were also used for bug reports so I could keep track of tricky bugs over time.


I used the tags feature in GitHub Issues for assigning story points, prioritising features based on [the MoSCoW method](https://en.wikipedia.org/wiki/MoSCoW_method), and categorising the user stories.

I used the [Milestones feature](https://github.com/davidindub/coffeecrew/milestones) to plan sprints and set deadlines.


## User Stories

User stories were prepared using GitHub Issues and assigned story points based on estimated completion time.

User Stories can been seen below under [User Story Testing](#user-story-testing), and in the [GitHub Issues](https://github.com/davidindub/coffeecrew/issues?q=is%3Aissue+is%3Aclosed) for full details including screenshots, story points and associated sprints.


## UX  


### Typography



### Wireframes


## Accessibility

I ensured that every element met AAA level in the [Web Content Accessibility Guidelines](https://www.w3.org/WAI/WCAG2AAA-Conformance) (WCAG).

Buttons featuring icons have appropriate `aria-labels`, and notification messages have `aria-live` tags and are read by screen readers.

I tested navigating the project with VoiceOver on macOS.

I used inline SVGs for icons in the project.

I recently watched [Seren Davies](https://github.com/ninjanails)' talk [Death to Icon Fonts](https://www.youtube.com/watch?v=9xXBYcWgCHA) where I learned of the issues that icon fonts can cause for accessibility. I researched the best way to use inline SVG icons, including descriptions where appropriate for screen readers. By using SVGs the icons don't break if a user chooses to use a custom font such as [Dyslexie](https://www.dyslexiefont.com/).

See also:
- [Inline SVG vs Icon Fonts - CSS Tricks](https://css-tricks.com/icon-fonts-vs-svg/)
- [SVG, Icon Fonts, and Accessibility: A Case Study - 24 Accessibility](https://www.24a11y.com/2017/svg-icon-fonts-accessibility-case-study/)

## Database Design

I used [Miro](https://miro.com/) to design the models. I created a Profile model to associate extra information with users not included in the default Django user model. 

![Database Diagram](/docs/images/database-diagram.jpg)


## Features 


## Existing Features

### Landing Page



### Navbar


### Register / Login

Users can either sign up using their Google or directly on the site.

Users signing up with Google just need to pick a username, and don't need to create a password.

Users who have previously registered with Google can easily sign in again with one click.


### Wishlist

Users can save products to a wishlist for future reference.


### Footer

The Footer includes:
- A link back to the homepage
- Copyright information
- A link to the Privacy Policy
- A link to the [GitHub repository for the project](https://github.com/davidindub/coffeecrew).

### Privacy Policy

As the project can collect data from users, I included a Privacy Policy link in the Footer which explains how data may be used. I used [GDPR.eu](https://gdpr.eu/) for help writing the policy.

See:
[Writing a GDPR-compliant privacy notice (template included)](https://gdpr.eu/privacy-notice/)

### Notifications

Django Messages and Bootstrap's Toast elements were combined to make elegant notification messages when the user performs actions.


### Staff Only Features


### Custom Error Pages

Custom error pages were added for 403, 404, and 500 errors.


### Favicon


### Features Left to Implement


## Technologies Used

- [Python](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/) for installing Python packages.
- [Git](https://git-scm.com/) for version control.
- [Sourcetree](https://www.sourcetreeapp.com/) for managing the remote repository.
- [GitHub](https://github.com/) for storing the repository online during development.
- GitHub Projects was invaluable throughout the project and helped me keep track of things to do and bugs to fix - you can see [the project's board here](https://github.com/users/davidindub/projects/8).
- [GitPod](https://gitpod.io/) as a cloud based IDE.
- [Balsamiq](https://balsamiq.com/wireframes/) for wireframing.
- [Bootstrap 5](https://getbootstrap.com/) as a front end framework.
- [Google Chrome](https://www.google.com/intl/en_ie/chrome/), [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/) and [Safari](https://www.apple.com/safari/) for testing on macOS Monterey.
- [Microsoft Edge](https://www.microsoft.com/en-us/edge) for testing on Windows 11.
- [Safari](https://www.apple.com/safari/) on iOS and iPadOS 15.
- [Google Chrome](https://www.google.com/intl/en_ie/chrome/) on Android 12.
- [Miro](https://www.miro.com/) for drawing database diagrams.
- [Copy.ai](https://www.copy.ai/) for inspiration for some of the slogans and headlines.
- [favicon.io](https://favicon.io/favicon-generator/) to make a favicon for site.
- [Device Frames](https://deviceframes.com/) for the device mockups in this README.
- [Meta Tags](https://metatags.io/) to prepare the Meta tags for social media share previews.

## External Python Packages Used


## Testing 

I performed manual testing continuously as the project was being developed, and filed [bug reports on GitHub](https://github.com/davidindub/designland/issues?q=is%3Aissue+is%3Aclosed+label%3Abug) as issues were discovered to keep track of bugs. I kept track of how to recreate bugs, expected behaviour, screenshots of the issue and how it was resolved to help myself in future.


### Browser Compatibility


### Responsiveness 


### Performance Testing


### Accessibility Testing


### User Story Testing


### Challenges Faced

### Code Validation

#### HTML Validation


#### CSS Validation


#### Python Validation


#### JavaScript


***


## Deployment

### Local Deployment

<!-- TODO: Add AWS deployment instructions -->


In order to make a local copy of this project, you can clone it. In your IDE Terminal, type the following command to clone my repository:

- `git clone https://github.com/davidindub/coffeecrew.git`


Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/davidindub/coffeecrew)

***

After cloning or opening the repository in Gitpod, you will need to:

1. Create your own `env.py` files in the root level of the project:

```
os.environ["DATABASE_URL"] = "postgres://"
os.environ["SECRET_KEY"] = "YOUR_DJANGO_SECRET_KEY"
os.environ["HEROKU_HOSTNAME"] = "URL_OF_PROJECT_DEPLOYED_ON_HEROKU"
os.environ["DEVELOPMENT"] = "True"
```
**Ensure the `env.py` file is added to your `.gitignore` file so it doesn't get pushed to a public repository.

If you don't have an AWS account already, you will need to [Sign Up for Free](https://aws.amazon.com/) to host the static files in the project.

2. Run `pip3 install -r requirements.txt` to install required Python packages.

3. Migrate the database models using:
`python3 manage.py migrate`

4. Create a superuser with your own credentials:
`python3 manage.py migrate`

5. Run the Django sever:
`python manage.py runserver`
The address of the server will appear in the terminal window.
Add /admin to the address to access the Django admin panel using your superuser credentials.

### Heroku Deployment
<details>

<summary>
Full Instructions on deploying to Heroku
</summary>

Sign up to [Heroku](https://heroku.com/) for free if you don't already have an account.

1. Create a new app in Heroku.

2. In the Resources tab of your app in the Heroku dashboard, click Add-Ons and select Heroku Postgres. Select Hobby Dev - Free as your plan.

3. When Heroku Postgres is installed, click the Settings tab in the Heroku Dashboard.
Click Reveal Config Vars, and add the same variables from your `env.py` file here, except for `DEBUG`, as you don't want debug mode on the deployed project.

4. Copy the value of `DATABASE_URL` from the Config Vars. In your `settings.py` file, comment out the default database configuration, and add a new one with the Postgres url.

```
DATABASES = {
    'default': dj_database_url.parse('your DATABASE_URL here'))
}
```

5. Migrate the database models using:
`python3 manage.py migrate`

6. Create a superuser with your own credentials:
`python3 manage.py migrate`

7. Create a file called `Procfile` (no extension) containing the following:
```
web: gunicorn designland.wsgi
```

8. Run `pip3 install -r requirements.txt` to install required Python packages.

9. Add the url of your Heroku app (for example 'designland.herokuapp.com') to your `env.py` file in the local deployment, and to the Config Vars in your Heroku deployment.

10. Disable collect static so that Heroku doesn't try to collect static files when you deploy by typing the following command in the terminal

```
heroku config:set DISABLE_COLLECTSTATIC=1
```

11. Stage and commit your files to GitHub
```
git add . 
git commit -m "Commit message"
git push
```

12. In the Heroku dashboard for your App, select Deploy.
Under Deployment Method, choose GitHub and search for your repository and click Connect.

13. Select Enable Automatic Deployments, and then Deploy Branch. Heroku will build the App from the branch you selected.

14. Now whenever you push your commits to GitHub, Heroku will rebuild the application.

</details>

<!-- TODO: Add a table with the config vars needed for Heroku deployment -->


### django-aullauth Setup

You need to use your own [Google Cloud](https://cloud.google.com/) credentials to set up `django-allauth`.

The [django-allauth documentation](https://django-allauth.readthedocs.io/en/latest/providers.html) provides instructions for how to complete setup in your Google Cloud Console settings.

*** 

## Credits 

### Content 
- [Writing a GDPR-compliant privacy notice (template included)](https://gdpr.eu/privacy-notice/)


### Media

- [Bootstrap Icons](https://icons.getbootstrap.com/) were used extensively in the project.
- Hero Image by [Rodrigo Flores](https://unsplash.com/@rodrigoflores_photo?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/sn87TQ_o7zs?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText).
  


### Acknowledgements

