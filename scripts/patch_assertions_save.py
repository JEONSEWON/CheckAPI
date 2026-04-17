FILE = r"C:\home\jeon\api-health-monitor\frontend\components\AssertionsPanel.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

old_save = """        {/* Save button */}
        {assertions.length > 0 && (
          <div className="pt-2 flex gap-3">
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Assertions'}
            </button>
            <button
              onClick={() => setShowTest(!showTest)}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-700 dark:text-gray-300"
            >
              <Play className="h-3.5 w-3.5" />
              Live Test
              <ChevronDown className={`h-3.5 w-3.5 transition-transform ${showTest ? 'rotate-180' : ''}`} />
            </button>
          </div>
        )}"""

new_save = """        {/* Save button */}
        <div className="pt-2 flex gap-3">
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Assertions'}
          </button>
          {assertions.length > 0 && (
            <button
              onClick={() => setShowTest(!showTest)}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition text-gray-700 dark:text-gray-300"
            >
              <Play className="h-3.5 w-3.5" />
              Live Test
              <ChevronDown className={`h-3.5 w-3.5 transition-transform ${showTest ? 'rotate-180' : ''}`} />
            </button>
          )}
        </div>"""

c = c.replace(old_save, new_save)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", "Save Assertions" in c)
