There are a handful of “psychology + structure” conditions that, when they build up over weeks/months, materially elevate downside risk. These are the kinds of things Varma would treat as risk-regime inputs rather than precise crash predictors.

***

## 1. Sentiment Extremes and Overconfidence

When everyone feels bulletproof, crash risk rises.

- Research across markets finds that **elevated investor sentiment** is associated with higher crash/bubble risk, especially when it persists and decouples from fundamentals.[1][2][3]
- High sentiment + rich valuations tends to precede poor forward returns and a higher probability of large drawdowns, not just “mild mean reversion.”[3][4][1]
- Overconfidence leads investors to overestimate their information, underweight risk, overtrade, and bid up prices beyond fundamentals.[5][6][7]

**How to incorporate:**

- Track one or more sentiment composites (e.g., AAII/II surveys, news-based sentiment, options put/call ratios, Google Trends “stock market crash” vs “buy stocks”).[8][9][1]
- Classify “sentiment regime” into low/normal/high and treat **extended high sentiment** (weeks–months) as a risk-upgrade, especially if price has been trending up at the same time.

***

## 2. Valuation and Household Positioning Extremes

Psychology shows up in how much risk households are actually running and what they’re willing to pay for earnings.

- When **household equity allocations** reach record highs, history shows this tends to precede major drawdowns; extreme equity concentration reflects widespread optimism and limited dry powder.[10][11]
- Very high **Shiller CAPE** (e.g., >30–35) is associated with low 10‑year forward real returns and a higher probability of deep interim drawdowns, though timing is noisy.[11][12][13]
- Current work aggregating multiple valuation metrics (PE, CAPE, P/B, EV/EBIT) shows that prolonged extremes correlate with heightened vulnerability to any negative catalyst.[14][10]

**How to incorporate:**

- Maintain a slow-moving **valuation regime** flag (e.g., CAPE tertiles or deciles). Treat the top bucket as “structurally elevated downside risk,” not a short signal by itself.  
- Combine valuation regime with sentiment regime: **high valuation + high sentiment** is the classic “froth” zone where Varma would argue you should be thinking about lower exposure, even if you don’t know when it breaks.

***

## 3. Sentiment–Momentum Alignment (Psychology Following Price)

Crashes tend to come after sentiment has chased price and then turns.

- Fed research finds that a **sentiment–momentum variable** (12‑month change in consumer/market sentiment × recent return momentum) has predictive power for 1‑month-ahead returns, especially when both sentiment and momentum have been negative (pessimism chasing declines).[9]
- Behavioral work shows **sentiment leads volatility** in stressed regimes: shifts in mood anticipate realized vol spikes by one or two steps.[15][16]
- High connectedness of sentiment across names/sectors (everyone feeling the same way at once) increases stock price crash risk by propagating irrational signals faster.[17]

**How to incorporate:**

- Build a simple **sentiment × price** feature for the index or your universe:  
  - Rising price + surging sentiment for months → late-cycle euphoria.  
  - Falling price + collapsing sentiment → high near-term crash risk / vol spike.  
- Use this as a **risk gate**: in “euphoria” states with rich valuations, cap gross exposure and avoid adding leverage; in “panic” states, expect higher short-term vol and be more conservative with tight stops/size even if you’re buying dips.

***

## 4. Flow, Participation, and Herding Clues

Psychological crowding shows up in what people are actually buying and how concentrated it is.

- Overconfidence and herding are repeatedly linked to bubbles and subsequent crashes: investors extrapolate recent success, crowd into the same trades, and ignore risk limits.[6][18][5]
- Persistent **high turnover and volume in popular sectors/themes** (AI, “Magnificent 7” style concentration) are often proxies for speculative participation rather than broad, healthy accumulation.[19][1]
- When household equity allocations, margin debt, and concentrated positioning all run hot together, the system becomes highly sensitive to any shock.[20][10]

**How to incorporate:**

- Monitor **concentration metrics** (e.g., top‑10 names’ weight in index, sector/Theme ETF flows) as slow risk variables. Rising concentration + hot sentiment = crowding risk.  
- Track **margin/leverage proxies** (FINRA margin debt, options volume skewed to calls); extreme leverage combined with bad news is what turns ordinary declines into forced-deleveraging cascades.[21][10]

***

## 5. Event and News Backdrop (Slow-Burning Risk)

Some macro / structural conditions don’t give a date for the drop, but they tilt the odds.

- Studies show that **negative news sentiment** and sustained pessimism in financial news are associated with higher future crash risk for individual stocks and indices, especially when retail participation is high.[22][23][8]
- Global crisis work (GFC vs COVID) finds sentiment-based measures have **greater predictive power for volatility during crises** than in normal times; the psychology around events matters more when the system is already stressed.[16][22]
- Things like **election uncertainty, concentrated economic bets (e.g., CRE debt cliffs), and geopolitical tension** raise the market’s sensitivity to bad surprises when layered on top of high valuation / high sentiment.[24][10]

**How to incorporate:**

- Maintain a **qualitative event layer** in your risk model: “elevated macro/geopolitical/event risk” as a binary/ternary input that modulates how much you trust your usual edges.  
- Couple this with simple **news-sentiment aggregates** (e.g., index-level news polarity), but use it for **risk throttling**, not alpha prediction—Varma’s style is to let risk flags change exposure, not to forecast exact returns.[25][8][16]

***

## 6. Translating Psychology into a Risk-First Process

To align with how Varma thinks:

- **Don’t ask**: “Will the market crash?”  
- **Do ask**: “Given sentiment, valuations, positioning, and backdrop, is the **penalty for being wrong on the long side** currently higher than usual?”  

Implementation outline:

1. Build a **risk score** with 3–5 components you trust:  
   - Valuation regime (CAPE/valuation composite).  
   - Sentiment regime (survey/news/options + its trend).  
   - Participation/crowding (household equity share, margin/flows, concentration).  
   - Volatility/correlation regime (realized vol, VIX, cross‑sectional correlation).  
2. Map that score into **LOW / MED / HIGH risk** buckets, updated weekly/monthly, not intraday.  
3. Tie **max gross exposure and per‑trade risk** directly to that bucket (e.g., 1.2× / 1.0× / 0.4× base risk).  
4. Backtest your strategies **by risk bucket** and confirm that your PnL is indeed worse, more negatively skewed, or more crash-prone in the “HIGH” bucket; if yes, you’ve got a defensible throttle.

That’s the kind of risk-first, psychology-aware framework Varma would be on board with: use slow, behavior-linked indicators to classify when being long is more dangerous, then **react by sizing and participation**, not by trying to call the exact top.

[1](https://www.ewadirect.com/proceedings/aemps/article/view/6052)
[2](https://www.frontiersin.org/articles/10.3389/fpsyg.2021.664849/full)
[3](https://onlinelibrary.wiley.com/doi/10.1111/fire.12301)
[4](https://www.emerald.com/books/book/15905/chapter/87558501/The-Predictive-Power-of-Investor-Sentiment-on-US)
[5](https://www.abacademies.org/articles/the-role-of-overconfidence-and-herding-in-stock-market-bubbles-and-crashes.pdf)
[6](https://virtusinterpress.org/The-impact-of-overconfidence-on-stock-market-valuation-An-empirical-study-on-listed-firms.html)
[7](https://www.sciencedirect.com/science/article/pii/S2214845022000813)
[8](https://downloads.hindawi.com/journals/ddns/2022/8305947.pdf)
[9](https://www.frbsf.org/research-and-insights/publications/economic-letter/2018/12/using-sentiment-and-momentum-to-predict-stock-returns/)
[10](https://discoveryalert.com.au/us-household-wealth-equity-concentration-2025/)
[11](https://www.financialplanningassociation.org/article/journal/JUL21-risk-households-take)
[12](https://threestreamsfinancial.com/shiller-cape-ratio/)
[13](https://insights.aaii.com/p/navigating-market-cycles-with-shillers)
[14](https://www.researchaffiliates.com/publications/articles/645-cape-fear-why-cape-naysayers-are-wrong)
[15](https://pmc.ncbi.nlm.nih.gov/articles/PMC7717912/)
[16](https://pmc.ncbi.nlm.nih.gov/articles/PMC9111709/)
[17](https://pmc.ncbi.nlm.nih.gov/articles/PMC12026076/)
[18](https://www.heygotrade.com/en/blog/behavioral-finance-in-trading)
[19](https://drpress.org/ojs/index.php/fbem/article/view/12559)
[20](https://www.forbes.com/sites/greatspeculations/2025/10/16/sp-500-poised-for-a-40-crash/)
[21](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2007/wp07-3.pdf)
[22](https://pmc.ncbi.nlm.nih.gov/articles/PMC9253256/)
[23](http://arxiv.org/pdf/1705.02447.pdf)
[24](https://eprajournals.com/IJES/article/15895)
[25](https://www.youtube.com/watch?v=itRL9v67v9I)
[26](https://ete.sciten.org/index.php/ete/article/view/20)
[27](https://www.nature.com/articles/s41598-024-61106-2)
[28](https://scholarworks.lib.csusb.edu/jitim/vol33/iss1/4)
[29](http://www.emerald.com/jfrc/article/32/5/590-619/1237406)
[30](http://www.bjmc.lu.lv/fileadmin/user_upload/lu_portal/projekti/bjmc/Contents/5_3_03_Liutvinavicius.pdf)
[31](https://www.tandfonline.com/doi/full/10.1080/23322039.2024.2422959)
[32](https://www.sciencedirect.com/science/article/abs/pii/S1544612325024110)
[33](https://pages.stern.nyu.edu/~jwurgler/papers/wurgler_baker_cross_section.pdf)
[34](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5376654)
[35](https://som.yale.edu/centers/international-center-for-finance/data/stock-market-confidence-indices/united-states)
[36](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1138&context=open_access_theses)
[37](https://www.investmentbankingcouncil.org/blog/how-behavioral-finance-shapes-investor-psychology)
[38](https://www.comparables.ai/articles/behavioral-finance-and-its-influence-on-company-valuations)
[39](https://www.lynalden.com/asset-allocation/)