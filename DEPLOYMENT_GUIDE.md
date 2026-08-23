# 🚀 How to Deploy Your App for Free to Streamlit Community Cloud

Follow these steps to deploy your Stock Earnings Prediction League to the web so you and your friends can access it from any phone or computer with a public URL (e.g. `https://your-app.streamlit.app`).

---

## Step 1: Push the App to GitHub

1. Open your terminal and navigate to your app directory:
   ```bash
   cd /Users/jianchen/.gemini/antigravity-ide/scratch/earnings-tracker-streamlit
   ```

2. Initialize Git and commit your files:
   ```bash
   git init
   git add app.py requirements.txt league_data.json
   git commit -m "Initial commit of EarningsBeat Streamlit app"
   ```

3. Create a new repository on [GitHub](https://github.com/new) (e.g., named `earnings-prediction-league`).

4. Link and push to GitHub:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/earnings-prediction-league.git
   git branch -M main
   git push -u origin main
   ```

---

## Step 2: Deploy on Streamlit Community Cloud (Free)

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New app"** (or **"Create app"**).
3. Select **"I already have an app"**.
4. Fill in the deployment details:
   - **Repository:** `<YOUR_GITHUB_USERNAME>/earnings-prediction-league`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** (Optional custom subdomain, e.g., `my-earnings-league`)
5. Click **"Deploy!"** 🚀

---

## Step 3: Share the URL with Your Friends

In 1–2 minutes, Streamlit Cloud will build the app and give you a live HTTPS link. 
Share that link with your friends so everyone can cast their predictions from their browser or mobile devices!
