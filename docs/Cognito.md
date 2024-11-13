
# Cognito 

1. **Create A User Pool**
   - Click "Create user pool"
   - Check "User name" and "Email" under "Cognito user pool sign-in options"
   - Click Next
   - For our deployment we used "Cognito defaults"
   - In "Multi-factor authentication" select "No MFA" in "Password Policy"
   - Leave all settings in "User account recovery" default
   - Click Next
   - Leave all defaults on next page
   - Click Next
   - In "Email" for this small app choose "Send Email with Cognito"
   - Click Next
   - Choose a User Pool Name
   - Click "Use a Cognito Hosted UI"
   - In "Domain" choose "Use a Cognito domain"
   - Choose a name for your domain
   - Leave "App Type" as "Public Client"
   - Choose App Name
   - Leave "Don't generate a client secret" Chosen
   - For now leave "Allowed callback URLs" as "http://localhost" for now but it will be changed later
   - Click Next
   - Review that all settings are okay and click Create user pool
     
2. **App Integration**
   - On the right select "User pools"
   - Click on your named user pool
   - Scroll down and over to "App Integration"
   - Scroll to the bottom of the page and under "App client list" click your "App client name"
   - Click on "Edit" in Hosted UI and change url in "Allowed callback URLS" to your "https://'API Gateway Invoke URL'/'Stage name'/callback"
   - Click Save Changes
