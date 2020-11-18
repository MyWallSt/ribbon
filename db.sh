export FLASK_APP=gifting.py
export SECRET_KEY="jk93unKsdn@*#jsd10170KJA"

export FLASK_ENV=development;
export FLASK_DEBUG=1;

export STRIPE_SECRET_RESTRICTED_KEY=rk_test_51DpwIJG2ErA65p3lLY9INvuUrZaozxD1UpRwqrWPKTwGRxWAfZCqA1wMMr3LOTVVoYvLgbIVhly9EcyI2aPSYYRD005XCD89LP
export STRIPE_SECRET_KEY=sk_test_t6zMjPp5WgSSYDoKI3M02sir00jCSXWiTu
export STRIPE_PUBLIC_KEY=pk_test_GIRYxB9FdJjp1Tw0T12NjKi4
export STRIPE_MYWALLST_PLAN_ID=price_1HkWfYG2ErA65p3l0AcJfExg;

export SMTP_HOST='smtp.gmail.com';
export SMTP_PORT=465;
export SMTP_SECURE='ssl';
export SMTP_AUTH=true;
export SMTP_USERNAME="hello@mywallst.com";
export SMTP_PASSWORD='afseclmslujscuhq';
export SENDER_EMAIL="hello@mywallst.com";
flask db upgrade;
