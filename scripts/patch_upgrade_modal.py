FILE = r"C:\home\jeon\api-health-monitor\frontend\components\CreateMonitorModal.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. import에 ArrowRight 추가
old_import = "import { X, Loader2, CheckCircle, XCircle } from 'lucide-react';"
new_import = "import { X, Loader2, CheckCircle, XCircle, ArrowRight, Zap } from 'lucide-react';"
content = content.replace(old_import, new_import)

# 2. state에 showUpgradeModal 추가
old_state = "  const [showAdvanced, setShowAdvanced] = useState(true);"
new_state = """  const [showAdvanced, setShowAdvanced] = useState(true);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);"""
content = content.replace(old_state, new_state)

# 3. catch에서 limit 에러 감지
old_catch = """    } catch (error: any) {
      toast.error(error.message || 'Failed to create monitor');
    } finally {"""
new_catch = """    } catch (error: any) {
      if (error.message && error.message.includes('Monitor limit reached')) {
        setShowUpgradeModal(true);
      } else {
        toast.error(error.message || 'Failed to create monitor');
      }
    } finally {"""
content = content.replace(old_catch, new_catch)

# 4. if (!isOpen) return null; 바로 뒤에 업그레이드 모달 삽입
old_check = "  if (!isOpen) return null;"
new_check = """  if (!isOpen) return null;

  if (showUpgradeModal) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl w-full max-w-md p-8 text-center">
          <div className="w-14 h-14 bg-orange-100 dark:bg-orange-900 rounded-full flex items-center justify-center mx-auto mb-4">
            <Zap className="h-7 w-7 text-orange-500" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Monitor limit reached</h2>
          <p className="text-gray-500 dark:text-gray-400 mb-2">
            You've used all <span className="font-semibold text-gray-700 dark:text-gray-300">10 monitors</span> on the Free plan.
          </p>
          <p className="text-gray-500 dark:text-gray-400 mb-6 text-sm">
            Upgrade to <span className="text-green-600 font-semibold">Starter</span> for 20 monitors and 1-minute checks, or <span className="text-green-600 font-semibold">Pro</span> for 100 monitors and faster intervals.
          </p>
          <div className="flex flex-col gap-3">
            <a
              href="/dashboard/settings?tab=billing"
              className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition font-semibold"
            >
              Upgrade Now
              <ArrowRight className="h-4 w-4" />
            </a>
            <button
              onClick={() => { setShowUpgradeModal(false); onClose(); }}
              className="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 transition text-sm"
            >
              Maybe later
            </button>
          </div>
        </div>
      </div>
    );
  }"""
content = content.replace(old_check, new_check)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
print("showUpgradeModal state:", "showUpgradeModal" in content)
print("limit error catch:", "Monitor limit reached" in content)
print("Upgrade modal JSX:", "Upgrade Now" in content)
