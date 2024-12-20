python3 -m venv .venv
# mac or linux users
#source .venv/bin/activate
# windows
#.venv\\Scripts\\activate
cd backend
# mac or linux users
#cp .env.example .env
# windows
#copy .env.example .env
pip install -r requirements.txt
python manage.py migrate
python manage.py create_system_user
python manage.py loaddata ingredients.json product_ingredients.json products.json
python manage.py runserver