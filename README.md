# Website Traffic Summary

**Veda Technology Internship · Data Analytics Track · Task 33 (Level 1)**

A basic web analytics project: visits analyzed by traffic source, day, and device, with a traffic summary and a dashboard.

![Dashboard](charts/dashboard.png)

## Repository contents

| File | Description |
|------|-------------|
| `traffic_data.csv` | Daily sessions by source and device, Oct 1-31, 2026 (465 rows) |
| `generate_data.py` | Creates the sample dataset (reproducible, seed 33) |
| `analysis.py` | Python analysis: KPIs by source, device, weekday and day; builds the dashboard image and Excel workbook |
| `website_traffic_summary.xlsx` | Excel: `Dashboard` (KPI tiles + 5 charts), `Summary` (formula tables), `Traffic Data` |
| `charts/dashboard.png` | Dashboard image |
| `power_bi_guide.md` | Steps and DAX measures to rebuild the dashboard in Power BI |
| `README.md` | Approach and outcome (this file) |

## Dataset
Columns: `Date`, `Source` (Organic Search, Direct, Social, Email, Referral), `Device` (Desktop, Mobile, Tablet), `Sessions`, `Pageviews`, `Bounced Sessions`, `Conversions`.
This is **sample data generated for the exercise**, not real website data.

## Approach
1. Defined KPIs: Sessions, Pageviews, Pages/Session, Bounce Rate, Conversions, Conversion Rate.
2. **Compared sources**: sessions, bounce rate and conversion rate per source.
3. **Checked the daily trend**: daily sessions plus a 7-day moving average to separate real trend from day-to-day noise.
4. Split the results by **device** and **weekday**.
5. Built the Excel summary with `SUMIFS` formulas (so it updates with the data), native Excel charts, and a Python dashboard image. A Power BI version is described in `power_bi_guide.md`.

## Traffic summary

| Metric | Value |
|--------|------:|
| Sessions | 33,591 |
| Pageviews | 99,103 |
| Pages / session | 2.95 |
| Bounce rate | 43.4% |
| Conversions | 1,188 |
| Conversion rate | 3.54% |

| Source | Sessions | % of sessions | Bounce rate | Conv. rate | % of conversions |
|--------|---------:|--------------:|------------:|-----------:|-----------------:|
| Organic Search | 12,367 | 36.8% | 42.6% | 3.46% | 36.0% |
| Direct | 7,726 | 23.0% | 36.4% | 4.89% | 31.8% |
| Social | 7,038 | 21.0% | 58.5% | 1.14% | 6.7% |
| Email | 3,802 | 11.3% | 30.7% | 6.05% | 19.4% |
| Referral | 2,658 | 7.9% | 45.4% | 2.71% | 6.1% |

| Device | Sessions | Bounce rate | Conv. rate |
|--------|---------:|------------:|-----------:|
| Mobile | 16,039 (47.7%) | 47.8% | 2.84% |
| Desktop | 15,523 (46.2%) | 38.8% | 4.32% |
| Tablet | 2,029 (6.0%) | 43.0% | 3.10% |

## Key insights
1. **Volume and quality are different things.** Social brings 21% of sessions but only 6.7% of conversions (1.14% conversion rate, 58.5% bounce rate). Email is the smallest big source (11.3% of sessions) but converts best at 6.05% and delivers 19.4% of all conversions.
2. **Mobile is half the traffic but converts worse.** Mobile has 47.7% of sessions, a 47.8% bounce rate and a 2.84% conversion rate, versus 38.8% and 4.32% on desktop. The mobile experience is the clearest place to improve.
3. **The daily trend is flat apart from a few spikes.** The 7-day average stays near 1,100 sessions/day. Peaks on Oct 8, Oct 16 and Oct 22 stand out, and Thursday is the busiest weekday mainly because of the Oct 8 and Oct 22 peaks. Sunday is the quietest day (9.6% of sessions). Spikes like these would normally be checked against campaign or email send dates before treating them as a lasting trend.

## Interview Questions
**What is a traffic source?**
Where a visit came from: for example organic search (search engines), direct (typed URL or bookmark), social media, email campaigns, or referral (links from other websites). Comparing sources shows which channels bring visitors and which bring valuable ones.

**Which KPI would you track?**
It depends on the goal, but I would track **conversion rate by source** as the main one, since it ties traffic to results. Alongside it: sessions (reach), bounce rate (landing page quality), and pages per session (engagement). Volume alone can mislead, as the Social example above shows.

## How to run
```bash
pip install pandas matplotlib openpyxl
python generate_data.py   # optional: regenerate sample data
python analysis.py        # prints results, saves charts/dashboard.png and the Excel workbook
```

## Tools
Excel (`SUMIFS`, charts, dashboard sheet), Python (pandas, matplotlib, openpyxl), Power BI (guide with DAX measures).
