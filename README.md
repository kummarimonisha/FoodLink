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
- Claim donations by Recipients
    - Implemented on Back-end, needs to be done on Front-end
    - Involves listing available donations to recipients.
    - Let the recipient claim a donation.
    - Updates Database/Donation data.
    - Updates Available Donation page.
    - Gives a confirmation of Accepted Donation.

## To Do Features
- Set-up an email service to properly send emails for registration.
- Messages between Donors and Recipients.
- Re-activate users.
- Send notifications for accepted/rejected donations.
- Let recipients see a history of their accepted donations.
- Tracking donations.
- Recipients can request anything rather than looking through only available donations.

# Paper
- Please find the paper covering the FoodLink app in the `docs` folder.

