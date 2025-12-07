# FoodLink
A food redistribution web app to reduce food waste.
By: Blaudschun Beauvoir, Deylis Cano Morera, Monisha Kummari, & Akul Singh

## Built Using:
- Flask for the Back-End.
- React for the Front-End.
- SQLite for the Database.

## Setup
- For a step-to-step guide, there is a [setup.txt](docs/setup.txt) file in the `docs` folder.
- After setting up you can run the code by doing the following:
    - Have 2 terminals open making sure they are in the root directory.
    - in one terminal, cd `backend` and then `flask run`.
    - in the other terminal, cd `frontend` and then `npm start`.

## Implemented Features
- The website currently has the capability of doing the following:
    - Public Endpoints
        - Login
        - Register
    - Available to any Logged in User:
        - Edit Profile
        - View Requests
        - Forgot Password
    - Donor Endpoints
        - Create Donations
        - My Donations
    - Recipient Endpoints
        - Available Donations
        - Filter Donations
    - Admin Endpoints
        - Available Donations
        - Admin Access to User Management
        - Manage Donations

## Creating a Donation
- Create a donor account via the register account.
- Login.
- There should now be a *Create Donation* link in the navbar.
- Create the donation.
- Go to *My Donations* and you should now see the donation is pending.

## Semi-Implemented Features
- Request
    - Currently works by just letting recipients claim donations and we have a empty Requests page for now.
    - Requires an entire new model inside the database
    - Lets users request for certain foods that are not listed in donations
    - Donators should be able to see and donate for it.
        - Need to account for it donators can only send partial parts of it.
        - Negotiating if they have a different type.

## To Do Features
- Set-up an email service to properly send emails for registration.
- Messages between Donors and Recipients.
- Re-activate users.
- Send notifications for accepted/rejected donations.
- Let recipients see a history of their claimed donations.
- Tracking donations.
- Recipients can request anything rather than looking through only available donations.
- Location based availability.

# Paper
- Please find the paper covering the FoodLink app in the `docs` folder.

