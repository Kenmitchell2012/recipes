from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id(session['user_id'])
    # catch for invalid user_id somehow being in session, clear it via logout so user can login
    if not user:
        return redirect('/user/logout')
        
    return render_template('recipes.html', user=user, recipes=user.get_all())

# add a new recipe
@app.route('/add/recipe', methods=['POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect('/login')
    print(session['user_id'])
    if not Recipe.validate_recipe(request.form):
        return render_template('new_recipe.html')
    new_recipe = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],

    }
    # validate the data
    Recipe.add_recipe(new_recipe)
    id_data = {
        'id': session['user_id']
    }
    one_user = User.get_by_id(id_data)
    return redirect('/recipes')

# render create recipe page
@app.route('/recipes/new',methods=['GET'])
def create_recipe_page():
    if 'user_id' not in session:
        flash("Please login","login")
        return redirect('/')
    return render_template('new_recipe.html')

# edit a recipe
@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please login","login")
        return redirect('/')
    id_data = {
        'id': session['user_id']
    }
    one_user = User.get_by_id(id_data)
    
    return render_template('edit.html',recipe=recipe_id,one_user=one_user)

# edit a recipe
@app.route('/recipes/edit/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please login","login")
        return redirect('/')
    id_data = {
        'id': session['user_id']
    }
    one_user = user.User.get_by_id(id_data)
    if not recipe.Recipe.validate_recipe(request.form):
        return render_template('edit.html',recipe=recipe,one_user=one_user)
    new_recipe = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['select'],

    }
    # validate the data
    recipe.Recipe.update_recipe(new_recipe,recipe_id)

@app.route('/recipes/<int:id>')
def get_recipe(id):
    if 'user_id' not in session:
        flash("Please login","login")
        return redirect('/')
    return render_template('view_recipe.html',recipe=recipe.Recipe.get_one_recipe({id: id}))