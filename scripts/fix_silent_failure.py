file_path = "frontend/app/page.tsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 전체 features 배열 블록 교체
old_grid = """          {[
            { icon: <Zap className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Instant Alerts', description: 'Check your APIs every minute. Get instant alerts when something goes wrong.' },
            { icon: <Bell className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Multi-Channel Notifications', description: 'Email, Slack, Telegram, Discord, or custom webhooks. You choose how to be notified.' },
            { icon: <BarChart3 className="h-6 w-6 text-green-600 dark:text-green-400" />, title: '24h Response Time Graphs', description: 'Track uptime, response times, and incidents. Distinguish provider lag from your own code.' },
            { icon: <Globe className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Customizable Status Pages', description: 'Share a public status page with your users. No more "is it down?" support tickets.' },
            { icon: <Shield className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Silent Failure Detection', description: 'Catches failures even when your API returns 200 OK but something is actually broken.' },
            { icon: <CheckCircle className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Free for Commercial Use', description: 'Unlike UptimeRobot, no restrictions on free plan. Use it for your business, your clients, or your side projects.' },
          ].map((feature, i) => (
            <div key={i} className="bg-white dark:bg-gray-800 p-6 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600 hover:shadow-lg transition">
              <div className="mb-4 p-2 bg-green-50 dark:bg-green-900/30 rounded-lg w-fit">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}"""

new_grid = """          {[
            { icon: <Shield className="h-6 w-6 text-orange-500" />, title: 'Silent Failure Detection', description: 'Your API returns 200 OK — but the response body says "error". Most monitors miss this. CheckAPI catches it.', highlight: true },
            { icon: <Zap className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Instant Alerts', description: 'Check your APIs every minute. Get instant alerts when something goes wrong.' },
            { icon: <Bell className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Multi-Channel Notifications', description: 'Email, Slack, Telegram, Discord, or custom webhooks. You choose how to be notified.' },
            { icon: <BarChart3 className="h-6 w-6 text-green-600 dark:text-green-400" />, title: '24h Response Time Graphs', description: 'Track uptime, response times, and incidents. Distinguish provider lag from your own code.' },
            { icon: <Globe className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Customizable Status Pages', description: 'Share a public status page with your users. No more "is it down?" support tickets.' },
            { icon: <CheckCircle className="h-6 w-6 text-green-600 dark:text-green-400" />, title: 'Free for Commercial Use', description: 'Unlike UptimeRobot, no restrictions on free plan. Use it for your business, your clients, or your side projects.' },
          ].map((feature, i) => (
            <div key={i} className={`p-6 rounded-xl border hover:shadow-lg transition ${feature.highlight ? 'bg-orange-50 dark:bg-orange-950 border-orange-200 dark:border-orange-800 hover:border-orange-400' : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-green-300 dark:hover:border-green-600'}`}>
              <div className={`mb-4 p-2 rounded-lg w-fit ${feature.highlight ? 'bg-orange-100 dark:bg-orange-900/30' : 'bg-green-50 dark:bg-green-900/30'}`}>{feature.icon}</div>
              <h3 className={`text-lg font-semibold mb-2 ${feature.highlight ? 'text-orange-700 dark:text-orange-400' : 'text-gray-900 dark:text-white'}`}>{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{feature.description}</p>
              {feature.highlight && <p className="mt-3 text-xs font-semibold text-orange-500 uppercase tracking-wide">★ Key differentiator</p>}
            </div>
          ))}"""

if old_grid in content:
    content = content.replace(old_grid, new_grid)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("✅ 완료!")
else:
    print("❌ 못 찾음")
    # 실제 패턴 출력
    idx = content.find("'Instant Alerts'")
    print(repr(content[idx-50:idx+100]))
