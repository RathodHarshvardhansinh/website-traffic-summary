# Power BI Dashboard: Build Guide (about 10 minutes)

The task lists Power BI as an optional tool. The `.pbix` file can't be created outside Power BI Desktop, so this guide rebuilds the same dashboard from `traffic_data.csv`. Add a screenshot of your finished report to the repo as `charts/powerbi_dashboard.png`.

## 1. Load the data
1. Open **Power BI Desktop** (free) > **Get data** > **Text/CSV** > pick `traffic_data.csv` > **Transform Data**.
2. Check types: `Date` = Date, the other numeric columns = Whole number > **Close & Apply**.

## 2. Add measures (Modeling > New measure)
```DAX
Total Sessions = SUM(traffic_data[Sessions])
Total Pageviews = SUM(traffic_data[Pageviews])
Pages per Session = DIVIDE([Total Pageviews], [Total Sessions])
Bounce Rate = DIVIDE(SUM(traffic_data[Bounced Sessions]), [Total Sessions])
Total Conversions = SUM(traffic_data[Conversions])
Conversion Rate = DIVIDE([Total Conversions], [Total Sessions])
Sessions 7d Avg =
AVERAGEX(
    DATESINPERIOD(traffic_data[Date], MAX(traffic_data[Date]), -7, DAY),
    CALCULATE([Total Sessions])
)
```
Format Bounce Rate and Conversion Rate as percentages.

## 3. Build the visuals
| Visual | Fields |
|--------|--------|
| 6 x **Card** | Total Sessions, Total Pageviews, Pages per Session, Bounce Rate, Total Conversions, Conversion Rate |
| **Line chart** | X = `Date`, Y = Total Sessions and Sessions 7d Avg |
| **Bar chart** | Y = `Source`, X = Total Sessions |
| **Bar chart** | Y = `Source`, X = Conversion Rate |
| **Donut chart** | Legend = `Device`, Values = Total Sessions |
| **Slicers** | `Source`, `Device`, `Date` (so the dashboard is interactive) |

## 4. Finish
- Title the page "Website Traffic Dashboard".
- Use navy `#1F3864` and orange `#C55A11` to match the Excel version.
- Save as `website_traffic_dashboard.pbix` and add it to the repo, plus a screenshot.
