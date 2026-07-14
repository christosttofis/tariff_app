To start it:

From inside the tariff-api folder:


python -m uvicorn main:app
Then open http://localhost:8000/admin.html or http://localhost:8000/customer.html.

No --reload — it breaks POST requests on Python 3.14.

Then navigate to:
http://localhost:8000/admin.html
http://localhost:8000/customer.html

To reset password:
Run create_user.py with the same email — it will prompt you to confirm an update, then let you set a new password:


cd 'c:\Users\pkoussi\OneDrive - Cyprus Energy Regulatory Authority\Desktop\Claude\Tariff backend\tariff-api'
python create_user.py --email admin@cera.gov.cy --role admin
It will ask:


User admin@cera.gov.cy already exists. Update password and role? [y/N]
Type y, then enter the new password. No server restart needed — the new hash is written straight to the DB.