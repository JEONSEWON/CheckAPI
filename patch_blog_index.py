FILE_INDEX = r"C:\home\jeon\api-health-monitor\frontend\app\blog\page.tsx"

with open(FILE_INDEX, 'r', encoding='utf-8') as f:
    c = f.read()

old_posts = """const posts = [
  {
    title: 'Best Free UptimeRobot Alternatives in 2026',
    excerpt: 'UptimeRobot recently restricted commercial use on free plans. Here are the best alternatives that still offer genuinely free monitoring — no strings attached.',
    date: 'Feb 20, 2026',
    readTime: '5 min read',
    slug: '/blog/uptimerobot-alternatives',
  },
  {
    title: 'How to Monitor Your API for Free (And Actually Get Alerted)',
    excerpt: 'Free API monitoring sounds great until you realize most tools either limit you to 1 monitor or charge for alerts. Here\'s how to do it properly without paying a cent.',
    date: 'Feb 10, 2026',
    readTime: '4 min read',
    slug: '/blog/free-api-monitoring',
  },
  {
    title: 'How to Set Up Slack Alerts for API Downtime in 5 Minutes',
    excerpt: 'Step-by-step guide to getting instant Slack notifications the moment your API goes down. No code required.',
    date: 'Jan 28, 2026',
    readTime: '3 min read',
    slug: '/blog/slack-api-alerts',
  },
];"""

new_posts = """const posts = [
  {
    title: 'How to Set Up a Free Public Status Page for Your API',
    excerpt: 'A public status page reduces support tickets, builds user trust, and takes 2 minutes to set up. Here\'s how to do it for free.',
    date: 'Apr 1, 2026',
    readTime: '4 min read',
    slug: '/blog/public-status-page',
  },
  {
    title: 'API Monitoring Checklist for Solo Founders',
    excerpt: 'A practical checklist of what to monitor, how often, and what to do when things go wrong — written for indie hackers and solo founders running production APIs.',
    date: 'Mar 25, 2026',
    readTime: '4 min read',
    slug: '/blog/api-monitoring-checklist',
  },
  {
    title: 'What is a Silent API Failure? (And How to Detect It)',
    excerpt: 'Your API returns 200 OK — but the response body is empty, broken, or contains an error message. This is a silent failure, and most monitoring tools miss it entirely.',
    date: 'Mar 15, 2026',
    readTime: '5 min read',
    slug: '/blog/silent-api-failures',
  },
  {
    title: 'Best Free UptimeRobot Alternatives in 2026',
    excerpt: 'UptimeRobot recently restricted commercial use on free plans. Here are the best alternatives that still offer genuinely free monitoring — no strings attached.',
    date: 'Feb 20, 2026',
    readTime: '5 min read',
    slug: '/blog/uptimerobot-alternatives',
  },
  {
    title: 'How to Monitor Your API for Free (And Actually Get Alerted)',
    excerpt: 'Free API monitoring sounds great until you realize most tools either limit you to 1 monitor or charge for alerts. Here\'s how to do it properly without paying a cent.',
    date: 'Feb 10, 2026',
    readTime: '4 min read',
    slug: '/blog/free-api-monitoring',
  },
  {
    title: 'How to Set Up Slack Alerts for API Downtime in 5 Minutes',
    excerpt: 'Step-by-step guide to getting instant Slack notifications the moment your API goes down. No code required.',
    date: 'Jan 28, 2026',
    readTime: '3 min read',
    slug: '/blog/slack-api-alerts',
  },
];"""

c = c.replace(old_posts, new_posts)

with open(FILE_INDEX, 'w', encoding='utf-8') as f:
    f.write(c)

print("Blog index done!", c.count("slug:"))


# uptimerobot-alternatives 3 monitors → 10 수정
import re

FILE_ALT = r"C:\home\jeon\api-health-monitor\frontend\app\blog\uptimerobot-alternatives\page.tsx"

with open(FILE_ALT, 'r', encoding='utf-8') as f:
    c2 = f.read()

# 모든 "3" monitors 패턴 수정
c2 = c2.replace('Free monitors: 3', 'Free monitors: 10')
c2 = re.sub(r'(CheckAPI[^\|]*\|\s*)3(\s*\|)', r'\g<1>10\g<2>', c2)
# 혹시 테이블 셀에 단독으로 3이 있을 경우
c2 = re.sub(r'(<td[^>]*>)\s*3\s*(</td>)', r'\g<1>10\g<2>', c2)

with open(FILE_ALT, 'w', encoding='utf-8') as f:
    f.write(c2)

print("uptimerobot-alternatives fixed!")
print("'Free monitors: 10' in file:", 'Free monitors: 10' in c2)
