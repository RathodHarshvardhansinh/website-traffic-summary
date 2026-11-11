"""Website traffic summary: KPIs by source, device and day; dashboard image and Excel workbook."""
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList

df = pd.read_csv("traffic_data.csv", parse_dates=["Date"])
df["Weekday"] = df["Date"].dt.day_name().str[:3]

def kpis(g):
    s = g["Sessions"].sum()
    return pd.Series({
        "Sessions": s, "Pageviews": g["Pageviews"].sum(),
        "Pages/Session": g["Pageviews"].sum() / s,
        "Bounce Rate %": g["Bounced Sessions"].sum() / s * 100,
        "Conversions": g["Conversions"].sum(),
        "Conv Rate %": g["Conversions"].sum() / s * 100,
    })

total = kpis(df)
by_src = df.groupby("Source").apply(kpis, include_groups=False).sort_values("Sessions", ascending=False)
by_dev = df.groupby("Device").apply(kpis, include_groups=False).sort_values("Sessions", ascending=False)
order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
by_wd = df.groupby("Weekday").apply(kpis, include_groups=False).reindex(order)
daily = df.groupby("Date")["Sessions"].sum()
daily_ma = daily.rolling(7).mean()
src_share = by_src["Sessions"] / total["Sessions"] * 100
conv_share = by_src["Conversions"] / total["Conversions"] * 100

pd.set_option("display.width", 200)
print("TOTAL\n", total.round(2).to_string())
print("\nBY SOURCE\n", by_src.round(2).to_string())
print("\nBY DEVICE\n", by_dev.round(2).to_string())
print("\nBY WEEKDAY\n", by_wd.round(2).to_string())
print("\nTop 3 days\n", daily.sort_values(ascending=False).head(3).to_string())
print("\nShare of sessions %\n", src_share.round(1).to_string())
print("\nShare of conversions %\n", conv_share.round(1).to_string())
wk = daily.groupby(((daily.index - daily.index[0]).days // 7)).sum()
print("\nWeekly sessions:", wk.tolist())

# ---------- Dashboard image ----------
navy, orange, grey, light = "#1F3864", "#C55A11", "#9AA5B1", "#6C8EBF"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
fig = plt.figure(figsize=(13, 8.2), facecolor="white")
fig.suptitle("Website Traffic Dashboard  |  Oct 1 - Oct 31, 2026", x=0.04, ha="left", fontsize=16, fontweight="bold", color=navy)
tiles = [("Sessions", f"{int(total['Sessions']):,}"), ("Pageviews", f"{int(total['Pageviews']):,}"),
         ("Pages / Session", f"{total['Pages/Session']:.2f}"), ("Bounce Rate", f"{total['Bounce Rate %']:.1f}%"),
         ("Conversions", f"{int(total['Conversions']):,}"), ("Conversion Rate", f"{total['Conv Rate %']:.2f}%")]
for i, (lab, val) in enumerate(tiles):
    ax = fig.add_axes([0.04 + i * 0.158, 0.80, 0.145, 0.10]); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="#F2F5FA", ec="#D5DCE8"))
    ax.text(0.5, 0.58, val, ha="center", va="center", fontsize=17, fontweight="bold", color=navy, transform=ax.transAxes)
    ax.text(0.5, 0.20, lab, ha="center", va="center", fontsize=9, color="#555", transform=ax.transAxes)

ax = fig.add_axes([0.05, 0.47, 0.90, 0.26])
ax.plot(daily.index, daily.values, color=light, lw=1.3, label="Daily sessions")
ax.plot(daily_ma.index, daily_ma.values, color=orange, lw=2.4, label="7-day average")
ax.set_title("Daily sessions trend", loc="left", fontweight="bold"); ax.legend(frameon=False, loc="upper left")
ax.set_ylim(0, daily.max() * 1.15)
ax.tick_params(axis="x", labelsize=8)
fig.autofmt_xdate(rotation=0, ha="center")

ax = fig.add_axes([0.12, 0.08, 0.20, 0.28])
b = ax.barh(by_src.index[::-1], by_src["Sessions"][::-1], color=navy)
ax.bar_label(b, labels=[f"{v:,}" for v in by_src["Sessions"][::-1].astype(int)], padding=3, fontsize=8)
ax.set_title("Sessions by source", loc="left", fontweight="bold"); ax.set_xlim(0, by_src["Sessions"].max() * 1.2)

ax = fig.add_axes([0.46, 0.08, 0.21, 0.28])
cr = by_src["Conv Rate %"].sort_values()
b = ax.barh(cr.index, cr.values, color=[orange if v < total["Conv Rate %"] else navy for v in cr.values])
ax.bar_label(b, labels=[f"{v:.1f}%" for v in cr.values], padding=3, fontsize=8)
ax.axvline(total["Conv Rate %"], color=grey, ls="--", lw=1)
ax.set_title("Conversion rate by source", loc="left", fontweight="bold"); ax.set_xlim(0, cr.max() * 1.2)

ax = fig.add_axes([0.74, 0.08, 0.22, 0.28])
_, _, ats = ax.pie(by_dev["Sessions"], labels=by_dev.index, autopct="%1.0f%%", startangle=90, colors=[navy, orange, grey],
       pctdistance=0.78, wedgeprops=dict(width=0.45, edgecolor="white"), textprops={"fontsize": 9})
for t in ats: t.set_color("white"); t.set_fontweight("bold")
ax.set_title("Sessions by device", loc="left", fontweight="bold")
fig.savefig("charts/dashboard.png", dpi=150); plt.close(fig)

# ---------- Excel workbook ----------
wb = Workbook(); dash = wb.active; dash.title = "Dashboard"; sm = wb.create_sheet("Summary"); raw = wb.create_sheet("Traffic Data")
raw.append(list(df.columns[:7]) + ["Weekday"])
for r in df.itertuples(index=False):
    raw.append([r.Date.date(), r.Source, r.Device, r.Sessions, r.Pageviews, r._5, r.Conversions])
N = len(df) + 1
for i in range(2, N + 1):
    raw[f"A{i}"].number_format = "yyyy-mm-dd"
    raw[f"H{i}"] = f'=TEXT(A{i},"ddd")'
hf = PatternFill("solid", fgColor="1F3864"); hf2 = PatternFill("solid", fgColor="C55A11")
thin = Side(style="thin", color="BBBBBB"); bd = Border(top=thin, bottom=thin, left=thin, right=thin)
for c in raw[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = hf
for col, w in zip("ABCDEFGH", [12, 16, 10, 10, 11, 17, 12, 10]): raw.column_dimensions[col].width = w
raw.freeze_panes = "A2"; raw.auto_filter.ref = f"A1:H{N}"
def R(col): return f"'Traffic Data'!${col}$2:${col}${N}"

def head(ws, row, labels):
    for j, l in enumerate(labels):
        c = ws.cell(row=row, column=1 + j, value=l); c.font = Font(bold=True, color="FFFFFF"); c.fill = hf2
        c.alignment = Alignment(horizontal="center", wrap_text=True)

sm["A1"] = "Traffic Summary"; sm["A1"].font = Font(bold=True, size=16, color="1F3864")
sm["A2"] = "All figures are formulas linked to the 'Traffic Data' sheet."
def table(top, title, key_col, keys):
    head(sm, top, [title, "Sessions", "Pageviews", "Pages/Session", "Bounce Rate", "Conversions", "Conv. Rate", "% of Sessions"])
    for k, key in enumerate(keys):
        r = top + 1 + k
        sm[f"A{r}"] = key
        sm[f"B{r}"] = f"=SUMIFS({R('D')},{R(key_col)},A{r})"
        sm[f"C{r}"] = f"=SUMIFS({R('E')},{R(key_col)},A{r})"
        sm[f"D{r}"] = f"=C{r}/B{r}"
        sm[f"E{r}"] = f"=SUMIFS({R('F')},{R(key_col)},A{r})/B{r}"
        sm[f"F{r}"] = f"=SUMIFS({R('G')},{R(key_col)},A{r})"
        sm[f"G{r}"] = f"=F{r}/B{r}"
        sm[f"H{r}"] = f"=B{r}/SUM({R('D')})"
        sm[f"D{r}"].number_format = "0.00"
        for c in "EGH": sm[f"{c}{r}"].number_format = "0.0%"
        for c in "BCF": sm[f"{c}{r}"].number_format = "#,##0"
        for c in "ABCDEFGH": sm[f"{c}{r}"].border = bd
    return top + 1, top + len(keys)
s1, s2 = table(4, "Source", "B", list(by_src.index))
d1, d2 = table(s2 + 3, "Device", "C", list(by_dev.index))
w1, w2 = table(d2 + 3, "Weekday", "H", order)
t0 = w2 + 3
head(sm, t0, ["Date", "Sessions", "7-day Avg"])
dates = list(daily.index)
for k, d in enumerate(dates):
    r = t0 + 1 + k
    sm[f"A{r}"] = d.date(); sm[f"A{r}"].number_format = "yyyy-mm-dd"
    sm[f"B{r}"] = f"=SUMIFS({R('D')},{R('A')},A{r})"
    if k >= 6: sm[f"C{r}"] = f"=AVERAGE(B{r-6}:B{r})"; sm[f"C{r}"].number_format = "#,##0"
t1, t2 = t0 + 1, t0 + len(dates)
for col, w in zip("ABCDEFGH", [16, 11, 12, 14, 12, 12, 11, 13]): sm.column_dimensions[col].width = w

# Dashboard sheet: KPI tiles + native charts
dash["A1"] = "Website Traffic Dashboard  |  Oct 1 - Oct 31, 2026"; dash["A1"].font = Font(bold=True, size=16, color="1F3864")
kp = [("Sessions", f"=SUM({R('D')})", "#,##0"), ("Pageviews", f"=SUM({R('E')})", "#,##0"),
      ("Pages / Session", f"=SUM({R('E')})/SUM({R('D')})", "0.00"), ("Bounce Rate", f"=SUM({R('F')})/SUM({R('D')})", "0.0%"),
      ("Conversions", f"=SUM({R('G')})", "#,##0"), ("Conv. Rate", f"=SUM({R('G')})/SUM({R('D')})", "0.00%")]
for i, (lab, f, nf) in enumerate(kp):
    col = 1 + i * 2
    dash.merge_cells(start_row=3, start_column=col, end_row=3, end_column=col + 1)
    dash.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col + 1)
    a = dash.cell(row=3, column=col, value=lab); a.font = Font(color="555555"); a.alignment = Alignment(horizontal="center")
    b = dash.cell(row=4, column=col, value=f); b.number_format = nf; b.font = Font(bold=True, size=18, color="1F3864"); b.alignment = Alignment(horizontal="center")
    for rr in (3, 4):
        for cc in (col, col + 1): dash.cell(row=rr, column=cc).fill = PatternFill("solid", fgColor="F2F5FA")
for c in range(1, 13): dash.column_dimensions[chr(64 + c)].width = 11
dash.row_dimensions[4].height = 30

lc = LineChart(); lc.title = "Daily Sessions (with 7-day average)"; lc.height = 8; lc.width = 24
lc.add_data(Reference(sm, min_col=2, max_col=3, min_row=t0, max_row=t2), titles_from_data=True)
lc.set_categories(Reference(sm, min_col=1, min_row=t1, max_row=t2))
lc.x_axis.number_format = "d-mmm"; lc.x_axis.delete = False; lc.y_axis.delete = False
dash.add_chart(lc, "A6")
bc = BarChart(); bc.type = "bar"; bc.title = "Sessions by Source"; bc.legend = None; bc.height = 8; bc.width = 12
bc.add_data(Reference(sm, min_col=2, min_row=4, max_row=s2), titles_from_data=True)
bc.set_categories(Reference(sm, min_col=1, min_row=s1, max_row=s2)); bc.x_axis.delete = False; bc.y_axis.delete = False
dash.add_chart(bc, "A23")
cc_ = BarChart(); cc_.type = "bar"; cc_.title = "Conversion Rate by Source"; cc_.legend = None; cc_.height = 8; cc_.width = 12
cc_.add_data(Reference(sm, min_col=7, min_row=4, max_row=s2), titles_from_data=True)
cc_.set_categories(Reference(sm, min_col=1, min_row=s1, max_row=s2)); cc_.y_axis.number_format = "0%"
cc_.x_axis.delete = False; cc_.y_axis.delete = False
dash.add_chart(cc_, "G23")
pc = PieChart(); pc.title = "Sessions by Device"; pc.height = 8; pc.width = 12
pc.add_data(Reference(sm, min_col=2, min_row=d1 - 1, max_row=d2), titles_from_data=True)
pc.set_categories(Reference(sm, min_col=1, min_row=d1, max_row=d2))
pc.dataLabels = DataLabelList(); pc.dataLabels.showPercent = True
for a in ("showVal", "showCatName", "showSerName", "showLegendKey"): setattr(pc.dataLabels, a, False)
dash.add_chart(pc, "A40")
wc = BarChart(); wc.type = "col"; wc.title = "Sessions by Weekday"; wc.legend = None; wc.height = 8; wc.width = 12
wc.add_data(Reference(sm, min_col=2, min_row=w1 - 1, max_row=w2), titles_from_data=True)
wc.set_categories(Reference(sm, min_col=1, min_row=w1, max_row=w2)); wc.x_axis.delete = False; wc.y_axis.delete = False
dash.add_chart(wc, "G40")
wb.save("website_traffic_summary.xlsx")
print("\nSaved workbook + charts/dashboard.png")
