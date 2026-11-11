"""Generate sample website traffic data (synthetic, reproducible): daily sessions by source and device."""
import csv, random, datetime as dt

random.seed(33)
start = dt.date(2026, 10, 1)
days = [start + dt.timedelta(d) for d in range(31)]
# base daily sessions, bounce rate, conversion rate per source
sources = {
    "Organic Search": (420, 0.42, 0.034),
    "Direct":         (260, 0.36, 0.046),
    "Social":         (230, 0.58, 0.012),
    "Email":          (110, 0.30, 0.062),
    "Referral":       (90,  0.45, 0.028),
}
device_share = {"Desktop": 0.46, "Mobile": 0.48, "Tablet": 0.06}
device_bounce_adj = {"Desktop": -0.04, "Mobile": 0.05, "Tablet": 0.0}
device_conv_adj = {"Desktop": 1.25, "Mobile": 0.80, "Tablet": 1.0}
weekday_mult = [1.05, 1.08, 1.06, 1.03, 0.97, 0.78, 0.74]  # Mon..Sun

rows = []
for d in days:
    for s, (base, bounce, conv) in sources.items():
        mult = weekday_mult[d.weekday()] * random.uniform(0.9, 1.1)
        if s == "Email" and d in (dt.date(2026, 10, 8), dt.date(2026, 10, 22)):
            mult *= 3.2            # newsletter send days
        if s == "Social" and d == dt.date(2026, 10, 16):
            mult *= 2.4            # one post went viral
        for dev, share in device_share.items():
            sess = max(1, round(base * mult * share * random.uniform(0.92, 1.08)))
            b = min(0.95, max(0.05, bounce + device_bounce_adj[dev] + random.uniform(-0.03, 0.03)))
            c = max(0.0, conv * device_conv_adj[dev] * random.uniform(0.85, 1.15))
            pv = round(sess * random.uniform(2.2, 3.4) * (1.15 if s in ("Email", "Direct") else 1.0))
            rows.append([d.isoformat(), s, dev, sess, pv, round(sess * b), round(sess * c)])

with open("traffic_data.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Source", "Device", "Sessions", "Pageviews", "Bounced Sessions", "Conversions"])
    w.writerows(rows)
print(len(rows), "rows written")
