# Allowed Web Domains for Research

**Version**: 1.0.0
**Last Updated**: 2025-10-07
**Purpose**: Comprehensive allowed domain list for web research agents (especially researcher-external)

## Quality Tier Definitions

- **Tier 1**: Highest quality, authoritative sources with established credibility
- **Tier 2**: Good quality, reputable sources with strong community or professional backing
- **Tier 3**: Acceptable quality, useful for specialized contexts or emerging content

---

## Financial Research Domains

### Financial News - Tier 1 (Authoritative Business Journalism)

| Domain              | Quality Tier | Specialization        | Update Frequency  | Access Model | Justification                                                           |
| ------------------- | ------------ | --------------------- | ----------------- | ------------ | ----------------------------------------------------------------------- |
| **wsj.com**         | Tier 1-A     | General Financial     | Daily             | Paywall      | 39 Pulitzers, 135+ years, fearless reporting, 3.2M digital subs         |
| **reuters.com**     | Tier 1-A     | Global Wire Service   | Continuous (24/7) | Mixed        | 2024 Pulitzers, 173+ years, 2,500+ journalists, value-neutral           |
| **ft.com**          | Tier 1-A     | International Finance | Daily + weekend   | Paywall      | 136+ years, newspaper of record, centrist authority                     |
| **bloomberg.com**   | Tier 1-A     | Markets & Data        | Continuous (24/7) | Metered      | 35 years, 2,300+ reporters in 146 bureaus, accuracy commitment          |
| **economist.com**   | Tier 1-B     | Analysis & Data       | Weekly            | Paywall      | 181+ years, data journalism, editorial anonymity, global reach          |
| **apnews.com**      | Tier 1-B     | General News          | Continuous (24/7) | Free         | 59 Pulitzers, 178+ years, nonprofit cooperative, AP Stylebook authority |
| **barrons.com**     | Tier 1-B     | Investment Analysis   | Weekly            | Paywall      | 103+ years, Dow Jones-owned, market authority                           |
| **marketwatch.com** | Tier 1-C     | Real-time Markets     | Continuous (24/7) | Paywall      | 27+ years, Dow Jones-owned, real-time coverage                          |

### Financial News - Tier 2/3 (Supporting Sources)

| Domain                  | Quality Tier | Specialization          | Best Use Case                                                      |
| ----------------------- | ------------ | ----------------------- | ------------------------------------------------------------------ |
| **cnbc.com**            | Tier 2       | Markets (Real-time)     | Real-time market monitoring, breaking news, live commentary        |
| **finance.yahoo.com**   | Tier 2       | Markets (Data Platform) | Market data aggregation, portfolio tracking, free quotes           |
| **forbes.com**          | Tier 2       | Management + Wealth     | Executive profiles, wealth trends, business leadership             |
| **fortune.com**         | Tier 2       | Management + Corporate  | Corporate strategy, Fortune 500 analysis, leadership trends        |
| **businessinsider.com** | Tier 3       | Tech + Startups         | Tech startup news, quick market summaries, trending stories        |
| **thestreet.com**       | Tier 3       | Markets (Retail)        | Retail investor education, stock screening, market sentiment       |
| **seekingalpha.com**    | Tier 3       | Markets (Crowdsourced)  | Alternative perspectives, crowdsourced analysis, dividend research |
| **investors.com**       | Tier 2       | Markets (Technical)     | Technical analysis, growth stock screening, systematic trading     |

### Regulatory & Government Sources - Tier 1

| Domain                 | Agency                                  | Key Data Types                            | API Available | Justification                                    |
| ---------------------- | --------------------------------------- | ----------------------------------------- | ------------- | ------------------------------------------------ |
| **sec.gov**            | Securities and Exchange Commission      | 10-K, 10-Q, 13-F, EDGAR filings           | Yes           | Primary US securities regulator, company filings |
| **finra.org**          | Financial Industry Regulatory Authority | Broker data, market regulation            | Limited       | Self-regulatory organization for brokers         |
| **fdic.gov**           | Federal Deposit Insurance Corporation   | Bank data, deposit insurance              | Yes           | Banking system stability, institution data       |
| **federalreserve.gov** | Federal Reserve System                  | Monetary policy, FOMC minutes, Beige Book | Yes           | US central bank, monetary policy authority       |
| **cftc.gov**           | Commodity Futures Trading Commission    | Derivatives, futures regulation           | Limited       | Derivatives market oversight                     |
| **occ.gov**            | Office of the Comptroller of Currency   | National bank regulation                  | Limited       | Federal banking system regulator                 |

### Market Data Platforms

| Domain                  | Quality Tier | Data Types                                      | Free Tier Quality | API Access            |
| ----------------------- | ------------ | ----------------------------------------------- | ----------------- | --------------------- |
| **fred.stlouisfed.org** | Tier 1       | Economic indicators, interest rates, employment | High              | Yes (Free)            |
| **finance.yahoo.com**   | Tier 1       | Stock quotes, historical prices, fundamentals   | High              | Unofficial (yfinance) |
| **alphaadvantage.co**   | Tier 2       | Stocks, forex, crypto, fundamentals             | Medium            | Yes (25 calls/day)    |
| **polygon.io**          | Tier 2       | US stocks, 2yr historical, EOD data             | Medium            | Yes (5 calls/min)     |
| **tradingview.com**     | Tier 3       | Charts, screeners, community ideas              | Medium            | No API                |
| **investing.com**       | Tier 3       | Global stocks, indices, commodities             | Medium            | No official API       |

### Economic Research Institutions - Tier 1

| Domain                  | Institution                          | Key Resources                                      | Update Frequency  | Authority |
| ----------------------- | ------------------------------------ | -------------------------------------------------- | ----------------- | --------- |
| **federalreserve.gov**  | Federal Reserve System               | Beige Book, FOMC Minutes, FEDS Papers              | Monthly/Quarterly | Very High |
| **imf.org**             | International Monetary Fund          | World Economic Outlook, GFSR, Country Reports      | Quarterly/Annual  | Very High |
| **worldbank.org**       | World Bank Group                     | Global Economic Prospects, WDI, Data360            | Annual/Quarterly  | Very High |
| **bis.org**             | Bank for International Settlements   | BIS Quarterly Review, Basel Committee              | Quarterly         | Very High |
| **nber.org**            | National Bureau of Economic Research | Working Papers, NBER Digest, Business Cycle Dating | Weekly/Monthly    | Very High |
| **bea.gov**             | Bureau of Economic Analysis          | GDP, Personal Income, Trade Data                   | Monthly/Quarterly | Very High |
| **bls.gov**             | Bureau of Labor Statistics           | Employment, CPI, PPI, Productivity                 | Monthly           | Very High |
| **ecb.europa.eu**       | European Central Bank                | Working Papers, Economic Bulletin, Euro Stats      | Weekly/Monthly    | Very High |
| **bankofengland.co.uk** | Bank of England                      | Staff Papers, Monetary Policy Reports              | Monthly/Quarterly | Very High |
| **newyorkfed.org**      | NY Federal Reserve Bank              | Liberty Street Economics, Consumer Expectations    | Monthly/Ongoing   | High      |

### Fintech Documentation & Industry

| Domain                       | Type                 | Quality Tier | Focus Area                                              |
| ---------------------------- | -------------------- | ------------ | ------------------------------------------------------- |
| **docs.stripe.com**          | Platform Docs        | Tier 1       | Payments API, comprehensive product coverage            |
| **plaid.com/docs**           | Platform Docs        | Tier 1       | Financial data API, KYC/AML, sandbox testing            |
| **developer.visa.com**       | Platform Docs        | Tier 2       | Payment networks, AI commerce APIs                      |
| **developer.mastercard.com** | Platform Docs        | Tier 2       | Payment networks, developer portal                      |
| **twilio.com/docs**          | Platform Docs        | Tier 2       | Communications, verify/lookup APIs                      |
| **americanbanker.com**       | Industry Publication | Tier 1       | Banking/fintech, regulatory/tech insights               |
| **pymnts.com**               | Industry Publication | Tier 1       | Payments analysis, fintech trends, proprietary research |
| **finovate.com**             | Industry Publication | Tier 2       | Fintech innovation, conference series                   |
| **bankingdive.com**          | Industry Publication | Tier 2       | Daily banking coverage, M&A/regulatory analysis         |

---

## Development & Technical Documentation

### Programming Languages - Tier 1 (Official Documentation)

| Language       | Official Domain                                 | Doc Quality | Community Size  | Justification                                                        |
| -------------- | ----------------------------------------------- | ----------- | --------------- | -------------------------------------------------------------------- |
| **Java**       | docs.oracle.com/en/java/                        | Excellent   | #3 TIOBE        | Oracle official, comprehensive API references, multi-version support |
| **JavaScript** | developer.mozilla.org/en-US/docs/Web/JavaScript | Excellent   | #6 TIOBE        | MDN de facto standard, Mozilla-backed, ECMAScript tracking           |
| **C#**         | learn.microsoft.com/en-us/dotnet/csharp/        | Excellent   | #5 TIOBE        | Microsoft official, comprehensive language + API docs                |
| **Go**         | go.dev/doc/                                     | Excellent   | #8 TIOBE        | Official Go project, Effective Go guide, codewalks                   |
| **TypeScript** | typescriptlang.org/docs/                        | Excellent   | Top 10 GitHub   | Microsoft official, comprehensive handbook + playground              |
| **Rust**       | doc.rust-lang.org/                              | Excellent   | Rapidly growing | Official Rust docs, The Book, By Example, exceptional quality        |
| **PHP**        | php.net/docs.php                                | Good        | Top 10 web      | Official PHP Group docs, multilingual, community-maintained          |
| **Ruby**       | ruby-lang.org/en/documentation/                 | Good        | Top 15          | Official Ruby docs, multiple resources, global community             |
| **Swift**      | swift.org/documentation/                        | Excellent   | Top iOS/macOS   | Official Swift.org, Apple/open source, concurrency focus             |
| **Kotlin**     | kotlinlang.org/docs/                            | Excellent   | #1 Android      | JetBrains official, multi-platform, comprehensive guides             |

### Frontend Frameworks - Tier 1/2

| Framework   | Domain           | Quality Tier | Corporate Sponsor    | Community                              | Justification                             |
| ----------- | ---------------- | ------------ | -------------------- | -------------------------------------- | ----------------------------------------- |
| **React**   | react.dev        | Tier 1       | Meta                 | 2M monthly visitors, 45M npm downloads | 77.4% market share, comprehensive docs    |
| **Next.js** | nextjs.org       | Tier 1       | Vercel               | Nike/Notion/WaPo use it                | Production-ready meta-framework           |
| **Vue**     | vuejs.org        | Tier 1       | Community (Evan You) | 7M npm downloads                       | 11.9% market share, strong community      |
| **Nuxt**    | nuxt.com         | Tier 2       | Community + sponsors | 4.2M npm downloads                     | Vue meta-framework, NASA/Microsoft use it |
| **Svelte**  | svelte.dev       | Tier 2       | Vercel               | 2M npm downloads                       | Compiler-based innovation, 3.4% share     |
| **Angular** | angular.dev      | Tier 2       | Google               | 476K npm downloads                     | Enterprise-focused, proven longevity      |
| **Solid**   | docs.solidjs.com | Tier 3       | Community            | 940K npm downloads                     | Fine-grained reactivity innovation        |

### Backend Frameworks - Tier 1

| Framework         | Language   | Domain                     | Doc Quality | Production Maturity                   |
| ----------------- | ---------- | -------------------------- | ----------- | ------------------------------------- |
| **Django**        | Python     | djangoproject.com          | Excellent   | Very High (since 2005)                |
| **FastAPI**       | Python     | fastapi.tiangolo.com       | Excellent   | High (Microsoft/Netflix/Uber use)     |
| **Flask**         | Python     | flask.palletsprojects.com  | Excellent   | Very High (v3.1.x)                    |
| **Express.js**    | JavaScript | expressjs.com              | Good        | Very High (OpenJS Foundation)         |
| **NestJS**        | TypeScript | nestjs.com                 | Excellent   | High (Enterprise sponsors)            |
| **Spring (Boot)** | Java       | spring.io                  | Excellent   | Very High (Industry standard)         |
| **ASP.NET Core**  | C#         | learn.microsoft.com/aspnet | Excellent   | Very High (Microsoft-backed)          |
| **Ruby on Rails** | Ruby       | rubyonrails.org            | Excellent   | Very High (20+ years, GitHub/Shopify) |

### Database Documentation - Tier 1/2

| Database          | Type            | Domain                   | License                   | Tier   | Doc Quality |
| ----------------- | --------------- | ------------------------ | ------------------------- | ------ | ----------- |
| **PostgreSQL**    | SQL             | postgresql.org           | Open (PostgreSQL)         | Tier 1 | Excellent   |
| **MySQL**         | SQL             | dev.mysql.com            | Mixed (GPL/Commercial)    | Tier 1 | Excellent   |
| **SQLite**        | SQL (Embedded)  | sqlite.org               | Public Domain             | Tier 1 | Excellent   |
| **MariaDB**       | SQL             | mariadb.com/kb           | Open (GPL)                | Tier 2 | Very Good   |
| **MongoDB**       | Document        | mongodb.com/docs         | Mixed (SSPL/Commercial)   | Tier 1 | Excellent   |
| **Redis**         | Key-Value/Cache | redis.io/docs            | Mixed (RSALv2/Commercial) | Tier 1 | Excellent   |
| **Elasticsearch** | Search          | elastic.co/guide         | Mixed (Elastic License)   | Tier 2 | Excellent   |
| **Cassandra**     | Wide-Column     | cassandra.apache.org/doc | Open (Apache 2.0)         | Tier 1 | Very Good   |
| **Neo4j**         | Graph           | neo4j.com/docs           | Mixed (GPL/Commercial)    | Tier 1 | Excellent   |

### DevOps & Infrastructure - Tier 1/2

| Tool               | Category                | Domain                            | Tier   | Foundation Status      | Doc Quality |
| ------------------ | ----------------------- | --------------------------------- | ------ | ---------------------- | ----------- |
| **Kubernetes**     | Container Orchestration | kubernetes.io                     | Tier 1 | CNCF Graduated         | Excellent   |
| **Docker**         | Container Runtime       | docs.docker.com                   | Tier 1 | Independent            | Excellent   |
| **Terraform**      | IaC                     | developer.hashicorp.com/terraform | Tier 1 | HashiCorp              | Excellent   |
| **Ansible**        | IaC/Config Mgmt         | docs.ansible.com                  | Tier 1 | Red Hat                | Excellent   |
| **GitHub Actions** | CI/CD                   | docs.github.com/actions           | Tier 1 | GitHub/Microsoft       | Excellent   |
| **GitLab CI/CD**   | CI/CD                   | docs.gitlab.com/ee/ci             | Tier 2 | GitLab Inc.            | Very Good   |
| **Jenkins**        | CI/CD                   | jenkins.io/doc                    | Tier 2 | CDF (Linux Foundation) | Very Good   |
| **Prometheus**     | Monitoring              | prometheus.io/docs                | Tier 1 | CNCF Graduated         | Excellent   |
| **Grafana**        | Visualization           | grafana.com/docs                  | Tier 1 | Grafana Labs           | Excellent   |

### Testing Frameworks - Tier 1/2

| Framework      | Language       | Type                 | Domain           | Tier   | Doc Quality                 |
| -------------- | -------------- | -------------------- | ---------------- | ------ | --------------------------- |
| **Jest**       | JavaScript/TS  | Unit/Integration     | jestjs.io        | Tier 1 | Excellent (300M+ downloads) |
| **Vitest**     | JavaScript/TS  | Unit/Integration     | vitest.dev       | Tier 1 | Excellent (Jest-compatible) |
| **Mocha**      | JavaScript     | Unit/Integration     | mochajs.org      | Tier 2 | Good (Flexible BDD/TDD)     |
| **Cypress**    | JavaScript     | E2E/Component        | cypress.io       | Tier 1 | Excellent (5.3M weekly)     |
| **Playwright** | Multi-language | E2E                  | playwright.dev   | Tier 1 | Excellent (Cross-browser)   |
| **pytest**     | Python 3.8+    | Unit/Integration     | docs.pytest.org  | Tier 1 | Excellent (1300+ plugins)   |
| **JUnit 5**    | Java           | Unit                 | junit.org/junit5 | Tier 1 | Good (Java standard)        |
| **TestNG**     | Java           | Unit/Integration/E2E | testng.org       | Tier 1 | Excellent (v7.9.0)          |
| **RSpec**      | Ruby           | Unit (BDD)           | rspec.info       | Tier 2 | Good (Ruby standard)        |
| **Selenium**   | Multi-language | E2E (Browser)        | selenium.dev     | Tier 2 | Good (v4.35)                |

---

## Existing Domains (Currently Allowed)

### AI/ML Platforms & Documentation (17 domains)

- platform.openai.com, openai.com, cookbook.openai.com (Tier 1)
- ai.google, developers.google.com, ai.googleblog.com (Tier 1)
- google.github.io, blog.research.google, research.google (Tier 1)
- langchain-ai.github.io, python.langchain.com, docs.langgraph.com (Tier 1)
- docs.pydantic.dev, ai.pydantic.dev (Tier 1)
- docs.llamaindex.ai, developers.llamaindex.ai (Tier 1)
- www.anthropic.com (Tier 1)

### Developer Documentation (11 domains)

- docs.stripe.com, stripe.com (Tier 1 - already covered in Fintech)
- docs.pytest.org (Tier 1 - already covered in Testing)
- python-jsonschema.readthedocs.io (Tier 1)
- pypi.org (Tier 1)
- swagger.io (Tier 1)
- docs.temporal.io (Tier 1)
- airflow.apache.org (Tier 1)
- backstage.io (Tier 1)
- www.npmjs.com (Tier 1)
- a2a-protocol.org (Tier 1)

### GitHub Ecosystem (5 domains)

- github.com (Tier 1)
- docs.github.com (Tier 1)
- cli.github.com (Tier 1)
- github.blog (Tier 1)
- microsoft.github.io (Tier 1)

### Web Standards & Protocols (4 domains)

- json-schema.org (Tier 1)
- schema.org (Tier 1)
- www.w3.org (Tier 1)
- spec.modelcontextprotocol.io (Tier 1)

### Academic Research Journals (8 domains)

- arxiv.org (Tier 1)
- nature.com (Tier 1)
- science.org (Tier 1)
- pnas.org (Tier 1)
- academic.oup.com (Tier 1)
- journals.plos.org (Tier 1)
- sciencedirect.com (Tier 1)
- www.aosabook.org (Tier 1)

### University News (4 domains)

- news.mit.edu (Tier 1)
- news.stanford.edu (Tier 1)
- news.yale.edu (Tier 1)
- yaledailynews.com (Tier 2)

### Tech Company Engineering Blogs (3 domains)

- engineering.fb.com (Tier 1)
- netflixtechblog.com (Tier 1)
- www.atlassian.com (Tier 1)

### Cloud Providers (2 domains)

- aws.amazon.com (Tier 1)
- www.microsoft.com (Tier 1)

### Security & Best Practices (2 domains)

- owasp.org (Tier 1)
- martinfowler.com (Tier 1)

### Productivity Tools (2 domains)

- developers.notion.com (Tier 1)
- www.notion.com (Tier 1)

### Context7 Documentation (1 domain)

- context7.com (Tier 1)

### Other (2 domains)

- hbr.org (Tier 1 - Harvard Business Review)
- health.harvard.edu (Tier 2 - Harvard Health)

---

## Quality Assessment Framework

### News Source Evaluation Criteria

**Tier 1 Markers:**

- Multiple Pulitzer prizes or equivalent journalism awards
- 50+ year track record
- Clear editorial standards and corrections procedures
- Transparent ownership/funding disclosure
- Professional journalism staff (not pay-to-play contributors)

**Tier 2 Markers:**

- Established reputation (20+ years)
- Professional editorial oversight
- Specialized credibility in specific domains
- Active fact-checking processes

**Red Flags (Exclusions):**

- Failed fact-checks (3+)
- Pay-to-play contributor models without editorial oversight
- Hidden ownership/funding
- SEO content farms

### Technical Documentation Evaluation Criteria

**Tier 1 Markers:**

- Official documentation from maintainers/creators
- Regular updates (within 6 months)
- Comprehensive: installation, API reference, examples, best practices
- GitHub stars >50k OR official language/framework foundation
- Active community (contributors >100)

**Tier 2 Markers:**

- GitHub stars 10k-50k
- Well-maintained (updates within 12 months)
- Good documentation coverage
- Established community

**Community Trust Metrics:**

- **Critical**: GitHub stars, npm/PyPI downloads
- **Important**: Contributors, release activity, forks
- **Supporting**: Foundation status, Stack Overflow volume

---

## Usage Guidelines for Agents

### For researcher-external Agent:

1. **Prioritize Tier 1 sources** for authoritative information
2. **Use Tier 2 sources** for specialized or supporting information
3. **Use Tier 3 sources** sparingly, for emerging trends or niche topics
4. **Cross-reference** findings across multiple sources when possible
5. **Cite tier level** in research outputs for transparency

### For Other Agents with WebFetch:

- Same prioritization applies
- When researching official documentation, always use official domains (Tier 1)
- For news/current events, prefer Tier 1-A/1-B financial news sources

### Source Freshness:

- **Financial news**: Prefer sources with continuous or daily updates
- **Technical docs**: Verify last update date, prefer <6 months
- **Regulatory data**: Verify update frequency matches data type (monthly, quarterly)

---

## Maintenance & Updates

**Update Schedule**: Quarterly review (January, April, July, October)

**Update Triggers**:

- New major frameworks/libraries released
- Financial sources change credibility ratings
- Breaking changes to official documentation URLs
- User feedback on missing critical domains

**Version History**:

- v1.0.0 (2025-10-07): Initial comprehensive domain list with quality tiers
