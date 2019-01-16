# Reseptivihko - RecipeApp
## Description
This is a web application created as course work for the course Tietokantojen harjoitustyö (Database excercise project).

The basic idea of the application is for users to be able to add and browse recipes.

Application users are able to register user accounts that they can log in with, add and edit their own recipes. Users with admin rights are able to edit any recipe or tag.

Recipes contain information such as name, preparation time, ingredient description and instructions. Users are also able to mark their recipes with tags of their choosing, and browse recipes by tags.

## Instructions for use
### Front page and navigation
Upon accessing the front page of the site, you are greeted with a welcome, short description and some site statistics. The navigation bar is located at the top of the site, and provides links to add a recipe, to view a list of all recipes and to browse tags associated with recipes. If user is not logged in, a possibility for doing so, or creating a new account is visible in the right corner of the navigation bar. If user is logged in, username and logout link is shown.

Without logging in, visitors can browse recipes added by others, and tags associated with recipes. If user wants to create their own recipe, login is required.

### User creation and logging in
Creating user is done by clicking the link "Create an accunt!" shown on the right corner of the navigation bar, when user is not signed in. This takes user to the account creation form, where user can choose their own username and password. Account credentials must follow these rules:

* Username must be unique
* Username must between 3 and 16 characters long
* Password must be between 8 and 144 characters long
* Password must contain both letters and numers
* Password must contain both uppercase and lowercase letters
* Password must match the password re-written in the "Re-type password"-field

If the credentials submitted by user do not meet these rules, the form is not accepted, and displays error messages to explain what rule is not met. After choosing suitable credentials, user-account is created, signed in and redirected to the front page of the site. From there, user can start accessing functionality that requires being logged in, I.E. adding and editing recipes.

If user already has an account they can log in by clicking the "Log in" link in the navigation bar that leads them to a log in form.

Once logged in, the right corner links of the navigation bar are replaced with the username of the logged in account, and a link to sign them out.

### Recipe list and individual recipe view
The "Recipe list"-link in the navbar leads users to (surprisingly) a list of recipes added into the application database. The list shows the name of the recipe, and the preparation time for that recipe. By clicking a name of a recipe, the user is led to a view of the recipe. This view contains all the information about the recipe: its name, creator, preparation time, ingredients that are needed, instructions for making the dish and lastly identifier tags that have been associated with the recipe. By clicking one of these tags, users can see other recipes associated with the tag. If the recipe that is viewed is created by the same user that has logged in, or logged in user is admin, a possibility to edit the recipe is shown.

### Creating and editing a recipe
Adding a recipe is done by clicking "Add a recipe" from the navigation bar. This opens a form that takes in all of the recipe information. Recipe information must meet following requirements:

* Name of the recipe must be unique
* Name of the recipe must be between 3 and 64 characters long
* Preparation time must be entered, and must be a number
* Each line of ingredients must be between 3 and 140 characters long
* Instructions must be between 10 and 6000 characters long
* Each tag must be between 3 and 18 characters long

If these requirements are not met, the form will show according error messages.

Users can separate different ingredients with linebreaks. This way ingredients are shown in a list form. Similarly adding multiple tags is possible by separating different tags with a comma.

Users can submit the recipe by pressing "Add recipe". On adding the recipe, different pieces of recipe information are ensured to have some spesific form. These include:

* Leading and trailing whitespace is removed from all fields
* Recipe name is forced to begin with a capital letter
* Ingredient lines are forced to begin with a capital letter
* Tags are forced to begin with a capital letter, and be otherwise lowercase

To edit a recipe, user must be the creator of said recipe, or be an admin. Editing form is opened from the individual recipe view. The editing form contains all of the same fields that the recipe creation form, but is preloaded with the values of the recipe being edited. Editing form also contains the possibility to remove the recipe. Edited recipe must pass same validations as a new recipe.

### Tag list and individual tag view
A list of tags is found under the "Browse tags" link on the navbar. This view contains a list of tags that have been added, and the amount of recipes belonging to each tag. This list is shown in descending order.

By clicking a tag name on the list, user is directed to a site containging a list of all the recipes that the tag is associated with. From there, user can navigate to view these recipes. Tags can also have descriptions added by administrators, to further describe recipes belonging to the tag. From this view, administrators are able to detach any recipes they deem unfit from the tag.

By default, users are not able to create tags in other ways than adding a previously unused tag to a recipe. However admins are capable of creating tags without any recipes. This functionality could be used for example to format the tag list with pre-meditated tag-names and descriptions to inspire and help users use tag functionality.

## Documentation
Various documentation about the project is located in the [documents-folder](../master/documentation) of the repository. Here are links to some key documentation:

* [Database diagram](../master/documentation/database_diagram.md)

* [User stories](../master/documentation/user_stories.md)

* [Running your own instance](../master/documentation/startup_guide.md)
      

## Application on Heroku
Application is running on Heroku at: https://reseptivihko.herokuapp.com

For testing purposes, feel free to use following admin-credentials:

__username:__  admin
__password:__ password

For basic user functionality, you can create your own user-account. Please note that at this time, passwords are stored in the application database as plain text.