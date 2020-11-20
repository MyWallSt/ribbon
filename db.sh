export FLASK_APP=gifting.py >> .env
export SECRET_KEY="jk93unKsdn@*#jsd10170KJA" >> .env

export FLASK_ENV=development >> .env
export FLASK_DEBUG=1 >> .env

export STRIPE_SECRET_RESTRICTED_KEY=rk_test_51DpwIJG2ErA65p3lLY9INvuUrZaozxD1UpRwqrWPKTwGRxWAfZCqA1wMMr3LOTVVoYvLgbIVhly9EcyI2aPSYYRD005XCD89LP >> .env
export STRIPE_SECRET_KEY=sk_test_t6zMjPp5WgSSYDoKI3M02sir00jCSXWiTu >> .env
export STRIPE_PUBLIC_KEY=pk_test_GIRYxB9FdJjp1Tw0T12NjKi4 >> .env
export STRIPE_MYWALLST_PLAN_ID=price_1HkWfYG2ErA65p3l0AcJfExg >> .env

export SMTP_HOST='smtp.gmail.com' >> .env
export SMTP_PORT=465 >> .env
export SMTP_SECURE='ssl' >> .env
export SMTP_AUTH=true >> .env
export SMTP_USERNAME="hello@mywallst.com" >> .env
export SMTP_PASSWORD='afseclmslujscuhq' >> .env
export SENDER_EMAIL="hello@mywallst.com" >> .env
flask db upgrade;