# Expense-tracker-backend
This the expense tracker web app made using Django RestFrame work using various azure services
List of azure serives used:-
1)App services plan
2) App services
3) Azure SQL DATABASE
4) Queue storage and blob storage
5) Queue storage is used as a queue trigger for azure functions
6) 

How to use 
python manage.py makemigration
python manage.py migrate
pip install ir requirements.txt
Provide all the enviorment variable asked on expense/settings.py and expense/expense_api/queues.py that are connection strings, storage account links,containers name and database credentials

git commands
echo "# Expense-tracker-backend" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/killer1503999/Expense-tracker-backend.git
git push -u origin main
