# Flask Machine Learning Competitions Web App

## Overview
This web application allows users to participate in machine learning competitions. Users can log in, upload their predictions, and view leaderboards.

## Setup

### Prerequisites
- Python 3.8
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Initialize the application:
- On Windows:
    ```cmd
    init_app.bat
    ```
- On Unix-based systems:
    ```bash
    ./init_app.sh
    ```

3. Start the application:
- On Windows:
    ```cmd
    start_app.bat
    ```
- On Unix-based systems:
    ```bash
    ./start_app.sh
    ```

## Resetting the application
This will update all users, competitions as defined in `add_initial_data.py` and wipe the leaderboards.
- On Windows:
    ```cmd
    reset_app.bat
    ```
- On Unix-based systems:
    ```bash
    ./reset_app.sh
    ```

## Testing
- On Windows:
    ```cmd
    run_tests.bat
    ```
- On Unix-based systems:
    ```bash
    ./run_tests.sh
    ```

## Adding competitions and users.
In `add_initial_data.py`, add a new user under `# Create Users`, using the following template:

```python
    # Create Users
    hashed_password = bcrypt.generate_password_hash('new_password').decode('utf-8')
    user_n = User(username='new_user', password=hashed_password)
```

In `add_initial_data.py`, add a new competition under `# Create Competitions`, using the following template:

```python
    # Read true values from files
    true_values = read_true_values('y_values.csv') 
    # Create Competitions
    competition_n = Competition(
        name='competition_n',
        description='Predict the credit card scores.', #
        image_path='app/tatic/images/competition_n.png', # reads a png belonging to the competition
        true_values=true_values, # loads the 
        is_classification=False # decides whether to use F1 score, if classification or MSE if regression
    )
```

Don't forget to update the the push to the database in `add_initial_data.py` with the new objects as well:
```python
    db.session.add_all([user_n, competition_n])
    db.session.commit()
```

## Azure Web App deployment
1. Install Azure CLI for Windows and log in:
    ```bash
    curl -sL https://aka.ms/InstallAzureCLIDeb | bash
    az login
    ```
2. Create an Azure App Service Plan:
    ```bash
    az group create --name myResourceGroup --location "West EU"
    az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku FREE
    ```  
3. Create a Web App:
    ```bash
    az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name mlScoringWebApp --runtime "PYTHON|3.8"
    ```  
4. Deploy the app using Git:
- Initialize Git:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```  
- Set the remote and push to Azure:
    ```bash
    az webapp deployment source config-local-git --name mlScoringWebApp --resource-group myResourceGroup
    git remote add azure <URL provided by the previous command>
    git push azure master
    ```  
5. Configure environment variables:
    ```bash
    az webapp config appsettings set --resource-group myResourceGroup --name mlScoringWebApp --settings FLASK_APP=run.py FLASK_ENV=production
    ```  
6. Access the applet
- The application should now be accessible at `https://mlScoringWebApp.azurewebsites.net`.

## Participating in competitions
Uploading csv's is straightforward and the following format is expected:
```
y
1
0
1
1
0
...
```
## Known bugs / issues
- Users won't receive an error message when the login fails. They will be redirected to the login.
- The tests have not been tested.
- Using `add_initial_data.py` is not very elegant. Plus the location of the content associated with  a competition (Title, description image, true vales) needs refactoring.
- Deployment to an Azure Web App has not been tested.
