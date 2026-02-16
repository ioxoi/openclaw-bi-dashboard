import { useState, useEffect } from 'react'
import './App.css'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function App() {
  const [overview, setOverview] = useState(null)
  const [tasks, setTasks] = useState(null)
  const [sessions, setSessions] = useState(null)
  const [automation, setAutomation] = useState(null)
  const [tokens, setTokens] = useState(null)
  const [memory, setMemory] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, tasksRes, sessionsRes, automationRes, tokensRes, memoryRes] = await Promise.all([
          fetch('/api/overview'),
          fetch('/api/tasks'),
          fetch('/api/sessions'),
          fetch('/api/automation'),
          fetch('/api/metrics/tokens'),
          fetch('/api/memory'),
        ])
        
        setOverview(await overviewRes.json())
        setTasks(await tasksRes.json())
        setSessions(await sessionsRes.json())
        setAutomation(await automationRes.json())
        setTokens(await tokensRes.json())
        setMemory(await memoryRes.json())
      } catch (error) {
        console.error('Failed to fetch data:', error)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30s
    return () => clearInterval(interval)
  }, [])

  if (!overview) return <div className="loading">Loading...</div>

  return (
    <div className="dashboard">
      <header>
        <h1>🦞 OpenClaw BI Dashboard</h1>
        <div className="status-badge">{overview.status}</div>
      </header>

      <div className="grid">
        {/* Session Activity */}
        <div className="card">
          <h2>📊 Current Session</h2>
          {sessions && (
            <div className="metrics">
              <div className="metric">
                <span className="label">Model</span>
                <span className="value">{sessions.active_session.model.split('/')[1]}</span>
              </div>
              <div className="metric">
                <span className="label">Tokens In</span>
                <span className="value">{(sessions.active_session.tokens_in / 1000).toFixed(0)}k</span>
              </div>
              <div className="metric">
                <span className="label">Tokens Out</span>
                <span className="value">{(sessions.active_session.tokens_out / 1000).toFixed(0)}k</span>
              </div>
            </div>
          )}
        </div>

        {/* Token Usage Trend */}
        <div className="card wide">
          <h2>📈 Token Usage (Last 7 Days)</h2>
          {tokens && (
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={tokens.daily}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                <XAxis dataKey="date" stroke="#71717a" />
                <YAxis stroke="#71717a" />
                <Tooltip 
                  contentStyle={{ background: '#18181b', border: '1px solid #27272a' }}
                  labelStyle={{ color: '#a1a1aa' }}
                />
                <Line type="monotone" dataKey="tokens_in" stroke="#3b82f6" name="Input" />
                <Line type="monotone" dataKey="tokens_out" stroke="#10b981" name="Output" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Active Projects */}
        <div className="card wide">
          <h2>🎯 Active Projects</h2>
          {tasks && (
            <div className="task-list">
              {tasks.active_projects.map((task, i) => (
                <div key={i} className="task-item">
                  <div className="task-header">
                    <span className="task-id">{task.id || task.title}</span>
                    <span className={`task-status status-${task.status.toLowerCase().replace(/\s+/g, '-')}`}>
                      {task.status}
                    </span>
                  </div>
                  <div className="task-title">{task.title}</div>
                  {task.deadline && (
                    <div className="task-meta">⏰ {task.deadline}</div>
                  )}
                  {task.progress !== undefined && (
                    <div className="progress-bar">
                      <div className="progress-fill" style={{width: `${task.progress}%`}}></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Automation Status */}
        <div className="card">
          <h2>⚙️ Automation</h2>
          {automation && (
            <div className="cron-list">
              {automation.cron_jobs.map((job, i) => (
                <div key={i} className="cron-item">
                  <div className="cron-name">{job.name}</div>
                  <div className="cron-schedule">{job.schedule}</div>
                  <div className={`cron-status ${job.status}`}>●</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Memory Files */}
        <div className="card">
          <h2>🧠 Recent Memory</h2>
          {memory && (
            <div className="memory-list">
              {memory.recent_files.map((file, i) => (
                <div key={i} className="memory-item">
                  <div className="memory-name">{file.name}</div>
                  <div className="memory-size">{(file.size / 1024).toFixed(1)} KB</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <footer>
        Last updated: {new Date(overview.last_updated).toLocaleTimeString()}
      </footer>
    </div>
  )
}

export default App
