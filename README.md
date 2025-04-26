# Trend Social Pulse

**Trend Social Pulse** is a cloud-deployed Flask web application that performs sentiment analysis on Reddit discussions for any product or topic across a selected year. It visualizes trends using AI-powered sentiment categorization and presents interactive charts to analyze public perception over time.

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge)](https://trend-social-pulse.onrender.com)

---

## Features

-  **Reddit Integration** using PRAW to fetch relevant posts
-  **Sentiment Analysis** powered by TextBlob
-  **Data Visualizations** with Matplotlib (Pie, Bar, Line charts)
-  **Cloud Storage** with Cloudinary for hosting generated plot images
-  **Fully deployed on Render** — accessible anywhere

---

## 📌 Use Cases

- ✅ Track how a product's reputation changed over a year
- ✅ Visualize seasonal patterns in public opinion
- ✅ Identify best/worst months for public perception
- ✅ Support marketing insights with Reddit-sourced data

---

## Tech Stack

| Layer        | Tech                        |
|--------------|-----------------------------|
| **Frontend** | HTML, CSS (via Flask Jinja) |
| **Backend**  | Python (Flask), PRAW        |
| **AI/ML**    | TextBlob for sentiment      |
| **Cloud**    | Render (App hosting), Cloudinary (image hosting) |
| **Data**     | Reddit posts via PRAW       |

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Harimhs/Trend-Social-Pulse.git
cd Trend-Social-Pulse
