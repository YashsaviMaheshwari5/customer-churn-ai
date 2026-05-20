# TODO - Railway + (optional) Vercel deployment

## Step 1: Deploy existing Streamlit app to Railway (recommended)
- [ ] Add/confirm Railway start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- [ ] Ensure `model.pkl` and `model_columns.pkl` are included in the repo (committed)
- [ ] Ensure `data/WA_Fn-UseC_-Telco-Customer-Churn.csv` exists and is included (or refactor to avoid requiring it)

## Step 2: (If needed) Make Streamlit deploy more robust
- [ ] Refactor `my_pages/prediction.py` to use `model_columns.pkl` for feature schema instead of loading the CSV

## Step 3: (Only if you want the original split) API on Railway + Next.js on Vercel
- [ ] Create FastAPI backend endpoint `/predict`
- [ ] Create Next.js frontend that calls the API
- [ ] Deploy backend to Railway and frontend to Vercel

