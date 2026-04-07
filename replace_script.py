import re

with open('web-app/src/components/sections/Method/Method.tsx', 'r') as f:
    content = f.read()

old_str = re.search(r"      case 'algorithm':\n        return \([\s\S]*?            </div>\n          </motion.div>\n        \);", content).group(0)

new_str = """      case 'algorithm':
        return (
          <motion.div 
            key="algorithm"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-12"
          >
            <div className="bg-white p-4 md:p-10 rounded-3xl shadow-xl border border-slate-100 space-y-12">
              <div className="prose prose-slate max-w-none text-slate-800 leading-relaxed overflow-x-auto">
                <ReactMarkdown
                  remarkPlugins={[remarkMath]}
                  rehypePlugins={[rehypeKatex]}
                >
                  {algorithmMarkdown}
                </ReactMarkdown>
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">Human vs. Algorithmic Interface Depth (m)</h4>
                </div>
                <img src={getAssetPath('/plots/method/stats_main_0.png')} className="w-full max-w-full h-auto rounded-2xl shadow-lg border border-slate-200" alt="Stats Plot" />
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">--- LOGS WITH SINGLE INTERFACE (Primary Only) ---</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Array.from({ length: 6 }).map((_, i) => (
                    <img key={`single_${i}`} src={getAssetPath(`/plots/method/single_interface_${i}.png`)} className="w-full max-w-full h-auto rounded-xl shadow-md border border-slate-200" alt={`Single Interface ${i+1}`} />
                  ))}
                </div>
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">--- LOGS WITH DUAL INTERFACES (Primary and Secondary) ---</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Array.from({ length: 6 }).map((_, i) => (
                    <img key={`dual_${i}`} src={getAssetPath(`/plots/method/dual_interface_${i}.png`)} className="w-full max-w-full h-auto rounded-xl shadow-md border border-slate-200" alt={`Dual Interface ${i+1}`} />
                  ))}
                </div>
              </div>

              <div className="space-y-12">
                <div className="text-center border-b border-slate-100 pb-4">
                  <h4 className="text-2xl md:text-3xl font-black text-slate-800">Complete set of logs and Algorithmic vs Human interfaces</h4>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Array.from({ length: 87 }).map((_, i) => (
                    <img key={`all_${i}`} src={getAssetPath(`/plots/method/all_logs_final_${i}.png`)} className="w-full max-w-full h-auto rounded-xl shadow-sm border border-slate-100" alt={`All Logs ${i+1}`} />
                  ))}
                </div>
              </div>

            </div>
          </motion.div>
        );"""

with open('web-app/src/components/sections/Method/Method.tsx', 'w') as f:
    f.write(content.replace(old_str, new_str))
