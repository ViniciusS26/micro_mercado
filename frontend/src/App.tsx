
import './App.css'
import {Login} from './Login/Login'
import {Home} from './Home/Home'
import Header from './Header/Header'
import {useState} from 'react'


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [activeSection, setActiveSection] = useState('inicio')

  return (
    <>
      
      {isAuthenticated ? (
        <div className="flex min-h-screen flex-col bg-slate-900 md:flex-row">
          <Header
            activeSection={activeSection}
            onSelectSection={setActiveSection}
            onLogout={() => setIsAuthenticated(false)}
          />
          <Home activeSection={activeSection} />
        </div>
      ) : (
        <Login onLoginSuccess={() => setIsAuthenticated(true)} />
      )}
    </>
  )
}

export default App
