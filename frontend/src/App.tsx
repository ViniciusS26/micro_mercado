
import './App.css'
import {Login} from './Login/Login'
import {Home} from './Home/Home'
import {useState} from 'react'


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  return (
    <>
      {isAuthenticated ? (
        <Home onLogout={() => setIsAuthenticated(false)} />
      ) : (
        <Login onLoginSuccess={() => setIsAuthenticated(true)} />
      )}
    </>
  )
}

export default App
