# Educational games for GCSE maths
The project title is Educational games for GCSE maths. The project supervisor is Dr Ian Kenny. The project is a website called 'Just Math It' and the project framework is Flask.

## Project File Structure
- **static**
    
    ***Some of the static files are referenced by [Themeum](http://www.themeum.com/) and  [WrapPixel](https://wrappixel.com/).***
    
    - **CSS**: stores CSS files
    - **JS**: stores JS files
    - **fonts**: stores font files
    - **images**: stores image files
    - **profile**: stores CSS and JS files of profile pages
        - CSS: store CSS files 
        - JS: store JS files
    - **json**: stores generated questions for users
        - wrong: stores questions in question collection for users
    
- **mathgenerator**: for generating math problems

- **templates**: stores HTML files (**Some of the HTML files are referenced by [Themeum](http://www.themeum.com/) and  [WrapPixel](https://wrappixel.com/) and I modified all the displays based on these files**)

- **config.py**: configuration realted parameter files

- **models.py**: stores the SQLAlchemy instance

- **form.py**: defines the form that are used in html files

- **myproject.py**: defines all the routes and functions to perform for each action

- **math.db**: database file

- **requirements.txt**: stores information about all libraries, modules, and packages that are used.

## Address of this website 

This project is deployed on the cloud server, you can visit this website on http://162.62.228.148.

This website has two kinds of actors: 

1. **Teacher** 
2. **Student**

Here, I provide two accounts for this website, one is teacher account, another is student accounts.

- Teacher's account: 
  - email: 1306057972@qq.com
  - password: 123123
- Student's account:
  - email: 1575631865@qq.com
  - password: 123123

Or you can sign up a new account for testing.

## Configuring the Local Environment

If you would like to run the project locally. There are several steps you need to take:

- **Before you do the following things, open your terminal and cd to the project file directory**

1. Creating a virtual environment

   ```python
   python3 -m venv myprojectenv
   ```

2. Activating virtual environment

   ```python
   source myprojectenv/bin/activate
   ```

3. Installing packages using requirements.txt

   ```pyth
   pip install wheel
   pip install flask
   pip install -r requirements.txt --no-cache-dir
   ```

4. Testing

   ```pyt
   python myproject.py
   ```

5. Entering the address on the browser

